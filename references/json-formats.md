# Bricks JSON formats

Choose the handoff by where the user will put it.

| Goal | Format | Handoff |
|---|---|---|
| Section / page content | Clipboard | paste in Builder |
| Header / footer / reusable template | Template import | Bricks Templates import |
| Bulk or automated site write | Postmeta | code/WP-CLI only when requested |

## Clipboard 2.3.10

```json
{
  "content": [],
  "source": "bricksCopiedElements",
  "sourceUrl": "https://reference.example",
  "version": "2.3.10",
  "globalClasses": [],
  "globalElements": [],
  "components": []
}
```

Only dependency arrays that are needed must be present.

Element node:

```json
{
  "id": "abc123",
  "name": "container",
  "parent": "sec001",
  "children": ["txt001"],
  "settings": {},
  "label": "Optional label"
}
```

Root `parent` is `0`. Keep `settings` an object.

## Template 2.3.10

A minimal hand-authored wrapper follows the source-verified import/export contract:

```json
{
  "title": "Header Main",
  "templateType": "header",
  "header": [],
  "global_classes": [],
  "globalVariables": [],
  "globalVariablesCategories": []
}
```

For footer use `footer`; for normal content/template types use `content`. Add `pageSettings` or `templateSettings` only when needed.

## Dependency merge

Clipboard uses `globalClasses`; template import uses `global_classes`.

Each class object:

```json
{"id":"crd001","name":"card","settings":{}}
```

If element settings reference `_cssGlobalClasses`, every referenced ID must exist in the artifact.

## Validation

Run:

```text
scripts/validate_bricks_json.py <file.json>
```

It checks parse, wrapper, six-character IDs, duplicate IDs, parent/children reciprocity, settings objects, and Global Class references.
