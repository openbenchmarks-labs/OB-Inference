# harness

Runs the benchmark and calls the providers. No grading code lives here.

- `spec.yaml` — Run settings: dataset paths, request settings, question order, smoke limits, and report columns.
- `cli.py` — Command-line runner (`init`, `smoke`, `run`, `watch`, `derive-full-run`, `list-workflows`), installed as `openbench-inference`.
- `__main__.py` — Lets `python -m harness` start the same command-line runner.
- `config.py` — Loads `spec.yaml` and the tool files, and refuses settings that break the fixed request rules.
- `providers.py` — Reads `tools/*.yaml` and builds each provider's request body and login headers.
- `transport.py` — Sends the streaming requests and records when each piece of the answer arrives.
- `dataset.py` — Checks the dataset files and fingerprints them.
- `schedule.py` — Picks 200 questions per task family and fixes the order they are asked in.
- `lifecycle.py` — Creates a run folder and locks its inputs, code, and settings before any request is sent.
- `runner.py` — Runs the smoke run and the full run, then rebuilds the results from saved data without calling anyone.
- `storage.py` — Saves every request record and checkpoint so a stopped run can resume.
- `watcher.py` — Shows run progress from local files only.
- `tests/` — Offline tests for the files above.

## How a run works

Every request uses the same settings: streaming chat completions, low reasoning, temperature 0, at most 256 output tokens, JSON output, one attempt, and a 20-second timeout. One local tokenizer counts tokens for every provider, so speed numbers stay comparable.

The questions are cycled one task family at a time. Each question goes to all providers at once, with the launch order rotated so no provider always goes first. The next question starts only after every provider has answered, failed, or timed out. Failed requests stay in the results and are never replaced.

## Commands

```sh
openbench-inference init      # check the dataset and create a run without sending requests
openbench-inference smoke     # 33 requests (one question per family per provider), at most 2 attempts and $5
openbench-inference run --full --approve-full --approval-id YOUR-AUDIT-ID   # the full 6,600-request run
openbench-inference watch --run-dir runs/micro-single-task/run-YYYYMMDD-HHMMSS
```

Add `--run-dir` to `smoke` or `run` to resume a run; finished requests are skipped. Add `--spec` to use a copy of `spec.yaml` with other dataset paths.

## Run folder

Each run lives in `runs/micro-single-task/run-YYYYMMDD-HHMMSS/`:

- `run-lock.json` — Fingerprints of the settings, dataset, chosen questions, code, provider setups, and tokenizer.
- `plan.json` — Expected request counts and spending limits.
- `checkpoints/` — Progress state used to resume.
- `raw/` — Every finished request and its streamed events. This is the source of truth.
- `artifacts/` — Chosen questions, question order, grades, metrics, provider-vs-provider comparisons, failures, and the run manifest.
- `report.md` — The readable report.
- `events.jsonl` — Run events in order.
