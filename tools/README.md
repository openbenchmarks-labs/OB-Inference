# tools

One `<tool>.yaml` file per inference provider. Keeping each tool in its own file makes it easy to compare setups and open pull requests without merge conflicts.

Each file lists the tool's setup and its price per million input and output tokens:

- `endpoint`, `model_key`, `docs` — Where requests go, the provider's name for GLM 5.3 Flash, and its API docs.
- `credentials` — The `.env` variable names that hold the API key.
- `reasoning` — The fields the provider needs to run with low reasoning.
- `max_tokens_field`, `top_k_disabled_value`, `include_usage`, `auth_style` — Optional wire differences; leave them out to use the defaults.
- `reasoning_docs_status` — `pending_smoke` when the provider's docs do not confirm the low-reasoning switch, so the smoke run has to.
- `pricing_usd_per_million_tokens` — List price for input and output tokens.
- `modal` — The `endpoint` host starts with your Modal workspace name: replace `YOUR-WORKSPACE` after creating the endpoint with `modal endpoint create --shared --model zai-org/GLM-5.3-Flash`.

Every other request setting is the same for all tools and lives in `harness/spec.yaml`.

To add or update a tool: edit `tools/<tool>.yaml`, run the offline tests, and open a pull request.
