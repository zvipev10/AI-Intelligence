---
name: i360-platform
description: >-
  Use when building anything on the i360 platform — modelling record types, creating and searching
  records, searching ingested items by text, meaning, picture, time or place, reading media, or
  asking the platform a question in plain words. Everything goes through platform-hl-api with an
  ordinary user's token; no cluster access. Triggers on i360, intel360, entity type, entity
  catalog, EMS, items search, or a request to build an app against the platform.
---

# i360, through one API

Built against **contract 252**. Everything below is generated from that contract and from the
API's own documentation — nothing here is written twice.

## First, always

Call `GET /map` on the estate you are building against. It answers JSON to anything that is not a
browser, and it tells you what THIS deployment can do, which differs between deployments.

Then compare its `contract_version` to **252** above. If the estate is ahead, this skill is
out of date: read the estate's own documentation with `GET /api/v1/meta/docs` and trust it over
anything baked in here.

## What you can do

- **Data model (ERD)** — Define the record types, their relationships, their fields and their controlled value sets.
- **Data records (CRUD)** — Create, read, update and remove records, and join them to each other.
- **Metadata and annotation** — Add human judgement on top of what the platform ingested.
- **Structured query** — Precise questions. This field equals that, in this window, inside this area.
- **Aggregation and analytics (OLAP)** — Counts, distributions and trends over whatever the query matched.
- **Vector and multimodal search** — Ask in plain language, or with a picture, and let the platform decide what you meant.
- **Object and media storage (BLOB)** — Get the actual bytes. A photo, a video, an audio clip, an attachment.
- **Identity and access management (IAM)** — Authentication, token issue, and what a caller is permitted to see and do.
- **Model inference (LLM)** — Have a model write, summarise or reason over what you found.
- **Events and messaging (pub/sub)** — Be told when something changes, instead of asking again.
- **API discovery and documentation** — Find out what this API can do, and what this particular installation supports.
- **Health and observability** — Know the service is alive and see how it is behaving.

## How to find out how

**`reference/index.md` in this skill names every topic this deployment serves** — the written guides
first, then the reference pages generated from the contract. Read it and pick the line that matches
what you are doing. It is the only list; do not work from memory.

Then:

```
GET /api/v1/meta/docs/<topic>          the one you picked, in full
GET /api/v1/meta/docs?q=<question>     if no line matches, rank the sections instead
```

Three topics are carried in `reference/` as text so you can start before you have a token. Every
other one is a single call away, and the deployment's copy is always the current one.

Ask, try the call, stop when it works.

## Turning a described data model into i360

This is the part you cannot look up, because it is a decision rather than a fact. Someone describes
their domain — "an incident tracker", "a chat app" — and you have to choose the i360 shapes.

**The domain is theirs. The i360 implementation of it is yours.** Do not ask them anything in i360
words. They do not know what an entity type is, and they should not have to.

### The decision that comes up every time

Is this thing its own record type, or a field inside another one? A chat message: its own type
linked to the conversation, or a repeating field inside it?

**Decide it by asking about behaviour, in their words.** The question is never "should this be an
entity type" — it is:

> *Do you need to find a single message on its own, or only find the chat and read it?*

Their answer decides it, and they can answer it. Read `reuse-or-create` for what each choice costs,
and `modelling-entity-types` for what the platform will and will not let you change afterwards.

### Ask rarely, and record everything

- **Ask only when both options are genuinely viable AND the choice is expensive to reverse.** Adding
  a field later is cheap. Splitting one type into two after it holds records is not.
- **Cap it at three questions.** Someone who asked for an incident tracker did not sign up for an
  interview, and a small model handles a long one badly.
- **Everything you did not ask, decide and write down.** Put a `MODEL-DECISIONS.md` in the app you
  build: each choice in plain English, why you made it, and what to change if it was wrong. That
  record is what you owe them in place of the question you did not ask.

### Then build it

1. **Look before you create.** `GET /api/v1/entity-types` — the deployment already carries dozens,
   and reusing one costs nothing. Never decide from a type name you remember.
2. **Dry run first.** The provisioning calls take `dry_run=true` and hand back the whole plan.
3. **One publish, not N.** Use the batch call. A publish restarts platform services for everyone on
   the deployment, so paying that once for a whole model is both faster and safer.
4. **Read back.** A write that answers ambiguously may still have landed. `errors` has the recovery,
   and its first line is the important one.
5. **Send `actors` on every record you create**, including the creator, or your list screens come
   back empty while `GET` by id keeps working.

### When something fails

Read the `hint` in the error before deciding the platform is broken. It names the next action.

`GET /api/v1/meta/docs?q=<the error code>` answers with the section that explains it. A `501` means
this deployment does not have that feature, which is not a bug and not worth retrying.

**Never blind-retry a write.** On a read a repeat costs nothing; on a write it is how a deployment
ends up with a half-created type that its own delete will refuse to remove.

### Before you tell anyone it works

Run it as the user who will actually use it, and try BOTH a search and a fetch by id. They are
checked differently, so either one can succeed while the other refuses — a fetch passes the
type-level check alone, and a search additionally filters by what that user may see. An admin gets
past everything and proves nothing.

### At the end, write down what this cost you

Before you finish, write `i360-session-feedback.md` next to whatever you built. It takes two minutes
and it is the only way this skill gets better.

The fields below are not a wish list. Five agents ran this skill against a live deployment,
and these are the five things that turned out to matter, in order:

1. **Anything the documentation told you that was WRONG** against the real deployment. Quote the
   sentence and say what actually happened. This outranks everything else on the page.
2. **Every question you asked `GET /api/v1/meta/docs?q=` that came back useless.** The exact words
   you typed, and what you wanted. Nobody can see a bad search from our side — a question that
   retrieves the wrong page looks identical to a question nobody asked.
3. **Every time you had to guess** a field name, a value shape, or a URL — and whether the guess was
   right. A lucky guess is still a gap.
4. **Every place you got stuck**, what unstuck you, and roughly how many calls it cost. If the thing
   that unstuck you was an error message rather than a document, say so: that means the API is
   teaching what the documentation should.
5. **What you wanted and could not find anywhere.**

Two rules for writing it:

- **No credentials, no tokens, no deployment hostnames, and none of your customer's data.** Describe
  the shape of what you were building, not the thing itself.
- **An unfinished task with a precise account of where the documentation ran out is more useful than
  a finished one with a vague report.** Do not tidy up your own confusion.

Send the file to whoever gave you this deployment. If a claim in it is wrong about the platform, the
fix goes into the documentation and reaches you on the next download — you do not edit your copy.

