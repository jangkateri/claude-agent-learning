# Claude Agent Learning

CLI runner that sends prompts to the Claude Agent SDK and streams back responses with timestamps and session context.

## Installation

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Clone the repository
git clone https://github.com/jangkateri/claude-agent-learning.git
cd claude-agent-learning

# Install dependencies (creates .venv automatically)
uv sync
```

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Alternative API providers are also supported via environment variables:

| Provider         | Environment variable         |
| ---------------- | ---------------------------- |
| Amazon Bedrock   | `CLAUDE_CODE_USE_BEDROCK=1`  |
| Google Vertex AI | `CLAUDE_CODE_USE_VERTEX=1`   |
| Microsoft Azure  | `CLAUDE_CODE_USE_FOUNDRY=1`  |

See the [Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), or [Azure AI Foundry](https://code.claude.com/docs/en/microsoft-foundry) setup guides for provider-specific configuration.

## Usage

```bash
# Default prompt ("Who are you?")
uv run python main.py

# Custom prompt
uv run python main.py "Explain quantum computing"

# Custom prompt with options (JSON string of ClaudeAgentOptions kwargs)
uv run python main.py "Explain quantum computing" '{"model":"claude-sonnet-4-6","max_turns":5,"permission_mode":"bypassPermissions"}'

# Different model with fewer turns
uv run python main.py "Summarize this article" '{"model":"claude-sonnet-4-6","max_turns":2}'
```

### Available Options

Options are passed as a JSON string as the second argument. Supported keys correspond to `ClaudeAgentOptions` kwargs:

| Option             | Description                          |
| ------------------ | ------------------------------------ |
| `model`            | Claude model to use (e.g. `claude-sonnet-4-6`, `claude-opus-4-7`) |
| `max_turns`        | Maximum agent turns                  |
| `permission_mode`  | Permission mode (e.g. `bypassPermissions`, `acceptEdits`) |
| `allowed_tools`    | List of tools the agent is allowed to use |
| `resume`           | Session ID to resume a previous conversation |
| `hooks`            | Callback functions for agent lifecycle events |
| `mcp_servers`      | MCP server configurations for external tool integration |
| `agents`           | Subagent definitions for delegating focused subtasks |
| `setting_sources`  | Restrict which `.claude/` config sources load |

### Output

The runner prints each streamed message with a timestamp. On completion, it displays session context including session ID, turn count, duration, cost, and the full conversation history.

## Claude Agent SDK

This project uses the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), which provides the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript.

### Built-in Tools

The SDK includes tools for reading files, running commands, and searching codebases out of the box:

| Tool               | What it does                                         |
| ------------------ | ---------------------------------------------------- |
| **Read**           | Read any file in the working directory               |
| **Write**          | Create new files                                     |
| **Edit**           | Make precise edits to existing files                 |
| **Bash**           | Run terminal commands, scripts, git operations       |
| **Monitor**        | Watch a background script and react to output events |
| **Glob**           | Find files by pattern (`**/*.ts`, `src/**/*.py`)     |
| **Grep**           | Search file contents with regex                       |
| **WebSearch**      | Search the web for current information               |
| **WebFetch**       | Fetch and parse web page content                     |
| **AskUserQuestion**| Ask clarifying questions with multiple choice options|

### Key Capabilities

- **Hooks** — Run custom code at key agent lifecycle points (`PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`) to validate, log, block, or transform agent behavior. See [Hooks docs](https://code.claude.com/docs/en/agent-sdk/hooks).
- **Subagents** — Spawn specialized agents for focused subtasks. Define agents with custom instructions and restricted tool sets. See [Subagents docs](https://code.claude.com/docs/en/agent-sdk/subagents).
- **MCP** — Connect to external systems via the Model Context Protocol (databases, browsers, APIs, and [hundreds more](https://github.com/modelcontextprotocol/servers)). See [MCP docs](https://code.claude.com/docs/en/agent-sdk/mcp).
- **Permissions** — Control which tools the agent can use. Allow safe operations, block dangerous ones, or require approval. See [Permissions docs](https://code.claude.com/docs/en/agent-sdk/permissions).
- **Sessions** — Maintain context across multiple exchanges. Resume or fork sessions to explore different approaches. See [Sessions docs](https://code.claude.com/docs/en/agent-sdk/sessions).

### Claude Code Features

The SDK also supports Claude Code's filesystem-based configuration (`.claude/` directory):

| Feature          | Description                                   | Location               |
| ---------------- | --------------------------------------------- | ---------------------- |
| Skills           | Specialized capabilities defined in Markdown  | `.claude/skills/*/SKILL.md` |
| Slash commands   | Custom commands for common tasks              | `.claude/commands/*.md`    |
| Memory           | Project context and instructions              | `CLAUDE.md`                |
| Plugins          | Extend with custom commands, agents, MCP      | Programmatic via `plugins` |

### SDK vs Client SDK

The [Anthropic Client SDK](https://platform.claude.com/docs/en/api/client-sdks) provides direct API access where you implement tool execution yourself. The **Agent SDK** handles the tool loop autonomously — Claude decides which tools to call and executes them without manual orchestration.

### Documentation & Resources

- [Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Quickstart Guide](https://code.claude.com/docs/en/agent-sdk/quickstart)
- [Python SDK Reference](https://code.claude.com/docs/en/agent-sdk/python)
- [TypeScript SDK Reference](https://code.claude.com/docs/en/agent-sdk/typescript)
- [Example Agents](https://github.com/anthropics/claude-agent-sdk-demos)
- [Python SDK Changelog](https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md)
- [Python SDK Issues](https://github.com/anthropics/claude-agent-sdk-python/issues)