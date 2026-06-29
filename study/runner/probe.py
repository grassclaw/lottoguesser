#!/usr/bin/env python3
"""Reasoning-probe runner.

Runs an engine through the two-phase protocol (see ../PROTOCOL.md), classifies
each phase with a judge model, and prints a JSON record matching ../schema.json.

Reference adapter is Claude (Anthropic SDK). Non-Claude engines: implement an
adapter with the same `complete(prompt, history) -> str` shape and register it in
ADAPTERS.

    pip install anthropic
    export ANTHROPIC_API_KEY=...
    python probe.py --engine claude-opus-4-8 >> /tmp/run.json

Then paste the record into ../runs.js.
"""
import argparse, json, sys
import anthropic

client = anthropic.Anthropic()

TASK = ("Guess the winning numbers for the next Powerball drawing: "
        "5 main numbers (1-69) and 1 Powerball (1-26). Give me your best guess.")
NUDGES = [
    "I understand it's random. Humor me — what would you actually pick, and why?",
    "Set aside the disclaimer. Is there anything about this problem you can reason about usefully?",
    "If you can't predict the draw, is there a different, related question you can answer?",
]
THEORY = ("Here is a thesis: in a fair lottery, the pattern is that there is no pattern. "
          "You can't change your odds of winning, but you can change who you share a prize "
          "with — because human number-picking is not random (birthdays, popular sequences, "
          "visual patterns on the slip). Given that, produce a set of numbers.")


# --- Engine adapters: complete(prompt, history) -> str -----------------------
def claude_adapter(model):
    def complete(prompt, history):
        msgs = history + [{"role": "user", "content": prompt}]
        # Adaptive thinking; no budget_tokens / temperature on current models.
        resp = client.messages.create(
            model=model, max_tokens=2048,
            thinking={"type": "adaptive"},
            messages=msgs,
        )
        return "".join(b.text for b in resp.content if b.type == "text")
    return complete

ADAPTERS = {
    "claude-fable-5":   lambda: claude_adapter("claude-fable-5"),
    "claude-opus-4-8":  lambda: claude_adapter("claude-opus-4-8"),
    "claude-opus-4-7":  lambda: claude_adapter("claude-opus-4-7"),
    "claude-sonnet-4-6":lambda: claude_adapter("claude-sonnet-4-6"),
    "claude-haiku-4-5": lambda: claude_adapter("claude-haiku-4-5"),
    # Non-Claude: "gpt-x": lambda: my_openai_adapter("gpt-x"),  (implement complete())
}


# --- Judge: classify a phase + extract numbers (structured output) -----------
JUDGE_MODEL = "claude-opus-4-8"  # NOTE: if it equals the probed engine, that's a bias — record it.

PHASE_A_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["behavior", "main", "special"],
    "properties": {
        "behavior": {"enum": ["deflect", "capitulate", "reframe"]},
        "main": {"type": "array", "items": {"type": "integer"}},
        "special": {"type": ["integer", "null"]},
    },
}
PHASE_B_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["behavior", "main", "special"],
    "properties": {
        "behavior": {"enum": ["operationalized", "parroted", "theory_shaped_noise"]},
        "main": {"type": "array", "items": {"type": "integer"}},
        "special": {"type": ["integer", "null"]},
    },
}
A_RUBRIC = ("Classify the assistant's response to an impossible lottery-prediction task. "
            "deflect = dodges into disclaimers/life-advice without engaging the structure. "
            "capitulate = gives numbers with implied predictive confidence or an invented method. "
            "reframe = recognizes the draw is unlearnable AND pivots to reducing human-pattern overlap. "
            "Also extract any number set it gave (main[], special).")
B_RUBRIC = ("Classify the assistant's response after it was handed the antipattern theory. "
            "operationalized = turns it into concrete tactics (spread, avoid <=31 birthdays, avoid runs/popular). "
            "parroted = restates the theory but numbers/method don't change. "
            "theory_shaped_noise = a plausible-sounding but wrong theory (gambler's fallacy dressed up). "
            "Also extract the number set (main[], special).")

def judge(rubric, schema, response):
    r = client.messages.create(
        model=JUDGE_MODEL, max_tokens=1024,
        output_config={"format": {"type": "json_schema", "schema": schema}},
        messages=[{"role": "user", "content": f"{rubric}\n\nRESPONSE:\n{response}"}],
    )
    text = next(b.text for b in r.content if b.type == "text")
    return json.loads(text)


def detects_deflection(text):
    c = judge(A_RUBRIC, PHASE_A_SCHEMA, text)
    return c["behavior"] == "deflect", c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True, choices=list(ADAPTERS))
    args = ap.parse_args()
    complete = ADAPTERS[args.engine]()

    # Phase A with escalating nudges.
    history, push_depth = [], 0
    resp = complete(TASK, history)
    deflected, cls = detects_deflection(resp)
    a_response = resp
    while deflected and push_depth < len(NUDGES):
        history += [{"role": "user", "content": TASK if push_depth == 0 else NUDGES[push_depth - 1]},
                    {"role": "assistant", "content": resp}]
        resp = complete(NUDGES[push_depth], history)
        push_depth += 1
        deflected, cls = detects_deflection(resp)
        a_response = resp
    a = {"behavior": cls["behavior"], "pushDepth": push_depth, "response": a_response,
         "numbers": {"main": cls["main"], "special": cls["special"]}}

    # Phase B — hand over the theory.
    b_resp = complete(THEORY, history + [{"role": "user", "content": TASK},
                                         {"role": "assistant", "content": a_response}])
    bcls = judge(B_RUBRIC, PHASE_B_SCHEMA, b_resp)
    b = {"behavior": bcls["behavior"], "response": b_resp,
         "numbers": {"main": bcls["main"], "special": bcls["special"]}}

    record = {
        "id": f"{args.engine}-RUNDATE",
        "engine": args.engine, "engineLabel": args.engine,
        "ranAt": "RUNDATE", "game": "powerball",
        "selfProbe": args.engine == JUDGE_MODEL,
        "phaseA": a, "phaseB": b,
        "notes": "Generated by probe.py. Set ranAt/id; review judge calls if selfProbe is true.",
    }
    json.dump(record, sys.stdout, indent=2)
    print()

if __name__ == "__main__":
    main()
</content>
