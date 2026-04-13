# phi-shield

HIPAA Safe Harbor PHI de-identification using [GLiNER2](https://github.com/fastino-ai/GLiNER2) (zero-shot NER) + the [autoresearch](https://github.com/karpathy/autoresearch) pattern for autonomous optimization.

Strips all 18 HIPAA Safe Harbor identifiers from clinical notes. Built for [CareAgent](https://github.com/careagent) — runs locally on CPU, no cloud dependency, data never leaves the device.

## Results

Optimized from baseline to production-grade in 42 autonomous experiments:

| Metric | Baseline | Final |
|--------|----------|-------|
| Recall | 57.8% | **100.0%** |
| Precision | 84.0% | **96.2%** |
| F1 | 68.4% | **98.0%** |

Evaluated on 400 synthetic clinical notes (80% eval split of 500 total) containing 5,623 PHI entities across 14 Safe Harbor types.

## What it detects

All 18 HIPAA Safe Harbor identifiers:

1. Patient names
2. Provider names
3. Dates (DOB, admission, discharge, appointment, procedure)
4. Phone/fax numbers
5. Email addresses
6. Social Security Numbers
7. Medical record numbers
8. Addresses (street, city, state, ZIP)
9. Health plan/beneficiary numbers
10. Account numbers
11. License/DEA numbers
12. Vehicle identifiers
13. Device identifiers
14. URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photos
18. Other unique identifiers

## How it works

GLiNER2 is a zero-shot NER model — you pass it text and entity type descriptions, and it scores every span against every label. `phi_shield.py` combines:

- **GLiNER2 inference** with optimized label descriptions and thresholds
- **Regex fallbacks** for structured PHI (SSN, phone, email, IP, URL, MRN patterns)
- **Context-aware name propagation** from clinical note headers
- **Note-type-aware address handling** to reduce false positives

## Setup

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/careagent/phi-shield.git
cd phi-shield
uv sync

# Generate synthetic test fixtures (one-time)
uv run prepare.py
```

## Usage

```bash
# Run evaluation against synthetic fixtures
uv run evaluate.py
```

## Running the autoresearch loop

To continue optimizing, follow the instructions in `program.md`:

```bash
git checkout -b autoresearch/<tag>
# The agent reads program.md and modifies phi_shield.py autonomously
```

## Project structure

| File | Purpose | Mutable? |
|------|---------|----------|
| `phi_shield.py` | PHI detection config — labels, thresholds, pre/post-processing | **Yes** (autoresearch target) |
| `evaluate.py` | Evaluation harness — loads fixtures, runs inference, scores | No |
| `prepare.py` | Synthetic data generator — templates + Faker | No |
| `templates.py` | 20 clinical note templates with PHI placeholders | No |
| `program.md` | Autoresearch agent instructions | No |

## License

Apache 2.0
