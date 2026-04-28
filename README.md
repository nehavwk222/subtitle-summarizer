# Subtitle Generator and Summarizer
---

## Project Overview

An AI pipeline that:
1. Extracts audio from lecture videos
2. Transcribes speech using **OpenAI Whisper**
3. Generates **SRT subtitle files** with accurate timestamps
4. Produces **concise summaries** (≤ 100 words) using **BART** or **FLAN-T5**
5. Evaluates using **Word Error Rate (WER)** and **ROUGE** scores

---

## Project Structure

```
subtitle_summarizer/
├── subtitle_summarizer.ipynb   ← Main Jupyter notebook (interactive)
├── run_pipeline.py             ← Standalone pipeline script
├── transcript_to_srt.py        ← Utility: plain text → .srt conversion
├── zip_outputs.py              ← Bundle outputs for submission
├── requirements.txt
├── README.md
├── samples/                    ← Place your video files here
│   ├── lecture1.mp4
│   ├── lecture2.mp4
│   └── lecture3.mp4
└── outputs/                    ← All generated files appear here
    ├── lecture1.wav
    ├── lecture1_transcript.txt
    ├── lecture1.srt
    ├── lecture1_summary.txt
    ├── lecture2.wav
    ├── ...
    └── evaluation_report.json
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your videos
Copy 3–5 lecture videos (10–15 min each) into the `samples/` folder.  
Supported formats: `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`

---

## Running the Pipeline

### Option A — Jupyter Notebook (recommended)
```bash
jupyter notebook subtitle_summarizer.ipynb
```
Run cells top to bottom. Each section is clearly labeled.

### Option B — Command-line script
```bash
# Default (Whisper medium + BART)
python run_pipeline.py

# Faster (smaller Whisper model)
python run_pipeline.py --model base

# Use FLAN-T5 instead of BART
python run_pipeline.py --summarizer flan

# All options
python run_pipeline.py --model medium --summarizer bart --chunk-secs 120 --max-words 100
```

### Convert an existing transcript to SRT
```bash
python transcript_to_srt.py outputs/lecture1_transcript.txt --duration 600
```

---

## Outputs

| File | Description |
|------|-------------|
| `{name}.srt` | Subtitle file with accurate timestamps |
| `{name}_transcript.txt` | Full Whisper transcription |
| `{name}_summary.txt` | ≤ 100-word AI-generated summary |
| `evaluation_report.json` | WER + ROUGE scores (if references provided) |

---

## Evaluation

### WER (Word Error Rate)
To compute WER, place reference transcript files in `outputs/`:
```
outputs/lecture1_ref_transcript.txt
outputs/lecture2_ref_transcript.txt
```
WER will be computed automatically on the next pipeline run.

### ROUGE Score
To compute ROUGE, place reference summary files in `outputs/`:
```
outputs/lecture1_ref_summary.txt
```

---

## Model Choices

| Model | Type | Notes |
|-------|------|-------|
| `whisper-medium` | Transcription | Best accuracy for lecture audio |
| `whisper-base` | Transcription | Faster, slightly less accurate |
| `facebook/bart-large-cnn` | Summarization | High-quality news/lecture summaries |
| `google/flan-t5-base` | Summarization | Lighter, instruction-tuned alternative |

---
