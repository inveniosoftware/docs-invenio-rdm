# Quick how-to: invenio-i18n CLI

This is the short, end-to-end path for the new `invenio-i18n` service. It keeps the order clear and shows where files land so overrides don’t get lost.

## Where things live and who wins
- Instance overrides are the highest priority and survive upgrades  
  - JS: `./translations/<locale>.json`  
  - Python: `./translations/<locale>/LC_MESSAGES/messages.po`
- Bundle translations: translation bundles middle layer
- Package translations: installed packages base layer
- Merge priority: instance > bundle > package

## Core workflow (collect → validate → distribute)
- Validate PO quality:
  - `invenio i18n validate-translations --all-packages -l de`
- Build JS translations collect+merge+distribute:
  - `invenio i18n js-translation build -p invenio-app-rdm -p invenio-communities`
  - Writes merged JSON to `./js-translations/`, then distributes into each package’s assets.
- Distribute custom JS if you edited copies elsewhere:
  - `invenio i18n js-translation distribute -i ./my-custom-js`

## Quick edits
- Update one Python translation:
  - `invenio i18n update-translation -p invenio-app-rdm -l de --msgid "Save" --msgstr "Speichern"`
- Update one JS translation:
  - `invenio i18n js-translation update -p invenio-communities -l de --msgid "Communities" --msgstr "Gemeinschaften"`

## Testing/validation JSON (not runtime)
- Build JSON for assertions:
  - `invenio i18n build-translations -p invenio-app-rdm -l de --path-to-global-pot ./python-translations.json`

## Checks and visibility
- JS source tracking: `./js-translations/<locale>.json` includes `_translation_sources` so you see which layer (package/bundle/instance) won; keys starting with `_` are skipped when distributing.
- Verify merged JS after build:
  - `cat js-translations/de.json | jq '.invenio_communities["Communities"]'`
- Verify instance PO override:
  - `msgcat translations/de/LC_MESSAGES/messages.po | grep -A1 "Save"`

## Why it’s upgrade-safe
- You never edit files in `site-packages`; keep overrides in `./translations/`. Upgrades replace package files, but your instance overrides stay and are merged last when you rebuild.

