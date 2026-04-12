# Step 3. Data Model (depends on all above)

## Items

- [x] 24) Verify each entity (Event, Thread, Contract, Report, Strategy, Policy) includes all required fields.
  - mostly documented in step_1_working.md (updates added to existing design)
- [/] 25) Ensure the YAML persistence mapping (PersistencePort → YamlFileStore) correctly serialises each entity.( skipped )
- [x] 26) Check naming consistency (`Thread.id` vs `thread_id` in code) to avoid mismatches.
- [/] 27) Evaluate whether extra entities (e.g., SchedulerState) are needed for future extensions. (skipped)
- [x] 28) Confirm versioning fields (e.g., contract version) are present for audit trails.

## Item 24

**Note – Entity field checklist**
- Event: defined with `type`, `payload`, `timestamp`; consider adding an `id` if unique tracking is needed.
- Thread: fields listed but no concrete class yet; ensure consistent naming (`id` vs `thread_id`) and define a `Message` sub‑type (`timestamp`, `sender`, `content`).
- Contract: fields present; optionally add a `version` field now for audit trails.
- Report: fields present; may add `report_id` for distinct identification.
- Strategy: fields present; ensure `focus_areas` typed as `List[str]`.
- Policy: fields present; `value` could be typed (`str|int|bool`) or a payload dict for richer policies.

**Next steps**
1. Resolve the Thread naming inconsistency across the codebase.
2. Define the `Message` schema used inside `Thread.messages`.
3. Add optional `version` to `Contract` now if audit trails are required.
4. Consider unique IDs for `Event` and `Report` for easier replay.
5. Make all field types explicit (`List[str]`, `Dict[str, Any]`, etc.) for static checking.

Once these dataclasses exist and naming is unified, the checklist items can be marked complete.
