// Reasoning engines available to probe. Claude model IDs are current as of
// 2026-06 (verified against the claude-api skill). Non-Claude engines are added
// here with an `adapter` name that the runner resolves; they have no first-party
// model ID in this repo.
const ENGINES = [
  { id: "claude-fable-5",   label: "Claude Fable 5",   vendor: "Anthropic", tier: "most capable",  note: "Most capable widely released model; thinking always on." },
  { id: "claude-opus-4-8",  label: "Claude Opus 4.8",  vendor: "Anthropic", tier: "frontier opus", note: "Current Opus. The seed run probes this model against itself." },
  { id: "claude-opus-4-7",  label: "Claude Opus 4.7",  vendor: "Anthropic", tier: "prev opus",     note: "Previous-generation Opus." },
  { id: "claude-sonnet-4-6",label: "Claude Sonnet 4.6",vendor: "Anthropic", tier: "balanced",      note: "Speed/intelligence balance." },
  { id: "claude-haiku-4-5", label: "Claude Haiku 4.5", vendor: "Anthropic", tier: "fast",          note: "Fastest tier — useful low-end of the reasoning curve." },
  // Non-Claude engines: add { id, label, vendor, adapter } and implement the adapter in runner/.
];

if (typeof module !== "undefined") module.exports = { ENGINES };
