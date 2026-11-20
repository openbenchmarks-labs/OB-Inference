# data

This folder holds the system prompt templates (`prompt_templates/`) for the three task families. Question files are not committed to git.

## Public vs. held-out evaluation sets

- **Public split:** Published on Hugging Face at [`openbenchmarks/OB-Inference-Microtasks`](https://huggingface.co/datasets/openbenchmarks/OB-Inference-Microtasks).
- **Held-out split (private):** The frozen evaluation set used for the published leaderboard stays private so providers cannot train on it. Place local dataset files under `data/micro-single-task/` (gitignored) to run the benchmark.

## Files and schema

Committed in this folder:

- `prompt_templates/meeting-notes.system.txt` — System prompt for meeting-notes lookup.
- `prompt_templates/ticket-triage.system.txt` — System prompt for ticket triage.
- `prompt_templates/contract-terms.system.txt` — System prompt for contract-terms extraction.

Expected local dataset directory (`data/micro-single-task/`, gitignored):

```text
data/micro-single-task/
├── manifest.json
├── meeting-notes-lookup.jsonl
├── ticket-triage.jsonl
└── contract-terms-extraction.jsonl
```

`manifest.json` marks the release as frozen and records per-family row counts (`<rows>` is the number of lines in that family's file):

```json
{
  "status": "frozen",
  "freeze_ready": true,
  "use_cases": {
    "meeting-notes-lookup": {"private_items": <rows>},
    "ticket-triage": {"private_items": <rows>},
    "contract-terms-extraction": {"private_items": <rows>}
  }
}
```

The harness checks each count against the rows it loads. To also pin the counts in the spec, add `available_items` to each task family (and a total under `dataset`) in the spec copy you pass with `--spec`; a mismatch is then refused.

Each JSONL line is one question with `id`, `use_case`, `split`, `prompt` (`system` matching the template in `prompt_templates/` verbatim, plus `user`), `output_schema`, `gold`, `aliases`, and `tokens`. The harness validates schemas, answer types, input lengths, row counts, and file fingerprints before starting a run.
