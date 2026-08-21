# Fast pattern index

All JSON patterns are Bricks 2.3.10 clipboard artifacts and must pass `scripts/validate_bricks_json.py`.

Use the closest pattern, replace content/assets/variables, keep the verified wrapper/tree, then validate again.

| Pattern | Best for |
|---|---|
| `hero-split.json` | two-column hero with CTA and image |
| `feature-grid.json` | services/features/reasons cards |
| `pricing-grid.json` | service packages/pricing cards |
| `testimonials.json` | reviews/testimonials cards |
| `contact-cta.json` | contact/booking CTA |
| `header-basic.json` | header structure pasted into a header template |
| `footer-basic.json` | footer structure pasted into a footer template |

Patterns intentionally use a small shared class vocabulary and foundation variables. Element-specific exceptions can be changed through native Bricks controls.

When composing a full page, adapt patterns individually and combine clipboard files with:

```text
scripts/compose_clipboard.py -o homepage.json hero.json features.json pricing.json
```

The composer remaps colliding element/class IDs, merges classes by name, and preserves one valid clipboard wrapper.
