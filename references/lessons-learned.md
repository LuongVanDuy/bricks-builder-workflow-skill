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
