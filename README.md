# 🎬 Subtitle Generator & Summarizer

> An AI-powered pipeline for automatic lecture transcription, subtitle generation, and summarization — built for edtech accessibility at scale.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-orange)](https://github.com/openai/whisper)
[![FLAN-T5](https://img.shields.io/badge/Google-FLAN--T5-green)](https://huggingface.co/google/flan-t5-small)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 📌 Overview

This project was developed as part of the **NewtonAI Technologies Research Programme**. It addresses a real-world challenge faced by edtech platforms: processing large volumes of recorded lecture videos to generate accurate subtitles and concise summaries — automatically, at scale.

The pipeline takes a raw video file as input and produces:
- ✅ A timestamped **SRT subtitle file** (compatible with VLC, YouTube, and all major platforms)
- ✅ A full **text transcript**
- ✅ A concise **summary** (under 100 words)
- ✅ An **evaluation report** (WER and ROUGE scores)

---

## ✨ Features

- 🎙️ **High-accuracy transcription** using OpenAI Whisper (base model, CPU-compatible)
- 📄 **Industry-standard SRT output** with millisecond-accurate timestamps and 80-character line wrapping
- 🧠 **Intelligent summarization** using Google FLAN-T5 Small via HuggingFace Transformers
- ⏱️ **Time-based chunking** to preserve semantic coherence across long lectures
- 📊 **Built-in evaluation** with WER (jiwer) and ROUGE scoring
- 🎞️ **Handles variable-length videos** — tested from short clips up to 40+ minute lectures
- 🧩 **Modular architecture** — each stage can be upgraded or replaced independently

---

## 🏗️ System Architecture

```
Video File (.mp4)
     │
     ▼
┌─────────────────┐
│  Audio Extraction│  ← MoviePy
│  (.wav output)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transcription  │  ← OpenAI Whisper (base)
│  + Timestamps   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│  SRT   │ │   Chunking   │  ← 2-minute time windows
│ File   │ │  + Summarize │  ← FLAN-T5 Small
└────────┘ └──────────────┘
                │
                ▼
         ┌────────────┐
         │  Evaluation│  ← WER + ROUGE
         └────────────┘
```

### Pipeline Stages

| Stage | Component | Input | Output |
|---|---|---|---|
| 1. Audio Extraction | MoviePy 1.0.3 | Video file (`.mp4`) | Audio file (`.wav`) |
| 2. Transcription | OpenAI Whisper base | Audio (`.wav`) | Timestamped segments + text |
| 3. SRT Generation | Custom Python | Whisper segments | Subtitle file (`.srt`) |
| 4. Chunking | Custom Python | Transcript segments | ~2-min text chunks |
| 5. Summarization | FLAN-T5 Small | Text chunks | Summary (`.txt`) |
| 6. Evaluation | jiwer + rouge-score | Transcripts + summaries | Metrics (`.json`) |

---

## 📁 Project Structure

```
subtitle_summarizer/
│
├── subtitle_summarizer.ipynb    # Main Jupyter notebook (interactive)
├── run_pipeline.py              # Standalone command-line script
├── transcript_to_srt.py         # Utility: plain text → SRT conversion
├── zip_outputs.py               # Bundles all outputs for submission
├── requirements.txt             # Python dependencies
│
├── samples/                     # Place your input video files here
│   ├── lecture1.mp4
│   ├── lecture2.mp4
│   └── lecture3.mp4
│
└── outputs/                     # All generated files appear here
    ├── lecture1.srt
    ├── lecture1_transcript.txt
    ├── lecture1_summary.txt
    ├── lecture2.srt
    ├── lecture2_transcript.txt
    ├── lecture2_summary.txt
    ├── lecture3.srt
    ├── lecture3_transcript.txt
    ├── lecture3_summary.txt
    └── evaluation_report.json
```

---

## ⚙️ Tech Stack

| Library / Tool | Version | Purpose |
|---|---|---|
| Python | 3.11 | Primary programming language |
| OpenAI Whisper | 20231117+ | Speech-to-text transcription |
| FLAN-T5 Small | HuggingFace | Text summarization |
| MoviePy | 1.0.3 | Audio extraction from video |
| HuggingFace Transformers | 4.38+ | Model loading and inference |
| PyTorch | 2.0+ | Deep learning framework |
| rouge-score | 0.1.2+ | Summary evaluation |
| jiwer | 3.0+ | Word Error Rate calculation |
| ffmpeg | 8.1 | Audio decoding (Whisper dependency) |
| yt-dlp | latest | YouTube video download |

---

## 🚀 Getting Started

### System Requirements

- Windows 10 or later (64-bit) — also works on macOS/Linux
- Python 3.9 or later (3.11 recommended)
- Minimum 8 GB RAM
- Minimum 5 GB free disk space (for models and outputs)
- Internet connection (for initial model downloads only)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/subtitle-summarizer.git
cd subtitle-summarizer
```

**2. Install Python dependencies**

```bash
pip install -r requirements.txt
pip install moviepy==1.0.3
```

> ⚠️ Pinning `moviepy==1.0.3` is important — version 2.x removed the `moviepy.editor` import used in this project.

**3. Install ffmpeg**

Whisper requires ffmpeg for audio decoding.

- **Windows (via winget):**
  ```bash
  winget install ffmpeg
  ```
  Then close and reopen your terminal to reload `PATH`.

- **macOS (via Homebrew):**
  ```bash
  brew install ffmpeg
  ```

- **Ubuntu/Debian:**
  ```bash
  sudo apt install ffmpeg
  ```

**4. Add your video files**

Place your `.mp4` or `.mkv` lecture files inside the `samples/` folder.

---

## ▶️ Running the Pipeline

### Option A — Command Line (recommended)

```bash
python run_pipeline.py --model base --summarizer flan
```

| Argument | Options | Default | Description |
|---|---|---|---|
| `--model` | `tiny`, `base`, `small`, `medium`, `large` | `base` | Whisper model size |
| `--summarizer` | `flan`, `bart` | `flan` | Summarization model |

### Option B — Jupyter Notebook (interactive)

```bash
jupyter notebook subtitle_summarizer.ipynb
```

Run the cells step by step to see intermediate outputs, including transcription segments and chunk previews.

### Bundle outputs for submission

```bash
python zip_outputs.py
```

This creates a `subtitle_summarizer_outputs.zip` containing all generated files.

---

## 📊 Sample Results

Three YouTube lecture videos (AI/tech topics) were processed as part of this project:

| Video | Segments | Word Count | Chunks | Processing Time |
|---|---|---|---|---|
| Lecture 1 (~10 min) | 414 | 2,817 | 9 | ~3.5 minutes |
| Lecture 2 (~15 min) | 700 | 4,016 | 14 | ~7.5 minutes |
| Lecture 3 (~40 min) | 5,948 | 36,305 | 97 | ~41 minutes |

> All processing was done on a standard consumer laptop with **CPU-only computation**.

---

## 📐 Output Format

### SRT Subtitle File

```
1
00:00:00,000 --> 00:00:04,200
Welcome to this lecture on machine learning fundamentals.

2
00:00:04,200 --> 00:00:09,600
Today we'll cover supervised and unsupervised learning approaches.
```

### Summary File

```
This lecture covers the fundamentals of machine learning, focusing on 
supervised and unsupervised learning techniques. Key topics include 
classification, regression, clustering, and dimensionality reduction. 
Practical examples using scikit-learn are demonstrated throughout.
```

---

## 📏 Evaluation

### Word Error Rate (WER)

WER measures transcription accuracy against a ground-truth reference:

```
WER = (Substitutions + Insertions + Deletions) / Total Reference Words
```

- Whisper base typically achieves **6–10% WER** on clear English lecture audio.
- State-of-the-art systems achieve below 5%.

### ROUGE Scores

ROUGE measures summary quality vs. reference summaries:

| Metric | Description | Target Range |
|---|---|---|
| ROUGE-1 | Unigram overlap | 0.40 – 0.60 |
| ROUGE-2 | Bigram overlap | 0.15 – 0.35 |
| ROUGE-L | Longest common subsequence | 0.35 – 0.55 |

**To compute scores against your own reference transcripts/summaries:**

Place reference files in `outputs/` with the naming convention:
- `lecture1_ref_transcript.txt`
- `lecture1_ref_summary.txt`

Then re-run the pipeline — evaluation scores will be computed automatically and saved to `outputs/evaluation_report.json`.

---

## 🔧 Whisper Model Comparison

Choose your model based on your hardware and accuracy requirements:

| Model | Parameters | VRAM | Relative Speed | Recommended For |
|---|---|---|---|---|
| tiny | 39M | ~1 GB | ~32x | Quick testing |
| **base (default)** | **74M** | **~1 GB** | **~16x** | **CPU / standard hardware** |
| small | 244M | ~2 GB | ~6x | Better accuracy |
| medium | 769M | ~5 GB | ~2x | High accuracy, GPU recommended |
| large | 1550M | ~10 GB | ~1x | Best accuracy, GPU required |

---

## 🐛 Known Issues & Fixes

| Issue | Cause | Fix |
|---|---|---|
| `moviepy.editor` import error | moviepy 2.x removed legacy imports | Pin to `moviepy==1.0.3` |
| Keras compatibility error | TensorFlow/Keras 3 incompatible with Transformers | Install `pip install tf-keras==2.21.0` |
| BART download timeout | `facebook/bart-large-cnn` is 1.6 GB | Use `flan-t5-small` (308 MB) instead |
| `ffmpeg not found` error | ffmpeg not on system PATH | Install ffmpeg and reopen terminal |
| `unzip` not recognized (Windows) | Windows CMD lacks `unzip` | Use right-click → Extract All in Explorer |

---

## 🔮 Future Improvements

- [ ] Upgrade to Whisper `medium` or `large` for improved accuracy with technical terminology and non-native speakers
- [ ] Integrate `BART Large CNN` or `FLAN-T5 Base` for higher-quality summaries
- [ ] Add GPU support to reduce 40-minute processing to under 5 minutes
- [ ] Implement speaker diarization to label different speakers
- [ ] Add automatic language detection for non-English lectures
- [ ] Build a web interface with Flask or Streamlit
- [ ] Integrate with LMS APIs (Moodle, Canvas) for fully automated workflows

---

## 📖 References

- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision.* OpenAI. https://openai.com/research/whisper
- Chung, H. W. et al. (2022). *Scaling Instruction-Finetuned Language Models.* Google Research. https://arxiv.org/abs/2210.11416
- Lewis, M. et al. (2020). *BART: Denoising Sequence-to-Sequence Pre-training.* Facebook AI. https://arxiv.org/abs/1910.13461
- Lin, C. Y. (2004). *ROUGE: A Package for Automatic Evaluation of Summaries.* ACL.
- HuggingFace Transformers Docs: https://huggingface.co/docs/transformers
- OpenAI Whisper GitHub: https://github.com/openai/whisper

---

## 👩‍💻 Author

**Neha Vishwkarma**
Research Intern, NewtonAI Technologies
📧 projects@newtonai.tech

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
