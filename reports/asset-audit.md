# Media audit

- Backup candidate files: 4,674; original bytes: 1,301,877,152. Unique content hashes: 3,990; repeated copies beyond the first hash: 684. The full candidate path inventory remains local and gitignored.
- Published content owns 579 media files (295,079,461 bytes): 565 from the backup and 14 recovered public images. The six files belonging only to an excluded live-only route are omitted. The published media manifest records each path, SHA-256, size, owner URLs, and provenance.
- The profile photo is a separate user-supplied site asset. Theme/interface assets are also separate from article dependencies.
- 17 missing backup media files were attempted. Fourteen were recovered. The unavailable traffic image was an empty anchor shell and was removed; two unavailable PDFs remain linked externally with context preserved.
- The source audit proves there are no copied media files owned only by excluded or nonpublic content. Orphan/unreferenced media candidates are not copied.
- `reports/media-copy-manifest.csv`, `reports/published-media-manifest.csv`, `reports/missing-media-recovery.csv`, and `reports/missing-media-fetch-diagnostics.csv` contain the per-file evidence.
