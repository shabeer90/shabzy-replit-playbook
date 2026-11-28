# <Name>

Lane: feature | bet
Status: draft | approved | shipped | dropped
Owner approval: <date, once approved>
Appetite: <how much time this is worth, in days. Past it, stop and ask the owner.>

## Problem
Who has it, when, and what they do today. In the user's words.

## The user journey
Step by step, from where the user starts to where they're done. Add it, or the change to it, to `docs/JOURNEYS.md`.

## How we'll know
One line: the number or observable that tells us it worked, and where to look.

## Acceptance criteria
1. <checkable by a tester, including edge cases, errors and phone width>

## Out of scope
What we're deliberately not doing, so nobody builds it by accident.

<!-- A Feature stops here. A Bet fills in everything below. -->

## Door
Which of the one-way criteria in the `lane` skill this trips, and why.

## Undo
<!-- How to switch it off, how long that takes, and what stays behind. Say plainly what can't be undone (sent emails, charged cards, overwritten rows) and what limits the damage instead. CI fails a Bet whose Undo is empty. -->

## How we'd notice
What tells us within the hour if it breaks, and who sees it.

## Review
One line per lens the Bet trips, from the reviewer in PRD mode (`review` skill).
- <lens>: approve | changes needed: <notes>
