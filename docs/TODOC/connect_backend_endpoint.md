# TODO(todoc_001): Connect Settings to Backend

## Description
The `ui/src/components/pages/SettingsPage.tsx` component currently logs "Saving settings..." but lacks connection to the actual backend endpoint.

## Why
User settings changes must be persisted and enacted by the backend core logic.

## Acceptance Criteria
- [ ] Connect `SettingsPage.tsx` save handler to the corresponding backend endpoint.
- [ ] Ensure settings are correctly loaded and applied.
