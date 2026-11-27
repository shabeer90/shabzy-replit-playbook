#!/usr/bin/env bash
# A test that passes before the fix is not evidence.
#
# Takes the tests a branch adds or changes, runs them against the BASE commit's source, and
# requires them to fail there. Written after shipping two fixes whose "it works" rested on a
# mechanism rather than on anything observed changing.
#
#   scripts/assert_new_tests_fail_on_base.sh <base-ref>
#
# Covers Playwright specs (whole files) and pytest tests (the individual functions the diff
# ADDS). Pytest is checked per function on purpose: changing a shared fixture makes the old
# tests fail on base too, and counting those as red would wave anything through.
#
# Exit 0: every new test failed on base, so it is measuring the change.
# Exit 1: one passed on base (proves nothing), or never ran (proves nothing either).
set -uo pipefail

BASE="${1:?usage: $0 <base-ref>}"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

mapfile -t SPECS < <(git diff --name-only --diff-filter=AM "$BASE"...HEAD -- 'e2e/*.spec.ts' | sort -u)
mapfile -t PYFILES < <(git diff --name-only --diff-filter=AM "$BASE"...HEAD -- 'scripts/test_*.py' | sort -u)

# A change that only rewrites comments in a test pins no behaviour, so there is nothing here to
# measure in either direction. Asked the normal question it passes on base, because the test it
# describes passed there too; asked the test-only question it passes again, because the test was
# never broken. Both refusals are true and useless, and what they cost is this: a comment that has
# gone stale — a fix landed, the comment still tells the next reader the bug is open — is cheaper
# to leave wrong than to correct. A gate that makes the documentation around the tests rot is
# doing harm.
#
# What counts as a comment depends on the language, and guessing cost nothing to check:
#   .ts  — //, /*, */ and a leading * (a JSDoc continuation). A leading * is also a multiplication
#          carried onto the next line, but prettier puts an operator at the end of a line, and no
#          line in e2e/ begins with one.
#   .py  — # only. NOT a leading *, because in Python that is an unpacking and real code:
#          a call split over lines can start a line with `*args`. Docstrings are not
#          prose either: a line inside one can look like anything.
# Anything else is never prose, so a path this script grows later is examined until someone says
# otherwise here.
#
# One changed line that is not prose and the whole file is examined as usual, so the exemption
# cannot be reached by burying a change among comments.
prose_only() {
  local pattern body
  case "$1" in
    *.ts|*.tsx) pattern='^(//|/\*|\*/|\*|$)' ;;
    *.py)       pattern='^(#|$)' ;;
    *)          return 1 ;;
  esac
  body="$(git diff -U0 "$BASE"...HEAD -- "$1" \
            | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' | sed -E 's/^[+-][[:space:]]*//')"
  [ -n "$body" ] || return 1
  ! printf '%s\n' "$body" | grep -qvE "$pattern"
}

drop_prose() { local f; for f in "$@"; do [ -n "$f" ] && { prose_only "$f" || echo "$f"; }; done; }
list_prose() { local f; for f in "$@"; do [ -n "$f" ] && { prose_only "$f" && echo "$f"; }; done; }

# Printed, never silent. A gate that skips things quietly is a gate that stops meaning anything.
mapfile -t PROSE_TESTS < <(list_prose "${SPECS[@]:-}" "${PYFILES[@]:-}")
mapfile -t SPECS < <(drop_prose "${SPECS[@]:-}")
mapfile -t PYFILES < <(drop_prose "${PYFILES[@]:-}")
if [ ${#PROSE_TESTS[@]} -gt 0 ]; then
  echo "Comments only, so there is nothing to measure either way. Not examined:"
  printf '  %s\n' "${PROSE_TESTS[@]}"
fi

# The pytest functions this branch adds, as file::name.
PYTESTS=()
for file in "${PYFILES[@]:-}"; do
  [ -n "$file" ] || continue
  while read -r name; do
    [ -n "$name" ] && PYTESTS+=("$file::$name")
  done < <(git diff -U0 "$BASE"...HEAD -- "$file" | sed -n 's/^+def \(test_[A-Za-z0-9_]*\).*/\1/p')
done

if [ ${#SPECS[@]} -eq 0 ] && [ ${#PYTESTS[@]} -eq 0 ]; then
  echo "No tests added or changed against $BASE."
  echo "A change that fixes behaviour should bring a test that fails without it."
  exit 0
fi

# A change that touches only tests cannot be evidenced the usual way, and asking it to be is a
# contradiction: the gate runs the branch's tests against the base SOURCE, so with no source
# change they necessarily pass there. Three specs were failing on main because the tests were
# wrong — a hard-coded slug absent from the mock, a grep matching the comment that explained
# why the thing it forbade was absent, and a hydration race — and the fix for each was in the
# test. The gate refused it with "the fix is not needed", which was true and useless.
#
# So for a test-only change the question is a different one, and still a real one: were these
# tests actually failing before? Run the BASE's own copy of each MODIFIED test file and require
# it to fail. A test that was already passing is a working test being changed, and no machine
# can judge whether that is a correction or a quiet weakening — so that still gets refused.
# Newly added files are not checked here: with no source change they evidence nothing either
# way, and a new passing test is not what this gate exists to catch.
TEST_ONLY=1
while read -r file; do
  [ -n "$file" ] || continue
  case "$file" in
    e2e/*.spec.ts|scripts/test_*.py) ;;
    # Prose is not behaviour, so a test may travel with the document it pins. This assumes the
    # project never renders or imports markdown (no MDX, no content loader, no runtime read of a
    # .md). If yours does, remove *.md from this exemption. Counting it as a source change
    # only forced the two apart: the test pinning the soft-404 decision went in one pull request
    # and the sentence it enforces would have had to go in another, because a characterisation
    # test necessarily passes on base. Documentation drifting away from the test that holds it
    # is the thing this gate exists to prevent, not something it should be causing.
    *.md) ;;
    *) TEST_ONLY=0 ;;
  esac
done < <(git diff --name-only "$BASE"...HEAD)

if [ "$TEST_ONLY" = 1 ]; then
  mapfile -t SPECS < <(drop_prose $(git diff --name-only --diff-filter=M "$BASE"...HEAD -- 'e2e/*.spec.ts' | sort -u))
  mapfile -t PYTESTS < <(drop_prose $(git diff --name-only --diff-filter=M "$BASE"...HEAD -- 'scripts/test_*.py' | sort -u))
  PYFILES=()
  if [ ${#SPECS[@]} -eq 0 ] && [ ${#PYTESTS[@]} -eq 0 ]; then
    echo "Only tests changed, and none of them was modified. Nothing to show either way."
    exit 0
  fi
  echo "Only tests changed against $BASE, so nothing new is being evidenced."
  echo "Checking instead that these were FAILING on $BASE, which is what makes fixing them honest:"
  printf '  %s\n' "${SPECS[@]:-}" "${PYTESTS[@]:-}" | grep -v '^  $' || true
else
  echo "Checking that these fail on $BASE (${#SPECS[@]} specs, ${#PYTESTS[@]} pytest tests):"
  printf '  %s\n' "${SPECS[@]:-}" "${PYTESTS[@]:-}" | grep -v '^  $' || true
fi

WORKTREE="$(mktemp -d)/base"
BASE_COPIES="$(mktemp -d)"
git worktree add --detach --quiet "$WORKTREE" "$BASE" || { echo "could not create a worktree at $BASE"; exit 1; }
cleanup() { git worktree remove --force "$WORKTREE" >/dev/null 2>&1 || true; git worktree prune >/dev/null 2>&1 || true; rm -rf "$BASE_COPIES"; }
trap cleanup EXIT

base_copy() { echo "$BASE_COPIES/$(echo "$1" | tr / _)"; }

# The base source, this branch's tests, and the dependencies already installed here.
ln -s "$ROOT/node_modules" "$WORKTREE/node_modules"
[ -f "$ROOT/.env.local" ] && cp "$ROOT/.env.local" "$WORKTREE/.env.local"
if [ "$TEST_ONLY" = 1 ]; then
  echo "  (running the base's own copy of each file, not this branch's)"
else
  for file in "${SPECS[@]:-}" "${PYFILES[@]:-}"; do
    [ -n "$file" ] || continue
    mkdir -p "$WORKTREE/$(dirname "$file")"
    # Kept because a test that already existed can be asked the OTHER question later: not
    # "does the branch's version fail here" but "was the version that was here reliable".
    # Only a modified file has one; an added file does not exist on base at all.
    [ -f "$WORKTREE/$file" ] && cp "$WORKTREE/$file" "$(base_copy "$file")"
    git show "HEAD:$file" > "$WORKTREE/$file"
  done
fi

passed=()
unrunnable=()
flaky=()

# How many times to ask before believing a test on BASE is reliable. Once is not an answer.
# A spec once failed on main in one CI run and passed on a re-run of
# that same commit, with no code in between; this gate ran base's copy once, saw the second
# kind of run, and refused the fix because "they were not broken". A test that passes four
# times in five WAS broken on base — intermittently, which is the hardest kind to fix and the
# kind every fix for was being turned away.
#
# Only ever applied to BASE's OWN copy of a test that already existed. A new test that passes
# on base evidences nothing however many times it is run, and repeating it would let a lucky
# red through. Specs only: flakiness here is browser timing, and the pytest tests in this
# repository do not touch a browser.
BASE_ATTEMPTS="${BASE_ATTEMPTS:-5}"

# One invocation, --repeat-each attempts. A loop of separate invocations would be the obvious
# way to write this and costs five dev-server starts instead of one: in this worktree Playwright
# brings up `pnpm run dev` every time, which is almost all of the ~23 seconds a run takes.
# With attempts of 1 this is exactly what the gate did before.
spec_on_base() {
  local spec="$1" attempts="$2"
  (cd "$WORKTREE" && ./node_modules/.bin/playwright test "$spec" \
     --repeat-each="$attempts" --reporter=line 2>&1)
}

# True when the copy that was on BASE fails within BASE_ATTEMPTS runs. Restores the branch's
# copy afterwards so nothing later in the run sees the wrong file.
was_unreliable_on_base() {
  local spec="$1" saved output
  saved="$(base_copy "$spec")"
  [ -f "$saved" ] || return 1
  cp "$saved" "$WORKTREE/$spec"
  output="$(spec_on_base "$spec" "$BASE_ATTEMPTS")"
  git show "HEAD:$spec" > "$WORKTREE/$spec"
  echo "$output" | grep -qE '[0-9]+ failed'
}

# A non-zero exit is not enough on its own. A web server that never started, or a file that
# would not compile, also exits non-zero — and reading that as "red" is exactly how a test
# that proves nothing gets waved through. Only a run that reported results counts.
classify() {
  local label="$1" output="$2" failed_re="$3" passed_re="$4"
  if echo "$output" | grep -qE "$failed_re"; then
    echo "  fails on base:  $label"
  elif echo "$output" | grep -qE "$passed_re"; then
    passed+=("$label")
    echo "  PASSES on base: $label"
  else
    unrunnable+=("$label")
    echo "  could not run:  $label"
    echo "$output" | tail -3 | sed 's/^/        /'
  fi
}

for spec in "${SPECS[@]:-}"; do
  [ -n "$spec" ] || continue
  if [ "$TEST_ONLY" = 1 ]; then
    # Base's own copy is already in place here, so asking repeatedly is asking the right thing.
    output="$(spec_on_base "$spec" "$BASE_ATTEMPTS")"
  else
    output="$(spec_on_base "$spec" 1)"
    # The branch's copy passed on base. For a NEW test that settles it: it shows nothing. For a
    # test that already existed it may instead mean the one that was there was unreliable, so
    # ask the question the test-only path asks before giving a verdict.
    if echo "$output" | grep -qE '[0-9]+ passed' && was_unreliable_on_base "$spec"; then
      flaky+=("$spec")
      echo "  flaky on base:  $spec"
      continue
    fi
  fi
  classify "$spec" "$output" '[0-9]+ failed' '[0-9]+ passed'
done

for test in "${PYTESTS[@]:-}"; do
  [ -n "$test" ] || continue
  output="$(cd "$WORKTREE" && python3 -m pytest "$test" -q --no-header 2>&1)"
  # "1 error" counts as red here: on base the function under test often does not exist yet,
  # and pytest reports a collection error rather than a failure.
  classify "$test" "$output" '[0-9]+ (failed|error)' '[0-9]+ passed'
done

if [ ${#unrunnable[@]} -gt 0 ]; then
  echo
  echo "These never produced a result against $BASE, so nothing was shown either way:"
  printf '  %s\n' "${unrunnable[@]}"
  echo "Fix the run before trusting this gate: a test that cannot run is not a failing test."
  exit 1
fi

if [ ${#flaky[@]} -gt 0 ]; then
  echo
  echo "These passed on $BASE with this branch's copy, but the copy that was ON $BASE failed"
  echo "within $BASE_ATTEMPTS runs, so they were broken there — intermittently:"
  printf '  %s\n' "${flaky[@]}"
  echo "A test that only sometimes passes is still a broken test, and the fix for one is real work."
fi

if [ ${#passed[@]} -gt 0 ]; then
  echo
  if [ "$TEST_ONLY" = 1 ]; then
    echo "These were already passing on $BASE, so they were not broken:"
    printf '  %s\n' "${passed[@]}"
    echo "Changing a working test may be a correction or a quiet weakening, and nothing here can"
    echo "tell which. Say in the pull request why, and have a human confirm it."
  else
    echo "These passed against $BASE, so they do not show the change does anything:"
    printf '  %s\n' "${passed[@]}"
    echo "Either the test is not measuring the fix, or the fix is not needed."
  fi
  exit 1
fi

echo
if [ "$TEST_ONLY" = 1 ]; then
  echo "Every changed test was failing on base. Fixing them is doing real work."
else
  echo "Every new test failed on base. The change is doing the work."
fi
