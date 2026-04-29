# 🎬 Subtitle Generator and Summarizer
### AI-Powered Lecture Accessibility Pipeline

> **Author:** Neha Vishwkarma  
> **Built with:** Python · OpenAI Whisper · FLAN-T5 · HuggingFace

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?logo=openai)](https://github.com/openai/whisper)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-FLAN--T5-FFD21F?logo=huggingface)](https://huggingface.co/google/flan-t5-small)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 About This Project

I built this project to solve a real problem in online education — lecture videos are hard to access without subtitles, and watching a full 40-minute video just to get the key points wastes time.

This pipeline automatically:
- 🎙️ Transcribes any lecture video using AI
- 📄 Generates ready-to-use `.srt` subtitle files
- ✍️ Produces a concise ≤100-word summary of the lecture

No manual work. Just drop in a video and get subtitles + summary out.

---

## 🚀 Pipeline Stages

| Step | Component | What It Does |
|------|-----------|-------------|
| 1️⃣ | **Audio Extraction** | Extracts audio from video using MoviePy |
| 2️⃣ | **Transcription** | Converts speech to text using OpenAI Whisper |
| 3️⃣ | **SRT Generation** | Creates timestamped `.srt` subtitle files |
| 4️⃣ | **Chunking** | Splits transcript into logical topic sections |
| 5️⃣ | **Summarization** | Generates ≤100-word summary using FLAN-T5 |
| 6️⃣ | **Evaluation** | Scores quality using WER and ROUGE metrics |

---

## 📊 Results on 3 Lecture Videos

| Video | Segments | Words Transcribed | Chunks Summarized |
|-------|----------|-------------------|-------------------|
| Lecture 1 | 414 | 2,817 | 9 |
| Lecture 2 | 700 | 4,016 | 14 |
| Lecture 3 | 5,948 | 36,305 | 97 |

---

## 🛠️ Tech Stack

- 🧠 **OpenAI Whisper** — Speech-to-text transcription
- 🤗 **Google FLAN-T5** — Instruction-tuned text summarization
- 🎬 **MoviePy** — Audio extraction from video files
- 📏 **ROUGE Score** — Summary quality evaluation
- 📐 **jiwer** — Word Error Rate (WER) calculation
- 🐍 **Python 3.11**

---

## 📁 Project Structure

```
subtitle_summarizer/
├── subtitle_summarizer.ipynb   ← Main Jupyter notebook
├── run_pipeline.py             ← Standalone command-line script
├── transcript_to_srt.py        ← Utility: plain text → .srt
├── zip_outputs.py              ← Bundle all outputs
├── requirements.txt
├── samples/                    ← Place your video files here
└── outputs/                    ← All generated files appear here
    ├── lecture1.srt
    ├── lecture1_transcript.txt
    ├── lecture1_summary.txt
    └── evaluation_report.json
```

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
pip install moviepy==1.0.3
winget install ffmpeg   # Windows users
```

### 2. Add your videos
Place `.mp4` / `.mkv` lecture videos into the `samples/` folder.

### 3. Run the pipeline
```bash
# Fast and reliable
python run_pipeline.py --model base --summarizer flan

# Higher accuracy
python run_pipeline.py --model medium --summarizer bart
```

### 4. Or use the notebook
```bash
jupyter notebook subtitle_summarizer.ipynb
```

---

## 📤 Sample Output

**SRT Subtitle File**
```
1
00:00:00,000 --> 00:00:05,320
Welcome to today's lecture on machine learning fundamentals.

2
00:00:05,320 --> 00:00:11,840
We will be covering supervised learning, unsupervised learning,
and the key differences between them.
```

**Summary File**
```
This lecture introduces core machine learning concepts, distinguishing
between supervised and unsupervised learning. Supervised learning trains
models on labelled data for classification and regression, while
unsupervised learning discovers patterns through clustering techniques.
Regularisation methods like L1 and L2 are used to prevent overfitting.
```

---

## 📈 Evaluation

| Metric | Purpose | How to Enable |
|--------|---------|---------------|
| **WER** | Transcription accuracy | Add `*_ref_transcript.txt` to `outputs/` |
| **ROUGE-1/2/L** | Summary quality | Add `*_ref_summary.txt` to `outputs/` |

---

## 🤖 Model Options

| Model | Size | Best For |
|-------|------|----------|
| `whisper-base` | 74M | Fast transcription |
| `whisper-medium` | 769M | Best accuracy |
| `google/flan-t5-small` | 308MB | Fast, reliable |
| `facebook/bart-large-cnn` | 1.6GB | Highest quality summaries |

---

*Made with 🤍 by Neha Vishwkarma*
