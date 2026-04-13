"""
Evaluation harness for PHI de-identification experiments.
IMMUTABLE — the autoresearch agent must never modify this file.

Usage: uv run evaluate.py
"""

import json
import sys
import time
from pathlib import Path

from gliner2 import GLiNER2

import phi_shield

FIXTURES_DIR = Path("fixtures")
NOTES_PATH = FIXTURES_DIR / "notes.jsonl"
TRUTH_PATH = FIXTURES_DIR / "ground_truth.jsonl"
EVAL_SPLIT = 0.8  # first 80% = eval set


def load_fixtures(use_test_set=False):
    """Load notes and ground truth. By default uses eval split only."""
    notes = []
    truths = []
    with open(NOTES_PATH) as nf, open(TRUTH_PATH) as tf:
        for note_line, truth_line in zip(nf, tf):
            notes.append(json.loads(note_line))
            truths.append(json.loads(truth_line))
    split_idx = int(len(notes) * EVAL_SPLIT)
    if use_test_set:
        return notes[split_idx:], truths[split_idx:]
    return notes[:split_idx], truths[:split_idx]


def span_iou(pred_start, pred_end, true_start, true_end):
    """Character-level intersection over union."""
    overlap_start = max(pred_start, true_start)
    overlap_end = min(pred_end, true_end)
    intersection = max(0, overlap_end - overlap_start)
    union = max(pred_end, true_end) - min(pred_start, true_start)
    if union == 0:
        return 0.0
    return intersection / union


def match_entities(predicted, ground_truth, iou_threshold=0.8):
    """Match predicted entities against ground truth. Returns (tp, fp, fn)."""
    tp = 0
    matched_truth = set()
    for pred in predicted:
        best_iou = 0
        best_idx = -1
        for i, true in enumerate(ground_truth):
            if i in matched_truth:
                continue
            if pred["label"] != true["label"]:
                continue
            iou = span_iou(pred["start"], pred["end"], true["start"], true["end"])
            if iou > best_iou:
                best_iou = iou
                best_idx = i
        if best_iou >= iou_threshold and best_idx >= 0:
            tp += 1
            matched_truth.add(best_idx)
    fp = len(predicted) - tp
    fn = len(ground_truth) - len(matched_truth)
    return tp, fp, fn


def run_evaluation():
    """Run the full evaluation pipeline."""
    notes, truths = load_fixtures()

    print(f"Loading model: {phi_shield.MODEL}", file=sys.stderr)
    model = GLiNER2.from_pretrained(phi_shield.MODEL)

    labels = phi_shield.ENTITY_LABELS
    threshold = phi_shield.THRESHOLD

    total_tp = 0
    total_fp = 0
    total_fn = 0
    total_phi = 0

    start_time = time.time()

    for note, truth in zip(notes, truths):
        text = phi_shield.preprocess(note["text"])

        result = model.extract_entities(
            text,
            labels,
            threshold=threshold,
            include_spans=True,
            include_confidence=True,
        )

        # Flatten result dict into list of entities
        predicted = []
        for label, ents in result.get("entities", {}).items():
            for ent in ents:
                predicted.append({
                    "text": ent["text"],
                    "label": label,
                    "start": ent["start"],
                    "end": ent["end"],
                })

        predicted = phi_shield.postprocess(predicted)
        ground_truth = truth["entities"]
        total_phi += len(ground_truth)

        tp, fp, fn = match_entities(predicted, ground_truth)
        total_tp += tp
        total_fp += fp
        total_fn += fn

    elapsed = time.time() - start_time

    recall = total_tp / total_phi if total_phi > 0 else 0
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print("---")
    print(f"recall:           {recall:.6f}")
    print(f"precision:        {precision:.6f}")
    print(f"f1:               {f1:.6f}")
    print(f"total_phi:        {total_phi}")
    print(f"detected:         {total_tp}")
    print(f"false_positives:  {total_fp}")
    print(f"missed:           {total_phi - total_tp}")
    print(f"eval_seconds:     {elapsed:.1f}")


if __name__ == "__main__":
    run_evaluation()
