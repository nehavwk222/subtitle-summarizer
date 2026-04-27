"""
Subtitle Generator and Summarizer — Standalone Script
NewtonAI Technologies | Neha Vishwkarma

Usage:
    python run_pipeline.py                    # process all videos in ./samples/
    python run_pipeline.py --model medium     # use whisper medium model
    python run_pipeline.py --summarizer flan  # use FLAN-T5 instead of BART
"""

import os
import re
import json
import textwrap
import argparse
from pathlib import Path

# ── Argument Parser ────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Subtitle Generator and Summarizer")
parser.add_argument("--model", default="medium", choices=["tiny", "base", "small", "medium", "large"],
                    help="Whisper model size (default: medium)")
parser.add_argument("--summarizer", default="bart", choices=["bart", "flan"],
                    help="Summarization model (default: bart)")
parser.add_argument("--video-dir", default="samples", help="Folder containing video files")
parser.add_argument("--output-dir", default="outputs", help="Folder for all outputs")
parser.add_argument("--chunk-secs", type=int, default=120, help="Seconds per transcript chunk")
parser.add_argument("--max-words", type=int, default=100, help="Max words in final summary")
args = parser.parse_args()

# ── Imports ────────────────────────────────────────────────────────────────────
print("Loading libraries...")
import whisper
import torch
from moviepy.editor import VideoFileClip
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from rouge_score import rouge_scorer
from jiwer import wer as compute_wer

os.makedirs(args.output_dir, exist_ok=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Audio Extraction
# ══════════════════════════════════════════════════════════════════════════════

def extract_audio(video_path: str, output_dir: str) -> str:
    video_path = Path(video_path)
    audio_path = Path(output_dir) / (video_path.stem + ".wav")
    if audio_path.exists():
        print(f"  [skip] Audio already exists: {audio_path.name}")
        return str(audio_path)
    print(f"  Extracting audio: {video_path.name}")
    clip = VideoFileClip(str(video_path))
    clip.audio.write_audiofile(str(audio_path), verbose=False, logger=None)
    clip.close()
    return str(audio_path)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Whisper Transcription
# ══════════════════════════════════════════════════════════════════════════════

def transcribe(audio_path: str, model) -> dict:
    print(f"  Transcribing: {Path(audio_path).name}")
    result = model.transcribe(audio_path, language="en", verbose=False)
    print(f"  → {len(result['segments'])} segments | {len(result['text'].split())} words")
    return result


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — SRT Generation
# ══════════════════════════════════════════════════════════════════════════════

def seconds_to_srt_time(s: float) -> str:
    ms = int(round((s % 1) * 1000))
    s = int(s)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def segments_to_srt(segments: list) -> str:
    blocks = []
    for i, seg in enumerate(segments, 1):
        start = seconds_to_srt_time(seg["start"])
        end   = seconds_to_srt_time(seg["end"])
        text  = textwrap.fill(seg["text"].strip(), width=80)
        blocks.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(blocks)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Chunking
# ══════════════════════════════════════════════════════════════════════════════

def chunk_by_time(segments: list, chunk_secs: float) -> list:
    if not segments:
        return []
    chunks, cur_texts = [], []
    cur_start = segments[0]["start"]
    target_end = cur_start + chunk_secs

    for seg in segments:
        cur_texts.append(seg["text"].strip())
        if seg["end"] >= target_end:
            chunks.append({"text": " ".join(cur_texts), "start": cur_start, "end": seg["end"]})
            cur_texts = []
            cur_start = seg["end"]
            target_end = cur_start + chunk_secs

    if cur_texts:
        chunks.append({"text": " ".join(cur_texts), "start": cur_start, "end": segments[-1]["end"]})
    return chunks


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Summarization
# ══════════════════════════════════════════════════════════════════════════════

def build_summarizer(choice: str):
    if choice == "bart":
        print("Loading BART summarizer...")
        return pipeline("summarization", model="facebook/bart-large-cnn",
                        device=0 if device == "cuda" else -1)
    else:
        print("Loading FLAN-T5 summarizer...")
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

        def flan_summarize_fn(text, max_length=80, min_length=20, **kwargs):
            prompt = f"Summarize the following lecture content concisely:\n\n{text}"
            inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            out = model.generate(**inputs, max_new_tokens=max_length)
            return [{"summary_text": tokenizer.decode(out[0], skip_special_tokens=True)}]

        return flan_summarize_fn


def summarize_video(chunks: list, summarizer_fn, max_words: int) -> str:
    parts = []
    for i, chunk in enumerate(chunks):
        text = chunk["text"].strip()
        if len(text.split()) < 30:
            parts.append(text)
            continue
        input_len = len(text.split())
        max_out = min(80, max(30, input_len // 3))
        min_out = min(20, max_out - 10)
        result = summarizer_fn(text, max_length=max_out, min_length=min_out,
                               do_sample=False, truncation=True)
        parts.append(result[0]["summary_text"])
        print(f"    chunk {i+1}/{len(chunks)} done")
    combined = " ".join(parts)
    words = combined.split()
    if len(words) > max_words:
        combined = " ".join(words[:max_words]) + "..."
    return combined


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Evaluation (WER + ROUGE)
# ══════════════════════════════════════════════════════════════════════════════

def evaluate(transcripts: dict, summaries: dict, output_dir: str):
    """
    Compute WER and ROUGE where reference files are available.
    Drop reference .txt files named:
        {video_stem}_ref_transcript.txt
        {video_stem}_ref_summary.txt
    into the outputs/ folder and this function will auto-detect them.
    """
    scorer_obj = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    report = {"wer": {}, "rouge": {}}

    for name in transcripts:
        ref_t_path = Path(output_dir) / f"{name}_ref_transcript.txt"
        if ref_t_path.exists():
            ref_text = ref_t_path.read_text(encoding="utf-8")
            hyp_text = transcripts[name]["text"]
            score = compute_wer(ref_text, hyp_text)
            report["wer"][name] = round(score, 4)
            print(f"  WER [{name}]: {score:.2%}")

        ref_s_path = Path(output_dir) / f"{name}_ref_summary.txt"
        if ref_s_path.exists():
            ref_sum = ref_s_path.read_text(encoding="utf-8")
            scores = scorer_obj.score(ref_sum, summaries[name])
            report["rouge"][name] = {
                "rouge1_f": round(scores["rouge1"].fmeasure, 4),
                "rouge2_f": round(scores["rouge2"].fmeasure, 4),
                "rougeL_f": round(scores["rougeL"].fmeasure, 4),
            }
            print(f"  ROUGE [{name}]: R1={scores['rouge1'].fmeasure:.3f} "
                  f"R2={scores['rouge2'].fmeasure:.3f} RL={scores['rougeL'].fmeasure:.3f}")

    if not report["wer"] and not report["rouge"]:
        print("  No reference files found — add *_ref_transcript.txt / *_ref_summary.txt to enable evaluation.")

    return report


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # 1. Discover videos
    video_exts = {".mp4", ".mkv", ".avi", ".mov", ".webm"}
    video_files = sorted(p for p in Path(args.video_dir).iterdir() if p.suffix.lower() in video_exts)
    if not video_files:
        print(f"No video files found in '{args.video_dir}/'. Place .mp4/.mkv/.avi files there and rerun.")
        return
    print(f"\nFound {len(video_files)} video(s).\n")

    # 2. Load Whisper
    print(f"Loading Whisper '{args.model}' model...")
    whisper_model = whisper.load_model(args.model)
    print("Whisper ready.\n")

    # 3. Load summarizer
    summarizer = build_summarizer(args.summarizer)
    print("Summarizer ready.\n")

    transcripts, summaries = {}, {}

    for vf in video_files:
        name = vf.stem
        print(f"\n{'─'*50}")
        print(f"Processing: {vf.name}")
        print(f"{'─'*50}")

        # Extract audio
        audio_path = extract_audio(str(vf), args.output_dir)

        # Transcribe
        result = transcribe(audio_path, whisper_model)
        transcripts[name] = result
        txt_path = Path(args.output_dir) / f"{name}_transcript.txt"
        txt_path.write_text(result["text"], encoding="utf-8")
        print(f"  Transcript saved: {txt_path.name}")

        # SRT
        srt_content = segments_to_srt(result["segments"])
        srt_path = Path(args.output_dir) / f"{name}.srt"
        srt_path.write_text(srt_content, encoding="utf-8")
        print(f"  Subtitle saved:   {srt_path.name}")

        # Chunk
        chunks = chunk_by_time(result["segments"], args.chunk_secs)
        print(f"  Chunks: {len(chunks)}")

        # Summarize
        print(f"  Summarizing...")
        summary = summarize_video(chunks, summarizer, args.max_words)
        summaries[name] = summary
        sum_path = Path(args.output_dir) / f"{name}_summary.txt"
        sum_path.write_text(summary, encoding="utf-8")
        print(f"  Summary saved:    {sum_path.name}")
        print(f"  Preview: {summary[:100]}...")

    # Evaluate
    print(f"\n{'─'*50}")
    print("Evaluation")
    print(f"{'─'*50}")
    report = evaluate(transcripts, summaries, args.output_dir)

    # Save full report
    report["summaries"] = summaries
    report["config"] = vars(args)
    rpt_path = Path(args.output_dir) / "evaluation_report.json"
    rpt_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nEvaluation report: {rpt_path}")

    print(f"\n{'═'*50}")
    print("ALL DONE — outputs in ./outputs/")
    print(f"{'═'*50}")
    for name in transcripts:
        print(f"  {name}.srt | {name}_transcript.txt | {name}_summary.txt")


if __name__ == "__main__":
    main()
