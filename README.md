<div align="center">

# 🎬 Subtitle Generator & Summarizer

### AI-powered pipeline that turns raw lecture videos into subtitles + summaries — automatically.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Whisper](https://img.shields.io/badge/OpenAI_Whisper-base-412991?style=for-the-badge)](https://github.com/openai/whisper)
[![FLAN-T5](https://img.shields.io/badge/FLAN--T5-small-4285F4?style=for-the-badge&logo=google)](https://huggingface.co/google/flan-t5-small)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

> Built for edtech platforms that need to process hundreds of lecture videos without manual effort.

</div>

---

## 🚀 What It Does

Drop in a lecture video → get back three things instantly:

| Output | Description |
|--------|-------------|
| 📄 `.srt` subtitle file | Timestamped, millisecond-accurate, compatible with VLC / YouTube |
| 📝 Full transcript | Every word, plain text |
| 🧠 Summary | Concise, under 100 words |

**Tested on videos from 10 minutes up to 40+ minutes. Runs entirely on CPU — no GPU needed.**

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-username/subtitle-summarizer.git
cd subtitle-summarizer

# 2. Install dependencies
pip install -r requirements.txt
pip install moviepy==1.0.3

# 3. Install ffmpeg (required by Whisper)
winget install ffmpeg        # Windows
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Ubuntu

# 4. Add your video to the samples/ folder, then run
python run_pipeline.py --model base --summarizer flan
```

> Outputs will appear in the `outputs/` folder automatically.

---

## 🏗️ How the Pipeline Works

```
  📹 Video (.mp4)
       │
       ▼
  🔊 Audio Extraction      ← MoviePy
       │
       ▼
  📝 Transcription         ← OpenAI Whisper (base)
       │
       ├──────────────────────────┐
       ▼                          ▼
  📄 SRT File              🧩 Chunking (~2 min blocks)
                                  │
                                  ▼
                           🧠 Summarization      ← FLAN-T5 Small
                                  │
                                  ▼
                           📊 Evaluation         ← WER + ROUGE
```

Each stage is independent — swap any model without touching the rest.

---

## 📊 Results on Real Lectures

| Video | Duration | Segments | Words | Processing Time |
|-------|----------|----------|-------|-----------------|
| Lecture 1 | ~10 min | 414 | 2,817 | ~3.5 min |
| Lecture 2 | ~15 min | 700 | 4,016 | ~7.5 min |
| Lecture 3 | ~40 min | 5,948 | 36,305 | ~41 min |

All processed on a **standard laptop, CPU only.**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `OpenAI Whisper` base | Speech-to-text transcription |
| `Google FLAN-T5 Small` | Text summarization |
| `MoviePy 1.0.3` | Audio extraction |
| `HuggingFace Transformers` | Model loading |
| `jiwer` | Word Error Rate (WER) evaluation |
| `rouge-score` | Summary quality (ROUGE) evaluation |
| `ffmpeg` | Audio decoding |

---

## 📁 Project Structure

```
subtitle-summarizer/
├── subtitle_summarizer.ipynb   ← Interactive notebook
├── run_pipeline.py             ← Run from command line
├── transcript_to_srt.py        ← Convert plain text → SRT
├── zip_outputs.py              ← Bundle outputs for sharing
├── requirements.txt
├── samples/                    ← Put your videos here
└── outputs/                    ← All results go here
    ├── lecture1.srt
    ├── lecture1_transcript.txt
    ├── lecture1_summary.txt
    └── evaluation_report.json
```

---

## ⚠️ Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| `moviepy.editor` import error | Run `pip install moviepy==1.0.3` |
| `ffmpeg not found` | Install ffmpeg and **reopen** your terminal |
| BART model download timeout | Use `--summarizer flan` (308 MB vs 1.6 GB) |
| Keras compatibility error | Run `pip install tf-keras==2.21.0` |

---

## 🔮 What's Next

- [ ] Whisper `medium` / `large` for better accuracy on technical terms  
- [ ] GPU support to cut 40-min processing down to ~5 minutes  
- [ ] Speaker diarization — label who is talking  
- [ ] Streamlit web interface for non-technical users  
- [ ] Direct LMS integration (Moodle, Canvas)  

---

## 📖 References

- [OpenAI Whisper](https://github.com/openai/whisper) — Radford et al., 2022  
- [FLAN-T5](https://arxiv.org/abs/2210.11416) — Chung et al., 2022  
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)  

---

<div align="center">

Made with ❤️ by **Neha Vishwkarma** · NewtonAI Technologies · `projects@newtonai.tech`

</div>
