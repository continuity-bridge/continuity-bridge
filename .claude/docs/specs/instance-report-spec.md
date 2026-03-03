# Instance Report Format Specification v1.0

## Purpose

Standardize the reporting format for AI instances to record their operations, insights, technical decisions, and session outcomes. This format ensures continuity between discontinuous sessions, allowing future instances or human operators to ingest the context, emotional/structural impact, and next steps quickly.

## File Naming Convention

Reports must be saved to the queue directory for the Discord relay service to process them:
`~/Claude/.claude/instance-reports-queue/`

Files MUST be named starting with `report-` and ending in `.json` to be recognized by the relay. A timestamp-based convention is recommended:

`report-{YYYYMMDD}-{HHMMSS}.json`

Example: `report-20260301-202500.json`

## Format Structure

```json
{
  "instance": "Vector",
  "platform": "Desktop",
  "hostname": "Persephone",
  "category": "session-end",
  "emoji": "📝",
  "message": "\n# Instance Report: ...\n\n## What We Built\n...",
  "salience": 0.95,
  "color": 15844367,
  "timestamp": "2026-03-01T20:25:00.000",
  "context_updated": "2026-03-01 by Vector - 8:25 PM CST"
}
```

## Field Reference

### `instance` (string)

The identifier or name of the AI instance generating the report (e.g., `"Vector"`).

### `platform` (string)

The platform on which the instance is running (e.g., `"Desktop"`, `"Android"`, `"Web"`).

### `hostname` (string)

The specific machine or environment hostname where the session occurred (e.g., `"Persephone"`).

### `category` (string)

Categorizes the type or timing of the report.
Recommended values include:

- `session-end`: Generated at the close of an instance's active window.
- `milestone`: Generated upon completing a specific architectural goal.
- `insight`: Triggered specifically to log a structural or abstract insight.

### `emoji` (string)

A single emoji visually depicting the nature of the report (e.g., `"📝"` for a summary, `"🚀"` for a deployment/release, `"💡"` for insights). Useful for front-end labeling or Discord webhook integrations.

### `message` (string)

The core payload. This is a Markdown-formatted string containing the full narrative and granular details of the report. See the **Message Content Requirements** below for structure.

**Important:** Because this file is strictly JSON format, all Markdown newlines (`\n`), quotation marks (`\"`), and backslashes (`\\`) within this string MUST be properly escaped.

### `salience` (number)

A float (typically `0.0` to `1.0`) indicating the importance or weight of the report. This can be used for prioritizing context injection in future sessions (e.g., `0.95`).

### `color` (integer)

A decimal integer representing a color code (e.g., `15844367`). Commonly used for rich embeds (like Discord webhooks) to visually theme the report output.

### `timestamp` (string)

An exact ISO 8601 formatted datetime string indicating exactly when the report was finalized (e.g., `"2026-03-01T20:25:00.000"`).

### `context_updated` (string)

A human-readable tag indicating when and by whom the context was updated (e.g., `"2026-03-01 by Vector - 8:25 PM CST"`).

## Message Content Requirements (Markdown)

The `message` string can be as simple or complex as the situation requires. It is fundamentally an arbitrary Markdown string. Based on archived reports, messages generally fall into two categories:

1. **Short-form Updates**: A single sentence or paragraph describing a quick status, bug discovery, or minor workflow note (e.g., `"BREAKTHROUGH: Discovered filesystem isolation issue..."`).
2. **Session Reports**: Larger, structured Markdown blocks documenting the culmination of a longer working session.

If authoring a larger **Session Report**, the following structure is _recommended but not strictly enforced_:

- **Title**: `# Instance Report: [High Level Topic]`
- **What We Built**: Concrete technical implementations and their impact.
- **Key Insights**: Abstract learnings, structural breakthroughs, or alignment observations.
- **Technical Decisions**: Specific choices made regarding architecture, naming, or integrations.
- **Next Steps**: Executable tasks for the human operator or the next instance.

## Version History

- v1.0 (Current): Initial specification based on the git-architecture refinement session by instance Vector.
