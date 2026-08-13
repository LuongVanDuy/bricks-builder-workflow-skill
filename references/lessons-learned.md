# Lessons Learned

Read this file before doing Bricks work. New confirmed lessons are appended chronologically.

## L001 — Global Class names are not Global Class references

**Status:** confirmed  
**Scope:** Bricks template JSON

**Wrong:** Put utility/component class names only in `_cssClasses` and assume Bricks treats them as native Global Classes.

**Correct:** Native Bricks Global Classes are referenced by internal IDs in `_cssGlobalClasses`. Obtain those IDs from a real Global Classes export from the target site.

**Rule:** Never invent Global Class IDs. Map `name → real ID`.

---

## L002 — Keep reusable design-system naming generic

**Status:** confirmed  
**Scope:** Variables, classes, templates

**Wrong:** Carry a reference brand name into reusable variables/classes.

**Correct:** Learn the reference site's values but normalize naming to generic roles such as `--container-max`, `--color-primary`, `--space-4`, `site-header`.

**Rule:** Reference sites teach values and patterns, not reusable naming.

---

## L003 — Project foundation import workflow

**Status:** confirmed for this workflow  
**Scope:** Bricks Style Manager setup

**Wrong:** Treat Variables, Colors, Typography, and Spacing as four equivalent CSS import stages.

**Correct:** Use:
1. Variables CSS for core + typography + spacing tokens.
2. Bricks Color Manager JSON for the palette.
3. Theme Style JSON for global defaults.
4. Parsed CSS for the Layout Framework.

**Rule:** Typography and spacing tokens are centralized in Variables for this workflow instead of relying on separate manual scale setup.

---

## L004 — Theme Style and Variables have different jobs

**Status:** confirmed  
**Scope:** Bricks Style Manager

**Wrong:** Duplicate the same design values in both Variables and Theme Style.

**Correct:** Variables store reusable values; Theme Style decides where those values become defaults.

**Rule:** Theme Style should reference tokens rather than duplicate hard-coded values.

---

## L005 — Native WordPress menu stays native

**Status:** confirmed  
**Scope:** Header/navigation templates

**Wrong:** Rebuild a WordPress navigation menu as a static set of HTML/text links.

**Correct:** Use the Bricks `nav-menu` element connected to WordPress Menu data.

**Rule:** Preserve WordPress/Bricks native dynamic behavior whenever available.

---

## L006 — Proactively discover public source assets before asking the user

**Status:** confirmed  
**Date:** 2026-08-13  
**Scope:** Reference-site cloning / source discovery  
**Evidence:** User correction during Langfarm clone setup  

**Wrong:** Ask the user to provide the site's CSS immediately even though the reference website is public and asset discovery has not yet been attempted.

**Correct:** Start from the public URL, inspect available HTML, follow discoverable stylesheet/bundle/import URLs, search related public asset paths when necessary, and only request HTML/CSS files if retrieval is blocked, incomplete, or exact source verification cannot be achieved.

**Rule:** Public URL first → proactive HTML/CSS/assets discovery → request user files only as fallback.

---

## L007 — Keep research scoped to the exact requested domain

**Status:** confirmed  
**Date:** 2026-08-13  
**Scope:** Reference-site cloning / web research  
**Evidence:** User correction during Langfarm clone setup  

**Wrong:** Use related, legacy, mirror, similarly named, or third-party domains as evidence for the requested reference website without explicit user approval.

**Correct:** Treat the exact hostname supplied by the user as authoritative. Search, open, and follow assets from that hostname first. Only leave that domain when the requested domain itself explicitly references an external asset/CDN, or when the user explicitly asks for broader research. Clearly label external-source evidence if it is ever needed.

**Rule:** Exact requested domain is the source of truth. Do not substitute `old.*`, mirrors, similarly named sites, aggregators, or unrelated search results for the target site.

---

## L008 — Artifact-first execution is required for interactive Bricks work

**Status:** confirmed  
**Date:** 2026-08-13  
**Scope:** Execution speed / ChatGPT Work / agent-style runs  
**Evidence:** A Style System run spent more than 10 minutes researching and re-checking Bricks documentation before producing the first file.

**Wrong:** Treat every Bricks task like an exhaustive autonomous research job: re-open documentation already encoded in the skill, validate repeatedly, continue researching after enough evidence exists, and delay all artifacts until the entire stage is fully analyzed.

**Correct:** Default to fast iteration. Work only the requested stage, reuse rules already verified in the skill, stop research when evidence is sufficient, create the first usable artifact immediately, validate once at the end, and continue to later stages only when explicitly requested. For multi-file stages, create files incrementally instead of waiting for every research branch to finish.

**Rule:** Earliest usable artifact wins. Research and verification must have a stopping condition and must not delay delivery without a material accuracy reason.

---
