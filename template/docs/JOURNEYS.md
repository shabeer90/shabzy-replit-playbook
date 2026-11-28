# User journeys

The end-to-end paths that must always work. Each one has an e2e test, CI runs all of them on every PR, and QA runs them on every Feature or Bet that touches the app. A PR that breaks one doesn't ship, even if its own feature works.

| Journey | Steps (start to done) | Test | Added by |
|---|---|---|---|
| <name, e.g. "Find and compare two products"> | <land → search → open → compare → click out> | `e2e/journeys/<name>.spec.ts` | <PRD link> |
