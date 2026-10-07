---
topic: reuse-or-create
title: Reuse an existing type, or create one?
summary: A type is not free — deciding when to read someone else's type, when to own your own, and why a near-duplicate is the worst answer.
keywords: reuse, reuse or create, near-duplicate, own the concept, already exists
---

Before you write `POST /api/v1/entity-types`, decide whether you need a type of your own at all.

## Why this is a real decision

A type is not free. Creating one publishes the catalog, which recompiles the generated model and
restarts the platform's services — about **80 seconds** for a single type, with replicas still
rolling for around two minutes after. `POST /api/v1/entity-types/batch`
pays that cost **once** for a whole model instead of once per type, but it does not make a type cheap:
each one still has to be verified, granted and eventually torn down. The mechanics of all that are on
[modelling entity types](modelling-entity-types.md); this page is only about the choice.

A working deployment already carries dozens of types. So the question is not "can I create one" — it
is "does this application need its own".

## Reuse when

- An existing type already carries the fields you need and you only **read** it. Reading someone
  else's type costs nothing and creates nothing.
- The concept is genuinely deployment-wide — a person, a vessel, a harbour — and your application is
  one more consumer of it rather than its owner.
- You would otherwise create a near-duplicate that differs by one or two fields.

## Create when

- Your application owns the concept and its whole life — an incident, an invoice, a shift. Writing
  your own records into a type another team owns changes what their data means.
- You need fields, a section layout or a title and grid configuration the existing type does not
  have, and adding them would change a type other applications depend on.
- Your application has to be removable later. Deleting a type you did not create is technically
  allowed and is somebody else's outage: the delete revokes the type's grants from every profile
  that holds one and restarts services for the whole deployment. Own what you tear down.

## The worst outcome is a near-duplicate

Two types that mean the same thing and differ by one or two fields is the answer to avoid. It costs
two publishes instead of one, and it leaves a permanent ambiguity about which of the two is
authoritative — every later reader, human or agent, has to guess, and records end up split across
both. If you are within a field or two of an existing type you own, add the field to it.

## Resolve names against the live listing, never memory

Which types exist differs between deployments, and it changes over time. Measured on two
deployments: `SITE` was listed on both, and `PERSON` on one and **not** on the other.
That is the opposite of what the team building against it assumed, until they measured.

**Being listed is not the same as being usable, and that is the trap.** Measured on one
deployment: `GET /api/v1/entity-types/SITE` answers `200` with `canBeCreated: false` and **no
`fields` key at all**. It is a platform-owned type you can read about and cannot write to. Two agents
in a row read its presence in the listing as an invitation to reuse it.

So the listing tells you a name exists. Only reading the type tells you whether you can use it:
check `canBeCreated`, and check that `fields` is there and holds what you need.

So never decide reuse from a type name you remember or one you saw in an example. Call
`GET /api/v1/entity-types` against the deployment you are actually building on, and decide from what
it returns.

## Editing beats recreating

If the type is yours and it is close, change it rather than replacing it.
`PATCH /api/v1/entity-types/{type_name}` adds fields and sections and changes grid columns, icon and
display name **in place, with the existing records preserved**.

The catch is that a change can only **add** fields. The type's own display name can be changed, but
no operation takes a FIELD back — see [modelling entity types](modelling-entity-types.md) for the
measurement. So renaming or removing a field means delete-and-recreate, which costs two publishes and
risks leaving a half-created type behind. Get field names right the first time, and prefer adding a
new field to renaming an old one.

## Try it

List what this deployment already has, and look for your concept before you create anything:

```
GET /api/v1/entity-types
```

Then read the closest candidate in full with `GET /api/v1/entity-types/{type_name}` and check three
things, in this order:

1. **`canBeCreated`** — `false` means the platform owns it and you cannot write records into it, no
   matter how well the name fits.
2. **`fields`** — the fields it actually carries, not the ones its name suggests. A missing `fields`
   key means there is nothing to reuse.
3. **Does anyone use it?** `POST /api/v1/entities/{type}/search` with an empty body returns a count.
   Nothing in this API reports who OWNS a type, so this is the closest measurable thing: a type
   holding records is one somebody is relying on.

If it passes all three and has what you need, you are done and you have paid nothing.

**A word on the ownership test above.** "Does another team own this concept" is the right question and
the API cannot answer it. The instance count is a proxy, not the answer — a type with zero records may
still be someone's half-built model. When it matters, ask a human.

## Read next

- [what already exists](inspecting-what-exists.md) - reading the listing and one type's real definition
- [modelling entity types](modelling-entity-types.md) - how to create one, once you have decided to
- [entity instances](entity-instances.md) - putting records into a type, yours or someone else's
