# dsh-skill-vault

> A DSH skill vault: manages distilled skills by scenario and individual skill toggles, with agent tools and a web panel.

[中文](README.md) | **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Introduction

dsh-skill-vault is a skill-vault plugin in the DSH (DeepSeek Harness) ecosystem. It organizes distilled skills by usage scenario and provides scenario-level and per-skill toggles. Enabled state is stored in a local data directory and never enters the public repository.

This repository also contains the plugin source and open-source skills/corpus. Its remote repository is [skill-group](https://github.com/dargonburn337845818/skill-group).

## Features

- **Central storage**: put distilled skills in `vault/`, organized by scenario, to avoid a cluttered directory.
- **On-demand enablement**: scenario-level toggles plus per-skill toggles; disabled by default to save context.
- **Agent tools**: query, enable, disable, and add skills.
- **Web panel**: a visual toggle panel that can work with the process monitor.
- **Automated push**: new skills are prepared by `skill_vault_add`; push is interactive by default, or fully automated with `scripts/push.sh --yes` once credentials are configured.

## Agent Tools

| Tool | Purpose |
|---|---|
| `skill_vault_list` | Query skills by scenario/expert/source/enablement status |
| `skill_vault_enable <target> [scope=global\|session]` | Enable a skill or an entire scenario |
| `skill_vault_disable <target> [scope=global\|session]` | Disable a skill or an entire scenario |
| `skill_vault_add` | Copy a distilled directory containing SKILL.md into the vault and generate a manifest (does not commit) |

## Enablement Semantics

- Default: all skills are disabled and only appear in the plugin directory.
- After enablement: the plugin calls `ctx.skills.register()`, and the skill enters the DSH global skill catalog.
- `scope=global` writes `~/.dsh/skill-vault/enabled.json` and persists across restarts.
- `scope=session` affects only the current process; restart restores global state.

## Repository Layout

```text
src/                 # plugin TypeScript source
vault/               # open-source skill repository
├── skills/          # skill packages organized by scenario
├── corpus/          # open-source corpus/artifacts
└── manifest.schema.json
scripts/             # build, validation, push (interactive by default)
tests/               # plugin and vault validation tests
lib/                 # prebuilt artifacts (committed)
```

## Development and Build

```bash
bash scripts/build.sh
npm run build:client
npm test
```

Follow `dsh-optimization-consensus`:

- never hot-install into a running agent;
- verify with config export and a smoke test in an isolated `DSH_HOME` first;
- rollback restores actual files, not just package.json pins;
- the plugin does not push automatically; automation requires `--yes`/`PUSH_CONFIRM=yes` and validation/review before pushing.

## Quick Start and Release

- [QUICKSTART.md](QUICKSTART.md): install, load, enable skills, release a new version.
- [DESIGN.md](DESIGN.md): module design notes.
- After pushing a `v*` tag, `.github/workflows/release-plugin.yml` validates the vault, packages it, and creates a GitHub Release.

## Pushing

Interactive mode by default:

```bash
bash scripts/push.sh
```

The script asks for confirmation and runs `git add -A && git commit && git push`; credentials come from git credential helpers or configured authentication. The script never asks the model to hold or paste a password.

Fully automated mode (CI or configured credentials):

```bash
bash scripts/push.sh --yes --message "vault: update distilled skills"
# or
PUSH_CONFIRM=yes PUSH_MESSAGE="vault: update distilled skills" bash scripts/push.sh
```

Automated mode keeps safety guards: internal artifacts (`assignments/`, `evals/`) are blocked, and personal state such as `enabled.json` never enters the public repository.

## Contributing and Security

- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Vulnerability reporting: [SECURITY.md](SECURITY.md)
- Community guidelines: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- The public repository does not publish internal development artifacts: `assignments/` and top-level `evals/` are excluded by `.gitignore`.

## License

[MIT](LICENSE)
