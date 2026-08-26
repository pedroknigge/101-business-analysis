# Skill discovery & upgrade

How agents detect that Business Analysis 101 is installed and current. **No silent auto-patch.**

## Detect install

| Signal | Meaning |
|--------|---------|
| Skill path exists | `~/.agents/skills/101-business-analysis/SKILL.md`, `~/.claude/skills/…`, `~/.grok/skills/…`, or a clone |
| Host skill list | `npx skills list` / agent UI shows `101-business-analysis` |
| Version | `VERSION` (one line) or YAML `metadata.version` in `SKILL.md` |

Announce when relevant:

```text
Business Analysis 101: installed | version: <x.y.z> | path: <skill dir>
```

`<this-skill>` is that directory (the folder that contains this `SKILL.md`). Never assume Claude-only.

## Detect outdated

1. Read local version from `VERSION` or `SKILL.md` frontmatter.
2. Compare to published **0.1.0** on GitHub `pedroknigge/101-business-analysis`.
3. If local **<** published: suggest update — do **not** overwrite without user OK.

```bash
npx skills update 101-business-analysis -g -y
```
