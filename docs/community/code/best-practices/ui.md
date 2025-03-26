# User interface

### Intended audience

This guide is intended for developers of InvenioRDM.

### Scope

The guide covers general style guidelines.

## User experience

### Colors

- **Standard**:
    - The default color used by Semantic UI for components (this is defined per component).
- **Brand**:
    - The color used for theming your InvenioRDM.

**Dos and don'ts:**

- ✅ Do style components with logical class names (like ``<div class="ui brand segment">``).
- ❌ Don't style components with color names (e.g. ``<div class="ui blue segment">``).

### Color emphasis

Semantic UI allows you to change the emphasis of certain components. For instance, a button can have the following emphasis:

- **Primary** - Used for making an element more noticable (e.g. for highlighting the primary action).
- **Secondary** - Used for making an element less noticeable.
- **Positive** - Used for creating of big new things (example New upload, New community).
- **Negative** - Used for dangerously destructive operations (example deleting a community).

**IMPORTANT**: When changing the color of a component, always think about the logic of the emphasis rather than a specific color. Always use logical names, rather than specific color names. Colors change from instance to instance, emphasis doesn't!

### Button colors and order

#### Style

- ✅ Do use ``compact`` or different sizes (``mini``, ``small``, ...) buttons.
- ❌ Don't use ``basic`` style buttons.

#### Order

Order buttons correctly:

- ✅ Cancel (standard) | Save (primary)
- ✅ Delete (negative) | ... (space) | Save (standard) | Publish (primary)
- ❌ Save (primary) | Cancel (standard)
- ❌ Cancel (negative) | Save (positive)

### Capitalization

**Form labels**:

- ✅ Resource type
- ❌ Resource Type
