# README photos review

Initial photo import, 2026-10-23. Four supplied hardware photos were resized without cropping
and encoded as WebP for the English and Russian README. Source photos remain
unchanged. The keyboard photo is visible above the features; PCB, markings
and controller photos are visible as linked 240-pixel thumbnails below it.

| Image | Dimensions | Bytes |
| --- | --- | ---: |
| keyboard.webp | 1440 × 624 | 53,404 |
| pcb.webp | 1600 × 669 | 178,980 |
| pcb-markings.webp | 1200 × 941 | 78,234 |
| controller.webp | 1200 × 904 | 68,200 |

Total size changed from 9,104,068 to 378,818 bytes, a 95.8% reduction.
Root visual inspection confirmed readable board and controller markings.
Independent reviewer review_readme_photos checked both README diffs, links,
all four images, dimensions and metadata profiles; no findings remained.
Documentation checks passed: 33 documents, zero failures. This is a
documentation and image review, not hardware compatibility verification.

Layout follow-up, 2026-10-23: the collapsed block was replaced with visible
linked thumbnails after the display request. Independent review_readme_photos
approved both README translations, paths and alt text; no image bytes changed.

Final layout, 2026-10-23: the keyboard photo was replaced by the supplied
banner, resized to 1440 × 720 and 74,610 bytes (source183,972 bytes). All
three technical photos are now inside one collapsed Hardware Compatibility
section. The previous keyboard asset was removed from the current tree; its
tracked version remains in Git history. Independent review_readme_photos
approved both README translations, readable banner, paths and unchanged
compatibility claims. Documentation and whitespace checks passed.
