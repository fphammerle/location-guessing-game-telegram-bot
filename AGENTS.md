# Agent Instructions

## Commit messages

- Attribution line: `Co-Authored-By: Claude <model name> <noreply@anthropic.com>` — always include the model name,
  e.g. `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- Do **not** include a `Claude-Session:` line — the session URL is private.

## CHANGELOG

- Only document **user-facing** changes (features, bug fixes, removed support).
- Test tooling changes (e.g. `Pipfile`, `Pipfile.lock`) are not user-facing → no entry needed.
- Wording for Python version support: `declare compatibility with \`python3.X\``

## Pull requests

- Rebase on `master` before opening a PR.
- One commit per PR; amend rather than adding new commits.
- Force-push with `--force-with-lease` on feature branches.
- **Never force-push to `master`.**
- **Always open a pull request — never push directly to `master`.**

## CI failures

- Fix CI failures automatically, iterating until all checks are green — no need to ask first.

## Working tree hygiene

- After running local tools (pytest, mypy, pylint, …), check `git status` for untracked
  generated artefacts (e.g. `.coverage`).
- Add them to `.gitignore` — do **not** commit them.

## Pipfile / dependency management

- Generate `Pipfile.lock` on the **lowest** supported Python version.
- When a package is a conditional transitive dependency (e.g. `dill`, `typing_extensions`)
  whose pip markers depend on the lock-generation Python version, add it **explicitly** as a
  direct dependency in `Pipfile` (without a version marker) so it installs on all supported
  Python versions.
- When constrained packages (e.g. `setuptools`, `urllib3`) need to override transitive
  resolution, put them in `[packages]`, not `[dev-packages]`.
