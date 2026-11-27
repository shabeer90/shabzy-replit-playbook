# Starter prompt

Paste this as the first message to the agent in a new project. Replace the bits in `<angle brackets>`.

---

We're starting a new project: **<one line: what it is and who it's for>**.

Set it up from my playbook at https://github.com/shabeer90/shabzy-replit-playbook before writing any feature code:

1. Read `PLAYBOOK.md` and `SKILLS.md` in that repo.
2. Copy everything in `template/` into this repo. Fill in every `<placeholder>` in `AGENTS.md`, and ask me for anything you can't work out.
3. Install the skills listed under "Every project" and "Review and QA" in `SKILLS.md`, plus any under "When the project needs it" that fit. Record each one in `skills-lock.json`.
4. Make the hooks in `.claude/hooks/` executable and check they block what they should (the test commands are in `template/.claude/hooks/README.md`).
5. Have the **head-of-design** agent create the design system first: tokens in `design/tokens`, the Tailwind theme from those tokens, and the base components in `components/ui/`. Nothing else gets built until it exists.
6. Work through the Day 0 checklist in `PLAYBOOK.md` section 2. Tell me which items only I can do, such as GitHub settings, secrets, the domain and Search Console.
7. Open one pull request with the setup. Before you open it, the **em-reviewer**, **qa-tester** and **cto-reviewer** agents each review it and sign off in `.reviews/<branch>.md` (the hook won't let the PR open otherwise).

From then on, every feature follows the flow in `PLAYBOOK.md` section 9: spec, design system, build test-first, three reviews, then the PR.

Rules from the start: the smallest complete change (ponytail), every change through a PR, no secrets in any tracked file, and SEO wins trade-offs.
