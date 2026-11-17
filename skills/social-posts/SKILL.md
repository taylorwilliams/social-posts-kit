---
name: social-posts
description: Write LinkedIn and Instagram posts in this business's own voice, draw on-brand images at each network's exact size, check the language, and save them in Publer ready to schedule. Use when asked for social posts about a link, a page, a product or a few words, or to schedule posts in Publer. Also "update my brand".
---

# Social posts

Everything about the business is in `brand/`:

- `brand/brand.md`: who they are, their voice, words to avoid, examples, what they never claim
- `brand/brand.json`: colours, fonts, logo, time zone, networks and posting times
- `brand/examples/`: posts they like and posts they've made

Read both brand files before you write a word. If `brand.json` has no `name`, the
setup hasn't been done: follow `START-HERE.md` from the kit first.

Work in five steps. Show the user the posts and images before anything goes to
Publer. Nothing is published or scheduled without their "yes".

## 1. Read the source

- A link: read the whole page. A few words: ask one question if you need more.
- Every claim must come from the source or from `brand.md`. Never invent numbers,
  prices, customers or results. Respect "never claim" in `brand.md`.

## 2. Write the posts

Follow the voice in `brand.md` exactly: their tone words, spelling, emoji choice
and banned words. Match the examples they gave.

**LinkedIn** (`linkedin.txt`)
- The first two lines are the hook and must work alone: LinkedIn cuts at about 210
  characters with "see more". Name the reader's problem in their words.
- 120 to 220 words, short paragraphs, one idea each. A list of 3 to 5 points is good.
- What the reader gets, then one line on how the business helps.
- The link on its own line, tagged:
  `?utm_source=linkedin&utm_medium=social&utm_campaign=<topic>`.
- 3 to 5 relevant hashtags on the last line.

**Instagram** (`instagram.txt`)
- The first line is the hook: Instagram cuts at about 125 characters.
- 60 to 120 words, warmer and shorter than LinkedIn.
- Links don't work in captions: end with "Link in bio" (or their own words for it).
- 5 to 10 relevant hashtags after a blank line.

**Alt text** (`alt-text.txt`): one plain sentence per image, saying what it shows.

Never: invented facts, hype words from `brand.md`'s list, a line that sounds clever
but isn't true, or a line that needs reading twice.

## 3. Draw the images

Write a spec and run `python3 scripts/render.py spec.json` (Pillow needed:
`pip install pillow`). The script's top comment shows every option.

- `title`: short and plain, 4 to 10 words. Use the source's own title if it fits.
- `accent`: one word of the title to draw in the accent colour, the word that hooks.
- `layout`:
  - `chat`: a phone with a three or four message conversation and a result card.
    Best when the post is about customers getting in touch, ordering or booking.
    Keep messages short, the way a customer would write them.
  - `screenshot`: a picture of their product or website. Put the file in
    `brand/examples/` and name it.
  - `cover`: the title with a simple brand shape. For everything else.
- Sizes: `linkedin` 1200 × 627, `linkedin-portrait` 1080 × 1350, `instagram`
  1080 × 1350, `instagram-square` 1080 × 1080, `story` 1080 × 1920.

Look at every image before you show it. Fix anything cut off or crowded: shorten the
title, shorten the messages, or pick another layout.

## 4. Check the language

Review in rounds before anything goes to Publer. If you can start a separate agent,
give it `reviewers/language.md`, the post files and the user's feedback, and nothing
of your own view. If you can't, do the review yourself, strictly, as that file says.

Apply every finding. A point the user asked for stays: change its wording, keep the
point. Run another round while there is an `important` finding, up to 3 rounds. If
something important is still open after 3, show the user.

Then show the user: both posts in full, the images, and which image goes with which
post. Ask what to change.

## 5. Put them in Publer

Only after the user is happy with the copy and images.

1. **Accounts**: look up their Publer accounts (and the workspace from `brand.json`).
   If a network they want isn't connected, say so and skip it.
2. **Images**, by where you are running:
   - **With a terminal (Claude Code)**: `python3 scripts/publer.py upload <files>`
     prints a media id for each file. Attach it by id.
   - **ChatGPT**: use the Publer tool that creates a post from a file in the chat.
   - **Claude without a terminal**: create the post without the image, then ask the
     user to drag the image in from the downloads, in the draft in Publer.
3. **Save as drafts**: one per network, dated at the next posting time from
   `brand.json` (with the time zone's offset), unless the user gave a time. A dated
   draft sits on the calendar and does not go out.
4. **Schedule only on a clear yes** ("schedule it", "post it at 2pm"). Then switch
   each draft to scheduled, or create it scheduled. Instagram: one post a day at most.
5. Publer can't change the image on an existing draft. To change it, make a new
   draft and delete the old one.

Never show Publer ids or API keys to the user. Name accounts and posts by name.

## Reply

- Both posts in full, ready to copy.
- Which image goes with which post, and the folder they're in.
- What is in Publer: which accounts, the date and time, and whether each is a
  draft or scheduled.

## "Update my brand"

Ask what to change, update `brand/brand.json` or `brand/brand.md`, render one test
image if the look changed, and show it.
