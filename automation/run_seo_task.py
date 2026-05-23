"""
run_seo_task.py — Startup wrapper for seo_pipeline.py
Rotates through seed_topics.txt, logs output to automation/logs/
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

AUTOMATION_DIR = Path(__file__).parent
SEED_FILE = AUTOMATION_DIR / "data" / "seed_topics.txt"
COUNTER_FILE = AUTOMATION_DIR / "data" / "seed_counter.txt"
LOG_DIR = AUTOMATION_DIR / "logs"
PIPELINE = AUTOMATION_DIR / "seo_pipeline.py"


def pick_seed() -> str:
    seeds = [l.strip() for l in SEED_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    idx = int(COUNTER_FILE.read_text().strip()) if COUNTER_FILE.exists() else 0
    seed = seeds[idx % len(seeds)]
    COUNTER_FILE.write_text(str((idx + 1) % len(seeds)))
    return seed


def main():
    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f"seo_{date.today()}.log"
    seed = pick_seed()

    header = f"=== SleepWise SEO Pipeline | {date.today()} | seed: {seed} ===\n"
    print(header, end="")
    log_path.write_text(header, encoding="utf-8")

    proc = subprocess.Popen(
        [sys.executable, str(PIPELINE), "run", seed],
        cwd=str(AUTOMATION_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    with open(log_path, "a", encoding="utf-8") as lf:
        for line in proc.stdout:
            print(line, end="")
            lf.write(line)

    proc.wait()
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
