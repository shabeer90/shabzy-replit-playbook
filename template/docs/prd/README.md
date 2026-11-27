# PRDs

Every piece of work bigger than a small fix starts here. No PRD, no build.

- The `cpo` agent writes the PRD from `_template.md` as `<yyyy-mm-dd>-<name>.md`.
- The leadership agents whose area it touches review it, in its **Review** section.
- The owner approves it last, by setting `Status: approved`.
- Only approved PRDs listed under **Now** in `docs/ROADMAP.md` get built.
- The PR links its PRD. The guard hook checks the link (see `.claude/hooks/README.md`).
