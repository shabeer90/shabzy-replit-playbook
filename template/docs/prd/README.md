# PRDs

Every Feature and Bet starts here (the `lane` skill decides which). A Fix doesn't need one.

- The `cpo` agent, or the CEO, writes the PRD from `_template.md` as `<yyyy-mm-dd>-<name>.md`. A Feature fills the top half; a Bet fills it all.
- A Bet's PRD is reviewed by the `reviewer` agent in PRD mode before the owner sees it.
- The owner approves it last, by setting `Status: approved`.
- Only approved PRDs listed under **Now** in `docs/ROADMAP.md` get built.
- The PR links its PRD with a `PRD:` line. CI (`scripts/check_lane.py`) checks the link and the status, and that a Bet has an Undo.
