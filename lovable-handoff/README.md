# Lovable Handoff Package

This package contains the material needed to reconstruct and continue the Hebrew intelligence-analysis prototype in Lovable without relying on chat history.

## Recommended import sequence

1. Create a new Lovable project.
2. Paste `PROJECT_KNOWLEDGE.md` into **Project settings -> Knowledge**.
3. Upload or provide the files in `data/` and `prototype/`.
4. Attach the screenshots in `screenshots/` as visual references.
5. Send the contents of `INITIAL_PROMPT.md` as the first project prompt.
6. Ask Lovable to verify every item in `ACCEPTANCE_TESTS.md` before redesigning or extending the application.
7. After parity is achieved, connect the Lovable project to a new GitHub repository.

## Package contents

- `PROJECT_KNOWLEDGE.md`: persistent product and implementation context.
- `INITIAL_PROMPT.md`: first prompt for rebuilding the application.
- `ACCEPTANCE_TESTS.md`: functional and visual parity checklist.
- `DATA_DICTIONARY.md`: schemas, terminology, and relationships.
- `DECISIONS.md`: important product decisions and rationale.
- `prototype/current-prototype.html`: current working standalone prototype.
- `data/events.csv`: 2,044 synthetic raw intelligence events.
- `data/locations.csv`: nine synthetic geographic locations.
- `screenshots/`: visual references for the existing application.

## Confidential evaluation material

The following source-project files are deliberately excluded:

- `event_id_mapping_private.json`
- `answer_key_he.md`
- `answer_key_he_large.md`
- internal model evaluation outputs

Do not add these to the client application or Lovable project. They reveal benchmark truth that should remain separate from the analyst experience.

## Source of truth

The current prototype is a design and behavior reference, not a required technical architecture. Lovable may rebuild it with React and TypeScript, but the terminology, data behavior, filtering behavior, RTL layout, and acceptance tests must remain intact.
