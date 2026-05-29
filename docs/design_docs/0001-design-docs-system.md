---
created: 2026-03-04
status: Implemented
---

# Design Docs System

## Overview

Implement a structured system for documenting feature ideas, requirements, and implementation plans before development begins.

## Objectives

- Create standardized template for design documents
- Establish clear naming and numbering conventions
- Track design doc lifecycle through status metadata
- Maintain centralized index of all design documents
- Enable quick scanning of requirements and examples without verbose text

## Requirements

### Functional Requirements

- Template must include YAML frontmatter with `created` date and `status` field
- Files named using sequential numbering: `NNNN-kebab-case-title.md`
- Guidelines doc tracks all docs grouped by status in index tables
- Template sections: Overview, Objectives, Requirements, Usage Examples, Implementation Steps, Open Questions
- Content should be concise: bullet points, code blocks, clear structure

### Non-Functional Requirements

- Easy to navigate and scan quickly
- No external dependencies or tooling required
- Flat directory structure (no nested folders by bounded context)
- Version controlled in git alongside source code

## Usage Examples

### Example 1: Creating New Design Doc

```bash
# Create a new file using the template from the "Template" section in design-doc-guidelines.md
touch docs/design_docs/0002-my-feature.md

# Edit metadata
# ---
# created: 2026-03-04
# status: Proposed
# ---

# Fill in sections with concise content following the template structure
```

### Example 2: Updating Design Doc Status

```yaml
# Change status in frontmatter when implementation starts
---
created: 2026-03-04
status: In Progress
---
```

### Example 3: Maintaining Index

```markdown
# Add entry to design-doc-guidelines.md in appropriate status table
| 0002 | My Feature | 2026-03-04 | [0002-my-feature.md](0002-my-feature.md) |
```

## Implementation Steps

1. Create `design-doc-guidelines.md` with the convention, template, and index tables for tracking all design docs
2. Create this meta design doc (0001) documenting the system itself
3. Add entry for 0001 to the Implemented table in `design-doc-guidelines.md`
4. Create the first feature design docs (0002, 0003, 0004) as real-world validation of the template
5. Add entries for each new doc to the index tables in `design-doc-guidelines.md`

## Open Questions

None - implementation complete.

## Notes

- YAML frontmatter is the standard format for metadata in markdown documentation systems (Jekyll, Hugo, etc.)
- Sequential numbering provides stable references even as documents change status
- The guidelines doc doubles as the index, keeping everything in one place
- Flat structure keeps things simple; can revisit if number of docs grows significantly
- No links to PRs/commits in design docs to avoid stale references

