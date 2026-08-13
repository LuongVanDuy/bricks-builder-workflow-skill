# Workflow B — Brand-led Greenfield

Use when there is **no reference website to clone** or the user explicitly wants an original website based on brand/business information.

## Goal

Turn limited business inputs (even only logo + industry + contact details) into a coherent Bricks-native website without making the user choose implementation details the agent can design itself.

## Fast intake rule

Normalize what is known into the fields in `references/intake-schema.md`.

Ask a question only when the missing fact can materially change positioning, information architecture, conversion flow, or legal/business correctness.

Usually **infer/design without asking**:
- exact color shades beyond the logo;
- font pairing;
- spacing scale;
- container widths;
- border radius;
- shadows;
- card style;
- section spacing;
- breakpoint details;
- ordinary component layout.

Usually **ask if truly unknown and consequential**:
- what the company actually sells/does;
- primary audience when B2B vs B2C changes the site significantly;
- primary conversion action when several are plausible;
- service area/market when it changes content or navigation;
- mandatory pages/content/compliance constraints.

Batch blockers in one compact question set. Do not ask one question at a time unless the answer creates a new blocker.

## Workflow

### 1. Brand signal extraction

From logo and supplied brand assets, derive signals rather than blindly copying colors:
- dominant/accent color candidates;
- visual geometry: sharp/technical, soft/friendly, premium/editorial, playful, etc.;
- likely typography direction;
- contrast and surface strategy;
- image/art direction.

A logo is a visual signal, not complete positioning. Do not infer premium/mass-market, B2B/B2C, or brand personality solely from logo appearance when business data says otherwise.

### 2. Business model and audience

Summarize in a compact internal brief:

```text
Offer → Audience → Problem/need → Proof → Primary CTA
```

If information is sparse, use the most conservative reasonable interpretation and label it as an assumption.

### 3. Industry pattern research

When current research is available and materially useful, inspect a **small representative set** of current industry websites/sources to learn common UX expectations. This is pattern research, not cloning.

Research only what helps decisions such as:
- expected navigation/content architecture;
- conversion patterns;
- trust/proof modules;
- product/service presentation;
- booking/quote/contact flows;
- industry-specific content conventions.

Keep research bounded for speed. Prefer roughly 3–5 representative sources when enough; do not browse endlessly.

Do not copy a competitor's brand system or page composition wholesale.

### 4. Information architecture

Choose the smallest useful page set and navigation structure from the business model.

Typical possibilities:
- Home
- About
- Products / Services
- Category / Detail templates
- Projects / Portfolio / Case studies
- News / Knowledge
- Contact

Only include pages/modules that serve the actual business.

### 5. Design direction

Before building, establish a short design direction:

```text
Brand character:
Audience:
Visual direction:
Primary color role:
Typography direction:
Layout density:
Image direction:
Primary CTA:
```

Then derive the Bricks foundation:

```text
01 Variables
02 Color Palette
03 Theme Style
04 Layout Framework
```

Do not use arbitrary starter values when logo/business/research provides a better basis.

### 6. Build order

```text
Foundation
→ Header
→ Footer
→ Home
→ Reusable cards/components
→ Archive/templates
→ Inner pages
→ Responsive/QA
```

Use native Bricks structure and dynamic WordPress/WooCommerce data where appropriate.

### 7. Component rule

Before creating component CSS, classify every style:

```text
Reusable value          → Variables / Color Palette
Global default           → Theme Style
Common layout/spacing    → Layout Framework
Component-specific style → Component Class
Structure/dynamic data   → Native Bricks element
```

Keep component CSS small.

### 8. QA

Check:
- brand coherence without overusing logo colors;
- readable contrast and hierarchy;
- clear primary CTA;
- sensible mobile order;
- no unnecessary pages/components;
- native Bricks behavior retained;
- generic framework naming retained;
- assumptions are visible where they materially affect strategy.

## Default behavior with very little data

If the user gives only:

```text
logo + company/brand name + industry + contact information
```

then:
1. inspect the logo;
2. infer a preliminary visual direction;
3. identify only the missing strategic blockers;
4. ask one compact batch if necessary;
5. otherwise proceed into IA + design system immediately.

Do not stop merely because there is no reference website.
