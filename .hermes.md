# pdf_translator — project rules

Agent-assisted PDF translation pipeline. Universal tool:
`scripts/pdf_translation_service.py` (extract → translate manifest →
build / build-inplace-flow → validate). Per-manual scripts in
`scripts/` are historical one-offs; do not extend them — generalize
into the service instead.

## Git
- Remote: https://github.com/Starzrng/pdf-translator.git (private, main)
- Commit after each finished change, explicit paths, push to main.
- NEVER commit: `input/*.pdf`, `output/`, `tmp/`, `.venv/`,
  `__pycache__/`. They are gitignored on purpose (~400 MB binaries).
- ALWAYS commit: `scripts/`, `translations/*.json` (the product data),
  README, pyproject.

## Verification before committing code changes
- `python3 -m venv .venv` exists; use `.venv/bin/python`.
- Smoke: run the CLI help (`pdf_translation_service.py --help`) and,
  for touched paths, one extract/build round-trip on a small PDF.
- Render-check any rebuilt PDF before claiming success.

## Conventions
- Fonts: do not hardcode macOS font paths; resolve from env/config.
- Translation manifests stay valid JSON; keep keys stable
  (`translation_title`, `translation_body`).
