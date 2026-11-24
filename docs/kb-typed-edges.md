# Proposal: typed, weighted links between kb pages

Status: recommendation only. Nothing in the skills reads this yet.

Today a kb page links to related pages with plain relative Markdown links
(`story-memory/resources/kb-layout.md`, "Linking"). A link says two pages are
related but not how, or how strongly. Agents that build context (muse,
`kb-lead`, `continuity-checker`, `atlas`) then treat a passing mention and a
defining relationship the same.

## The proposal

Each kb page may carry a `relations:` list in its frontmatter. One entry per
link that matters, with a type from a small fixed vocabulary, a weight, and
where the story shows it:

```yaml
---
relations:
  - to: ../characters/theo.md
    type: loves            # from the vocabulary below
    weight: 0.9            # 0.0 (incidental) to 1.0 (defining)
    since: ch03            # chapter or arc where it is established
    evidence: ch03 "the letter scene"; ch11 reunion
  - to: ../world/cryo-facility.md
    type: located-in
    weight: 0.6
    since: ch01
---
```

Plain links in the body stay as they are. `relations:` lists only the edges
worth weighting.

## Suggested type vocabulary

Keep it short and put it in `kb/vocab.md` so every agent uses the same words.

| Group | Types |
|---|---|
| People | `loves`, `family-of`, `allied-with`, `opposes`, `mentors`, `owes`, `fears` |
| Place and things | `located-in`, `belongs-to`, `controls`, `made-of` |
| Story logic | `causes`, `reveals`, `foreshadows`, `contradicts`, `depends-on` |
| Time | `before`, `after`, `during` |

Edges are directed. When the reverse matters (`mentors` and `mentored-by`),
write it on the other page too, or let a tool derive it.

## Weight scale

- `1.0` defining: the story breaks without it
- `0.7` strong: drives scenes or choices
- `0.4` present: recurs, but changes little
- `0.1` incidental: mentioned once

A weight is a judgment about the story, so it follows the kb rule: only what
the author confirmed or the finished prose establishes. Trials stay in `work/`.

## What would read it

- `kb-lead` and `kb-maintainer` keep `relations:` current when a chapter settles.
- `continuity-checker` flags prose that contradicts a heavy edge.
- `atlas` sizes and labels its relationship map by type and weight.
- Context building pulls the heaviest edges first when the budget is tight.
- `hooks/check_kb_links.py` can be extended to check that every `to:` resolves.

Adopting it means changes to `story-memory`, `kb-lead` and `atlas`; that is a
separate change once the shape is agreed.
