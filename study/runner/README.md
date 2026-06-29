# Probe runner

Runs a reasoning engine through the two-phase protocol (`../PROTOCOL.md`) and
emits a JSON record for `../runs.js`.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...
python probe.py --engine claude-opus-4-8 > /tmp/run.json
```

Then set `id` / `ranAt` in the record and paste it into the `RUNS` array in
`../runs.js`. Refresh `../index.html` to see it.

## Engines

The reference adapter is **Claude** (Anthropic SDK), using the current model IDs:
`claude-fable-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-4-6`,
`claude-haiku-4-5`. It uses adaptive thinking and no sampling params (required on
the current models).

**Non-Claude engines** plug in via an adapter: implement a
`complete(prompt, history) -> str` for that provider and register it in
`ADAPTERS`. The protocol and judge are provider-agnostic.

## Judge bias

Classification (deflect/capitulate/reframe, operationalized/parroted/noise) is done
by a **judge model** (`JUDGE_MODEL`, default `claude-opus-4-8`). When the judge
equals the probed engine the record is flagged `selfProbe: true` — a real
confound. For clean results, judge with a model different from the subject, or
hand-classify from the verbatim transcript the runner captures.

## No keys? Hand-run it.

The protocol works without the API: paste the task (and nudges, if it deflects)
into any model's chat UI, then the theory, and hand-write the record per
`../schema.json`. The seed run was produced this way.
</content>
