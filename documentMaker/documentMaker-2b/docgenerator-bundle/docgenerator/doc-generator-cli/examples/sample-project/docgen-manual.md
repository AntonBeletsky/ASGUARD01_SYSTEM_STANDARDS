# User Manual -- hand-written parts

> This file is yours. `doc_generator.py` reads it on every run but never overwrites it.
> Write text under a `##` heading and it appears in the generated User Manual, marked as
> written by hand. Basic markdown works: paragraphs, `-` lists, **bold**, `code`, [links](url).
> Text inside HTML comments is ignored, including the hints below; a section you leave empty
> stays marked TEMPLATE in the output instead of pretending to be an answer.

## Overview
<!-- docgen-hint: README.md was found at the project root, so this section is already filled from it. Write below only to ADD something the README does not say. -->

## Requirements
<!-- docgen-hint: Declared runtime versions and external libraries are filled in automatically. Add what code cannot show: required server or OS, supported browsers, accounts or API keys. -->

## Getting started
For a local preview with live reload instead of opening the file directly:

```bash
npm install
npm start
```
<!-- docgen-hint: 2 package.json script(s) are listed automatically. Write the real first-run steps: install, configure, run, and what success looks like. -->

## Project structure
<!-- docgen-hint: The folder summary is automatic. Add one line per top-level folder saying what it is FOR. -->

## Customization
To retheme, edit the variables in `css/vars.css` -- `--color-primary` and `--color-accent` drive almost every color on both pages.
<!-- docgen-hint: 11 CSS custom properties found and listed automatically. Explain HOW to use them: switch the color scheme, change fonts, add a page. The tool sees the properties, not your intent. -->

## Third-party credits
<!-- docgen-hint: Packages, CDN libraries and bundled fonts are listed automatically, but their LICENSES cannot be read from code. For every font, icon, image and library you did not author: who made it, under which license, and a link to the source. -->

## FAQ
**Can I use the drone photos on my own site?** No -- the images in this demo are placeholders and carry no license.

**Does the page need JavaScript?** Only for the theme toggle and the email check; everything else works without it.
<!-- docgen-hint: Real questions people ask about this project, each as a bold question followed by its answer. The tool has no way to know what they are. -->

## Changelog
<!-- docgen-hint: CHANGELOG.md was found and is used automatically -- you can delete this heading. -->

## Support
<!-- docgen-hint: How to reach you, what you will help with, what is out of scope, and how long support lasts. -->
