"""
zip_outputs.py — Bundle all project files into a submission zip
Run after the main pipeline has completed.

Usage:
    python zip_outputs.py
    python zip_outputs.py --name submission_neha_vishwkarma
"""

import argparse
import zipfile
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Zip project outputs for submission")
    parser.add_argument("--name", default=None, help="Zip file name (without .zip)")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_name = args.name or f"subtitle_summarizer_neha_{timestamp}"
    zip_path = Path(f"{zip_name}.zip")

    include_dirs  = ["outputs", "samples"]
    include_files = [
        "subtitle_summarizer.ipynb",
        "run_pipeline.py",
        "transcript_to_srt.py",
        "zip_outputs.py",
        "requirements.txt",
        "README.md",
    ]

    print(f"Building: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        count = 0
        for fname in include_files:
            p = Path(fname)
            if p.exists():
                zf.write(p, p.name)
                print(f"  + {p.name}")
                count += 1

        for d in include_dirs:
            dp = Path(d)
            if dp.exists():
                for fp in sorted(dp.rglob("*")):
                    if fp.is_file():
                        zf.write(fp, str(fp))
                        print(f"  + {fp}")
                        count += 1

    size_kb = zip_path.stat().st_size / 1024
    print(f"\nZip ready: {zip_path}  ({count} files, {size_kb:.1f} KB)")
    print(f"Submit to: projects@newtonai.tech")


if __name__ == "__main__":
    main()
