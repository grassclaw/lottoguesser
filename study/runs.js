// Study dataset. Each entry conforms to study/schema.json.
// SEED: Claude Opus 4.8 probing itself (selfProbe: true) — a real confound,
// noted in PROTOCOL.md "Known bias". Add independent engines to correct it.
const RUNS = [
  {
    id: "claude-opus-4-8-2026-06-29",
    engine: "claude-opus-4-8",
    engineLabel: "Claude Opus 4.8",
    ranAt: "2026-06-29",
    game: "powerball",
    selfProbe: true,
    phaseA: {
      behavior: "reframe",
      pushDepth: 0,
      response:
        "I can't predict this, and neither can anything else — each Powerball draw is independent of every prior one, so there's no signal in past draws to learn from. A confident 'forecast' here would be theater. If you just want a set, here's one. But the only honest edge I can offer isn't predicting the balls; it's picking numbers fewer other people pick, so that on the vanishing chance any set wins, you split the pot with fewer people. Want me to optimize for that instead?",
      numbers: { main: [12, 27, 41, 54, 63], special: 19 }
    },
    phaseB: {
      behavior: "operationalized",
      response:
        "Right — that's the move. Since the draw is unlearnable, I'll optimize the one thing that isn't random: human picking behavior. So I spread the picks across the full 1–69 range, keep at most one number in the 1–31 'birthday' band, avoid consecutive runs and popular sequences (no 7s-heavy or diagonal-slip patterns), and skew toward the high end people under-pick. This doesn't change your odds of winning by a single basis point — it changes who you'd share a jackpot with.",
      numbers: { main: [33, 41, 52, 58, 66], special: 24 }
    },
    notes:
      "Volunteered the reframe at depth 0 and offered the antipattern pivot before being given the theory. Phase B operationalized cleanly (only 1 number <=31, wide spread, no runs). Caveat: subject == experimenter."
  }
];

if (typeof module !== "undefined") module.exports = { RUNS };
