# judge

Grades provider answers and computes the board numbers. No provider or network code lives here.

- `evaluation.py` — Decides whether each answer is correct for its task family, and labels failures.
- `metrics.py` — Computes latency, speed, success, and failure numbers per provider and task family.
- `reporting.py` — Writes the readable `report.md` for a run.
- `tests/` — Offline tests for grading, metrics, and the report.

## Grading

- **Meeting-notes lookup** — The answer must match the ground truth or one of its listed aliases, ignoring case and extra spaces.
- **Ticket triage** — Both the category and the priority must match exactly. There is no partial credit.
- **Contract-terms extraction** — All ten fields must be present and match by type and value. The report also counts how many fields were right.

Answers that are not valid JSON or miss a field count as wrong.

## Board numbers

There is no single headline score. Each provider gets, at the 50th, 95th, and 99th percentile:

- **Time to first output** — from sending the request to the first token of any output, reasoning included.
- **Time to first answer** — from sending the request to the first visible answer token.
- **End-to-end time** — from sending the request to the last answer token.
- **Reasoning before the answer** — tokens of reasoning sent before the answer starts.
- **Output speed** — answer tokens per second, not counting reasoning. Higher is better, so the 95th and 99th figures are the slow end.

It also reports task success and failure rates over all sent requests, failures split by type (timeout, HTTP 429, other HTTP 4xx, HTTP 5xx, connection error), and the share of answers that reasoned before answering.

Requests without the needed timing event are left out of that timing number but still count in the success and failure rates. Providers are listed by end-to-end time at the 99th percentile across all task families.
