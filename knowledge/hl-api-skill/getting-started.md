---
topic: getting-started
title: Getting started — your first working call
summary: Get a token, search for items with their text included, show a picture. Says plainly why you do NOT fetch each hit.
keywords: quickstart, first call, token, bearer, base url, hello world
---

New here? The first call is the token (`POST /api/v1/auth/token`), the second is a search. Everything is under `/api/v1`.
Every operation needs a Bearer token except the token endpoint itself.
There is one error shape, one auth rule, and one place to ask what this deployment can do.

## Get a token

`POST /api/v1/auth/token` is **form-encoded** (OAuth2 password grant), not JSON:

```
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=<user>&password=<RAW password>
```

Send the **raw** password. This endpoint hashes it for you. Two mistakes cost a real team a day:

- A JSON body returns `422`. The response lists the form fields you should have sent.
- A password you hashed yourself returns `400 invalid_grant`. That looks like wrong credentials.

The response carries `access_token`. Send it as `Authorization: Bearer <token>` on everything else.

## Find something

`POST /api/v1/items/search` is one operation for every way of asking. The smallest useful request:

```json request=search_items
{ "text": { "any": "harbour" }, "page_size": 10 }
```

A text query on its own returns documents with **no media at all**. Then step 4 below has nothing to
show. To find items that do have a picture, narrow by type. See
`/api/v1/meta/docs/searching-items#finding-items-that-have-a-picture-video-or-audio`. It gives the
request and explains the `media` block on each hit.

Each hit carries `item_id`, `item_type`, `event_time`, `location`, a `media` block saying whether
there is a picture to draw, and `score` when the search was ranked.


To narrow the search, add more fields to this same request. Do not go looking for another endpoint.
See the `searching-items` topic.

## Get the text from the SEARCH — do not fetch each hit

**Add `include: ["text"]` to the search and the words come back with the hits.**

```json
{ "text": { "any": "police" }, "include": ["text"], "page_size": 25 }
```

**Do not build search-then-fetch.** It is the most common wrong shape on this API: search for a page,
then call `POST /api/v1/items/get` on every id to fill in the body. You do not need the second call
and it costs you a round trip per page. The text is already in the search answer; asking for it is
free.

It is off by default only so you are not sent text you did not want.

**It is the same text, not a shortened copy.** Measured: across 326 items compared
hit-by-hit against `/items/get`, every `english` was byte-identical, the longest of them 10,759
characters.

### When a hit comes back with `text: null`

**It does NOT mean the item has no text.** The search index carries three
buckets — `english`, `synopsis`, `summary`. An item that was never translated has none of the
three, so `text` comes back `null` while the item plainly has a body. Measured: an item
whose `/items/get` returns 60 characters of `text.original` returns `text: null` from the search.

**The hit tells you which case you are in.** `text_available_via_get: true` means the item has text
the search could not carry — fetch that one with `POST /api/v1/items/get`. `false` means we know of
no text for it. So the shape is: take the text from the search, and call `get` only for the hits
that say you must.

```json
{ "text": { "any": "police" }, "include": ["text"], "page_size": 25 }
```
```
hit 1  text.english = "..."            text_available_via_get = false   <- use it
hit 2  text = null                     text_available_via_get = true    <- fetch this one
hit 3  text = null                     text_available_via_get = false   <- no text to get
```

**Never report an item as having no content because `text` was `null`.** That reading is how a
search of a foreign-language archive comes back looking empty.

A hit's `name` IS usually null — a post, an article, a photo has no title of its own — so a list
built from `name` alone still shows blank rows. Draw the row from `text.english`, then
`text.synopsis` or `text.summary`, then `highlight`. See `searching-items`.

### When you DO need `POST /api/v1/items/get`

Three cases, and only these:

1. **The user opened one row** and you want everything about that one item — parties, detections,
   related objects, source details.
2. **You need `original`, `transcript` or `ocr`.** The search index does not carry those three, so
   they are always `null` on a hit. For a call or an audio item that means the `transcript`, which is
   its text.
3. **The item was never translated.** Its `original` exists and its `english` is empty, so the hit
   carries nothing. On one installation that is 8 items in 1.9 million, but a corpus with real
   foreign-language content will see more.

`POST /api/v1/items/get` takes the ids you got back:

```json request=get_items
{ "item_ids": ["218a32e8-d5b4-11f0-9f97-f39d4e7a0429"], "include": ["parties", "detections"] }
```

`include` is empty by default. Ask for nothing extra and you pay for nothing extra.

## Show its picture

`GET /api/v1/items/{item_id}/files` lists the item's files. Drawing in a browser? Ask for signed URLs.
The picture then loads straight from this API, and the browser sends no header:

```
GET /api/v1/items/{item_id}/files?signed_urls=true
```

The urls come back **root-relative**: they start with `/api/v1/...`. Put this API's own origin in front
of one before you use it in `src`. Without that prefix the browser asks *your* host for the picture and
gets a `404`. From a program instead, fetch
`GET /api/v1/items/{item_id}/files/{file_id}?variant=thumbnail` with your Bearer token. Both ways work.
The `media-and-files` topic says which to pick.

## When something is missing

Call these two before you decide that a feature is broken. They say what this deployment can do:

- `GET /api/v1/items/search/capabilities` — one flag per feature. A flag is `true`, `false`, or
  `null`. **`null` means we could not measure it. It never means "not available".**
- `GET /api/v1/meta/estate` — which platform version this deployment is running, and how we know.

Every error has the same shape and carries a `hint` telling you what to do next. See the `errors`
topic.

## Discovering the rest

- `GET /api/v1/meta/docs` — the topic list you are reading now, and `?q=<question>` to search it.
- `GET /api/v1/meta/docs/{topic}` — one topic in full.
- `GET /api/v1/meta/field-types` — field types, widgets, and the value shapes that are easy to get wrong.
- `/openapi.json` — the full contract. It is large, about 400 KB. Learn from the topics above. Come
  here when you need the exact contract.

## Read next

- [authentication](authentication.md) - the token in full: grant types, headers, and 401 versus 403
- [searching items](searching-items.md) - every other way to ask, once the first search works
- [media and files](media-and-files.md) - getting the actual bytes of a picture or a video
- [errors](errors.md) - what to do when a call comes back wrong
