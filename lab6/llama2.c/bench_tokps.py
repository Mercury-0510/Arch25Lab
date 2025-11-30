#!/usr/bin/env python3
import subprocess
import re
import statistics
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration
WORKDIR = Path(__file__).parent
BINARIES = ["stories15M.bin", "stories42M.bin", "stories110M.bin"]  # adjust if needed
RUNNERS = ["./run", "./run_origin"]
STEPS = 256  # number of generation steps; adjust for speed
PROMPT = "Once upon a time"  # small prompt
REPEATS = 5

TOKS_RE = re.compile(r"achieved tok/s:\s*([0-9.]+)")


def run_once(exe: str, model: str) -> float:
    cmd = [exe, model, "-n", str(STEPS), "-i", PROMPT]
    try:
        proc = subprocess.run(
            cmd, cwd=WORKDIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stderr = proc.stderr
        m = TOKS_RE.search(stderr)
        if not m:
            raise RuntimeError(f"Failed to parse tok/s from {exe} {model}. stderr:\n{stderr}")
        return float(m.group(1))
    except Exception as e:
        raise RuntimeError(f"Error running {exe} {model}: {e}")


def bench() -> dict:
    results = {model: {exe: [] for exe in RUNNERS} for model in BINARIES}
    # Verify files exist
    for model in BINARIES:
        path = WORKDIR / model
        if not path.exists():
            print(f"Warning: {model} not found at {path}. Skipping.")
    # Run benchmarks
    for model in BINARIES:
        path = WORKDIR / model
        if not path.exists():
            continue
        for exe in RUNNERS:
            vals = []
            for i in range(REPEATS):
                tokps = run_once(exe, model)
                vals.append(tokps)
                print(f"{exe} {model} run {i+1}/{REPEATS}: {tokps:.3f} tok/s")
            results[model][exe] = vals
    return results


def summarize(results: dict):
    summary = {}
    for model, runners in results.items():
        summary[model] = {}
        for exe, vals in runners.items():
            if vals:
                summary[model][exe] = statistics.mean(vals)
            else:
                summary[model][exe] = None
    return summary


def plot(summary: dict, out_path: Path):
    models = [m for m in BINARIES if (WORKDIR / m).exists()]
    labels = models
    x = range(len(labels))

    run_means = [summary[m].get("./run") for m in labels]
    origin_means = [summary[m].get("./run_origin") for m in labels]

    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([i - width/2 for i in x], run_means, width, label="run", color="#4e79a7")
    ax.bar([i + width/2 for i in x], origin_means, width, label="run_origin", color="#f28e2b")

    ax.set_ylabel("tok/s (average of 5 runs)")
    ax.set_title("tok/s comparison across models")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=0)
    ax.legend()
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"Saved plot to {out_path}")


if __name__ == "__main__":
    results = bench()
    summary = summarize(results)
    plot(summary, WORKDIR / "tokps_compare.png")
