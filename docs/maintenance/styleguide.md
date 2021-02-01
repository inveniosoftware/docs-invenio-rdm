# UX Guide for Developers

### Intended audience

This guide is intended for developers of InvenioRDM itself.

### Scope

The guide covers general style guidelines.

## User Experience

### Colors

- Standard:
    - The default color used by Semantic UI for components (this is defined per component).
- Brand:
    - The color used for theming your InvenioRDM


- ❌ Do not style components with color names (e.g. ``<div class="ui blue segment">``).
- ✅ Do style components with logical color names (like ``<div class="ui brand segment">``).

### Color emphasis

Semantic UI allows you to change emphasis of certain components. For instance, a button can have the following emphasis:

- Primary - Used for making an element more noticable (e.g. for highlighting the primary action).
- Secondary - Used for making an element less noticeable.
- Positive - Used for creating of big new things (example New upload, New community).
- Negative - Used for dangerously destructive operations (example deleting a community).

**IMPORTANT**: When changing color of a component, always thing about logically about emphasis rather than a specific color. Always use logical names, rather than specific.

### Button colors and order

#### Order

- ✅ Cancel (standard) | Save (primary)
- ❌ Save (primary) | Cancel (standard)
- ❌ Cancel (negative) | Save (positive)
- ✅ Delete (negative) | ...  | Save (standard) | Publish (primary)

### Captilization

**Form labels**:

- ✅ Resource type
- ❌ Resource Type
