"""
transcript_to_srt.py — Convert a plain text transcript to .srt format
Useful when you already have a text transcript but need subtitle timestamps.

Usage:
    python transcript_to_srt.py transcript.txt --duration 600
    python transcript_to_srt.py transcript.txt --wpm 130 --output my_video.srt

The script distributes words evenly across the video duration to generate
approximate timestamps, useful when timestamps are unavailable.
"""

import argparse
import textwrap
from pathlib import Path


def seconds_to_srt_time(s: float) -> str:
    ms = int(round((s % 1) * 1000))
    s = int(s)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def text_to_srt(text: str, video_duration_secs: float,
                words_per_subtitle: int = 12) -> str:
    """
    Split plain text into subtitle blocks with estimated timestamps.

    Args:
        text: Full transcript text.
        video_duration_secs: Total video length in seconds.
        words_per_subtitle: Approximate words per subtitle card.

    Returns:
        SRT-formatted string.
    """
    words = text.split()
    if not words:
        return ""

    total_words = len(words)
    secs_per_word = video_duration_secs / total_words

    blocks = []
    idx = 1
    pos = 0

    while pos < total_words:
        chunk_words = words[pos: pos + words_per_subtitle]
        start_sec = pos * secs_per_word
        end_sec   = (pos + len(chunk_words)) * secs_per_word

        text_line = textwrap.fill(" ".join(chunk_words), width=80)
        start_ts  = seconds_to_srt_time(start_sec)
        end_ts    = seconds_to_srt_time(end_sec)

        blocks.append(f"{idx}\n{start_ts} --> {end_ts}\n{text_line}\n")
        idx += 1
        pos += words_per_subtitle

    return "\n".join(blocks)


def main():
    parser = argparse.ArgumentParser(description="Convert plain transcript to .srt")
    parser.add_argument("transcript", help="Input .txt transcript file")
    parser.add_argument("--duration", type=float, default=None,
                        help="Video duration in seconds (e.g. 600 for 10 min)")
    parser.add_argument("--wpm", type=float, default=130,
                        help="Estimated words per minute if duration unknown (default: 130)")
    parser.add_argument("--words-per-sub", type=int, default=12,
                        help="Words per subtitle card (default: 12)")
    parser.add_argument("--output", default=None,
                        help="Output .srt path (default: same name as input)")
    args = parser.parse_args()

    txt_path = Path(args.transcript)
    if not txt_path.exists():
        print(f"File not found: {txt_path}")
        return

    text = txt_path.read_text(encoding="utf-8").strip()
    word_count = len(text.split())

    if args.duration:
        duration = args.duration
    else:
        duration = (word_count / args.wpm) * 60
        print(f"  Estimated duration from {args.wpm} WPM: {duration:.0f}s ({duration/60:.1f} min)")

    srt_content = text_to_srt(text, duration, args.words_per_sub)

    out_path = Path(args.output) if args.output else txt_path.with_suffix(".srt")
    out_path.write_text(srt_content, encoding="utf-8")
    print(f"SRT saved: {out_path}  ({srt_content.count(chr(10) + chr(10))} entries)")


if __name__ == "__main__":
    main()
