# PHI De-Identification Autoresearch

This is an experiment to autonomously optimize PHI (Protected Health Information)
de-identification using GLiNER2, a zero-shot NER model.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `apr12`). The branch `autoresearch/<tag>` must not already exist.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current main.
3. **Read the in-scope files**: The repo is small. Read these files for full context:
   - `README.md` — repository context.
   - `evaluate.py` — fixed evaluation harness. Do not modify.
   - `extract.py` — the file you modify. Entity labels, descriptions, thresholds, pre/post-processing.
   - `templates.py` — clinical note templates. Do not modify.
   - `prepare.py` — fixture generator. Do not modify.
4. **Verify fixtures exist**: Check that `fixtures/notes.jsonl` and `fixtures/ground_truth.jsonl` exist. If not, tell the human to run `uv run prepare.py`.
5. **Initialize results.tsv**: Create `results.tsv` with just the header row. The baseline will be recorded after the first run.
6. **Confirm and go**: Confirm setup looks good.

Once you get confirmation, kick off the experimentation.

## Experimentation

Each experiment runs on CPU. You launch it simply as: `uv run evaluate.py`.

**What you CAN do:**
- Modify `extract.py` — this is the only file you edit. Everything is fair game: entity label names, descriptions, threshold, model selection, preprocessing, postprocessing.

**What you CANNOT do:**
- Modify `evaluate.py`, `prepare.py`, `templates.py`, or anything in `fixtures/`.
- Install new packages or add dependencies.
- Modify the evaluation harness or span matching logic.

**The goal is simple: get the highest recall while keeping precision >= 0.70.**

The metric is `recall` — the percentage of PHI entities correctly detected. Higher is better. Since we're protecting against HIPAA breaches, missed PHI is far more dangerous than false positives.

**Precision floor**: If an experiment drops precision below 0.70, discard it. A model that flags everything as PHI is useless even if recall is 100%.

**Simplicity criterion**: All else being equal, simpler is better. A small recall improvement that adds ugly complexity is not worth it. Removing something and getting equal or better results is a great outcome.

**The first run**: Your very first run should always be to establish the baseline, so you will run the evaluation as is.

## Output format

Once the script finishes it prints a summary like this:

```
---
recall:           0.823400
precision:        0.789100
f1:               0.805800
total_phi:        2847
detected:         2345
false_positives:  312
missed:           502
eval_seconds:     12.3
```

You can extract the key metrics from the log file:

```
grep "^recall:\|^precision:" run.log
```

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated).

The TSV has a header row and 5 columns:

```
commit	recall	precision	status	description
```

1. git commit hash (short, 7 chars)
2. recall achieved (e.g. 0.823400) — use 0.000000 for crashes
3. precision achieved (e.g. 0.789100) — use 0.000000 for crashes
4. status: `keep`, `discard`, or `crash`
5. short text description of what this experiment tried

Example:

```
commit	recall	precision	status	description
a1b2c3d	0.723400	0.810000	keep	baseline
b2c3d4e	0.745600	0.795000	keep	expanded name descriptions for clinical context
c3d4e5f	0.710200	0.820000	discard	removed date subcategories (recall dropped)
d4e5f6g	0.000000	0.000000	crash	invalid label format caused GLiNER2 error
```

## The experiment loop

The experiment runs on a dedicated branch (e.g. `autoresearch/apr12`).

LOOP FOREVER:

1. Look at the git state: the current branch/commit we're on
2. Tune `extract.py` with an experimental idea.
3. git commit
4. Run the experiment: `uv run evaluate.py > run.log 2>&1`
5. Read out the results: `grep "^recall:\|^precision:" run.log`
6. If the grep output is empty, the run crashed. Run `tail -n 50 run.log` to read the Python stack trace and attempt a fix.
7. Record the results in the tsv (NOTE: do not commit the results.tsv file, leave it untracked by git)
8. If recall improved AND precision >= 0.70, you "advance" the branch, keeping the git commit
9. If recall is equal or worse, or precision < 0.70, you git reset back to where you started

**Crashes**: If a run crashes, use your judgment: If it's something dumb and easy to fix (e.g. a typo), fix it and re-run. If the idea itself is fundamentally broken, just skip it, log "crash", and move on.

**NEVER STOP**: Once the experiment loop has begun, do NOT pause to ask the human if you should continue. The human might be asleep. You are autonomous. If you run out of ideas, think harder — try combining previous near-misses, try more radical changes, try per-entity-type thresholds, try regex fallbacks for structured patterns, try chunking long notes. The loop runs until the human interrupts you, period.

## Experiment ideas to try

These are starting points. You should come up with your own ideas too.

**Label descriptions:**
- Make descriptions more specific to clinical note language
- Add examples to descriptions (e.g. "Names like 'Mary Johnson', 'Dr. Smith', 'RN Williams'")
- Split broad categories into sub-types (e.g. separate "appointment_date" from "date_of_birth")
- Try different phrasings — clinical vs. lay language

**Thresholds:**
- Lower global threshold to catch more entities (watch precision)
- Try per-entity-type thresholds (lower for high-risk types like SSN, higher for dates)

**Model:**
- Switch between `fastino/gliner2-base-v1` and `fastino/gliner2-large-v1`

**Preprocessing:**
- Chunk long notes into overlapping windows
- Normalize whitespace, line breaks
- Strip header formatting to reduce noise

**Postprocessing:**
- Merge adjacent spans of the same type
- Add regex fallbacks for structured patterns (SSN: \d{3}-\d{2}-\d{4}, phone numbers, emails, IPs, URLs)
- Expand partial name matches to full names
- Filter out false positives (e.g. "mg" flagged as an abbreviation)
