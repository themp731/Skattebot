# Codex workflow

For every substantial feature change or Codex work order in this repository:

1. Start from a new Git worktree and a new branch. Do not perform the work in an existing shared checkout.
2. Name the branch with the source issue reference, using the form `codex/<issue-id>-<short-description>` (for example, `codex/123-add-tax-summary`). If no issue reference is provided, ask for one before creating the branch.
3. Keep the change scoped to that work order and preserve unrelated working-tree changes.
4. When the work is complete and verified, commit the changes with a clear message and push the branch to `origin`.

Small changes may be committed and merged directly on `main`: documentation updates, skill or instruction changes, and typo fixes. Small read-only inspections and purely conversational requests also do not require a worktree or branch.
