# Project Intake Schema

Use this only to normalize project inputs and decide whether questions are actually necessary.

## Machine-readable brief

```text
project_mode: reference | greenfield | hybrid
brand_name:
logo_assets:
reference_urls:
industry:
business_model:
primary_offer:
audience:
market_or_service_area:
primary_cta:
secondary_cta:
required_pages:
products_or_services:
contact:
content_assets:
technical_constraints:
design_constraints:
unknowns:
assumptions:
```

Do not ask the user to fill every field. Populate what is already known from the conversation/files.

## Minimum viable input

### Greenfield

Strong enough to start in most cases:

```text
Brand/logo
+ industry
+ what the business sells/does
+ contact details
```

If business model, audience, or CTA is obvious enough from supplied material, proceed. If a missing item materially changes the site's conversion strategy, ask it as a blocker.

### Reference clone

Usually enough to start:

```text
Reference URL
+ requested scope
```

Public HTML/CSS/assets should be discovered proactively. Do not ask for CSS before attempting discovery.

## Helpful but non-blocking inputs

```text
Target audience
Geographic market
Primary CTA
Product/service priority
Existing copy/images
Required pages
Known integrations
SEO/content priorities
Competitors the user likes/dislikes
```

## Question policy

Before asking anything, classify each unknown:

```text
BLOCKER   = different answers materially change strategy/IA/conversion/compliance
INFERABLE = AI can design a safe, reasonable default
DEFERABLE = not needed for the current step
```

Then:
- ask only BLOCKER items;
- combine blockers into one compact batch;
- prefer 1–3 questions, rarely more than 5;
- never ask the user to choose routine CSS/design implementation details;
- state important assumptions instead of hiding them.

## Example

User gives:

```text
Logo
Industry: industrial laser machines
Phone/email/address
```

Normalization:

```text
project_mode: greenfield
industry: industrial laser equipment
business_model: likely B2B [assumption]
primary_offer: unknown [blocker if product/service range cannot be inferred]
audience: manufacturers/factories [assumption]
primary_cta: request quote/consultation [inferable]
contact: known
```

The agent should ask only for the missing offer if it truly cannot be inferred, not for colors, radius, font size, card style, or container width.
