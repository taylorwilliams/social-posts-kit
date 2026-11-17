# Setup playbook (for the AI)

You are setting up **Social Posts Kit** for someone who runs a business. They have
shared this repository with you and asked for help setting it up. They are probably
not technical. When you are done, they can say "make social posts about <link>" and
get LinkedIn and Instagram posts in their own voice, with on-brand images, saved in
Publer ready to schedule.

Follow this playbook in order. It has six stages. Finish each one before the next.

## How to work with them

- One question or one instruction at a time. Wait for the answer.
- Plain words. Say "the address in your browser's bar", not "URL". No jargon.
- Number the steps you give them, and name buttons exactly as they appear.
- Tell them what you are doing and why in one short line, then do it.
- If they get stuck, ask for a screenshot of what they see.
- **Never ask them to paste a password or API key into the chat.** If they do,
  tell them to delete that key in Publer and make a new one.
- Interfaces change. If a button has a different name from the one here, use what
  they see and carry on.

## Stage 1. Get the kit, and find out where you are running

You need the kit's files, not just this page: the skill, its scripts and its font.
Get them without asking the user if you can:

- **With a terminal**: `git clone https://github.com/taylorwilliams/social-posts-kit`
  into a folder they choose (their home folder if they have no preference).
- **With a code tool**: download and unzip
  `https://github.com/taylorwilliams/social-posts-kit/archive/refs/heads/main.zip`.
- **If neither works** (no internet in your code tool): ask them to open
  https://github.com/taylorwilliams/social-posts-kit, choose the green **Code** button,
  then **Download ZIP**, and add the zip to this chat. Then unzip it.

The paths in this playbook are inside the kit's folder.


Work out which of these you are, from your own tools. Ask only if you can't tell.

| You are | You can run commands on their computer? | How images reach Publer |
|---|---|---|
| **Claude Code, or Claude Desktop with a terminal** | Yes | Uploaded with `scripts/publer.py` and an API key |
| **Claude on the web or the desktop app, without a terminal** | No (a code sandbox only) | They drag the image into the Publer draft |
| **ChatGPT** | No (a code sandbox only) | The Publer app attaches files from the chat |

Tell them in one sentence which route you will take.

## Stage 2. Publer (the prerequisite)

Publer is the scheduling tool that posts to LinkedIn and Instagram for them.

**Offer to do it for them.** Ask: "Would you like to do these steps yourself, with me
guiding you, or shall I do them for you?"
- **You can do it for them** if you can control their browser (for example Claude in
  Chrome, or ChatGPT's agent mode) or run commands (Claude Code). Go through each
  step below yourself, saying what you're doing as you go.
- **Only they can**: sign up and pay, type passwords, log in to Instagram, Facebook
  and LinkedIn, and press approve or allow on a sign-in screen. Stop at each of
  those, tell them exactly what to press, and carry on once they say it's done.
- **If you can't control the browser**, give them the steps one at a time.

1. **Account and plan.** Ask whether they have a Publer account on the
   **Business** plan (or its free trial). The connection to AI needs Business or
   Enterprise. If not: go to publer.com, sign up, and choose Business.
2. **Social accounts.** In Publer, they connect each network they will post to
   (Accounts, then Add account):
   - **LinkedIn**: their company page, not only their personal profile, if they
     post as the business.
   - **Instagram**: it must be a **Business or Creator** account linked to a
     **Facebook Page**. If it is a personal account, walk them through switching it
     in the Instagram app (Settings, Account type and tools, Switch to professional
     account) and linking a Page.
3. **Connect Publer to you.** In Publer: Settings, AI & Automations, then under
   AI & MCP choose their AI (Claude or ChatGPT). Publer shows the steps for each.
   - **Claude (web or desktop)**: Customize, Connectors, Add, Add custom connector.
     Name: `Publer`. Server URL: `https://mcp.publer.com`. Sign in now, using
     Claude's published identity, then Connect and Allow access.
   - **Claude Code**: Publer's Claude Code tab gives one command to run in the
     terminal. Run it for them, then they sign in when the browser opens.
   - **ChatGPT**: Plugins, Add, Create MCP App. Name `Publer`, Connection: Server
     URL (copied from Publer's "Add new app" step), Authentication: OAuth. Create
     it, Connect, Continue to Publer, approve.
   - **Other AI apps**: Settings, AI & Automations, MCP shows the server URL. Use
     OAuth if the app supports it.
   - If a screen looks different, Publer's guides have the latest steps:
     https://publer.com/help/en/article/how-to-connect-claude-with-publers-mcp-1s22vvm and
     https://publer.com/help/en/article/how-to-connect-chatgpt-with-publers-mcp-2pw2bc
4. **Check it worked.** Use the Publer tools to list their accounts. Read back the
   names and networks you can see, and ask if that is everything.

## Stage 3. The API key (only if you can run commands)

Skip this stage in ChatGPT and in Claude without a terminal.

The Publer connector can't attach a file from their computer, so images go up
through Publer's API with a key that only lives on their computer.

1. In Publer: Settings, Access & Login, **API Keys**, Create API Key. Name it
   `Social posts`. Keep **Workspaces** and **Accounts** ticked, and tick **Media**
   and **Posts**. Create.
2. Tell them: "Copy the key with the copy button. Don't paste it anywhere, not
   even here. Tell me when it's copied."
3. When they say it's copied, save it from the clipboard without showing it, then
   clear the clipboard:
   - **Mac**:
     `security add-generic-password -U -a "$USER" -s publer-api-key -w "$(pbpaste | tr -d '[:space:]')" && pbcopy </dev/null`
   - **Windows (PowerShell)**:
     `[Environment]::SetEnvironmentVariable('PUBLER_API_KEY', (Get-Clipboard).Trim(), 'User'); Set-Clipboard -Value ' '`
     (new terminals pick it up)
   - **Linux**: ask them to add `export PUBLER_API_KEY=...` to their shell profile themselves.
4. Check it: `python3 skills/social-posts/scripts/publer.py workspaces`. Read back
   the workspace names, never the ids. If they have more than one, ask which is for
   this business and note it for `brand.json`.

Never print, echo or log the key.

## Stage 4. Their brand

Ask these one at a time. Offer to work things out from their website whenever you
can, so they type less. Save what they share in `skills/social-posts/brand/`.

1. **The business.** Name, what they do, who their customers are, and their
   website. Read the website if you can: it answers several of the questions below.
2. **Logo.** Ask them to upload it, ideally a PNG with a transparent background or
   an SVG. Save it as `brand/logo.png` (convert an SVG if you can). No logo is fine:
   the name is drawn in their heading font instead.
3. **Colours.** Ask for their brand colours. If they don't know, take them from the
   logo or the website, show them the colours you picked (hex and a plain name,
   such as "deep green #1F5135"), and ask if they look right. You need: background,
   ink (text), accent, soft (a light tint of the accent) and muted (grey text).
4. **Font.** Ask what font they use.
   - If they don't know, ask for their website and find it there (the page's CSS
     `font-family`, or a Google Fonts link).
   - If it's on Google Fonts, run `python3 skills/social-posts/scripts/get_font.py "Font Name"`
     (or ask them to download it from fonts.google.com and upload the file).
   - If it's a paid font, they can upload the file they are licensed to use.
   - Or they can suggest one, or keep the default, Inter.
   You need a heading weight (bold or extra bold) and a body weight.
5. **Voice.** Ask:
   - three words for how they want to sound (for example: friendly, expert, plain)
   - words or phrases they never want used
   - UK or US spelling
   - emoji: none, a few, or plenty
   - anything they must never claim (legal, medical, prices)
6. **Examples.** Ask for posts they like, from anyone (screenshots or links), and
   posts they have made before. Say what you notice in them: length, tone, how they
   open, image style. Save images in `brand/examples/`.
7. **Where and when.** Which networks (LinkedIn, Instagram; more later). How often,
   which days and at what time, and their time zone. Instagram posts work best at
   no more than one a day.
8. **Links.** LinkedIn posts can carry a link. Instagram can't: what is their link
   in bio? Suggest a link-in-bio page if they don't have one.
9. **What they'll post about.** Blog posts, products, offers, news, tips. Where
   those live (website pages, a document, their own words).

## Stage 5. Write it down, then test it

1. Fill in `skills/social-posts/brand/brand.json` (colours, fonts, logo, time
   zone, networks, posting) and `skills/social-posts/brand/brand.md` (everything
   else, in their words). Show them `brand.md` and ask what to change.
2. **Test image.** Make a spec for a real topic of theirs and run
   `python3 skills/social-posts/scripts/render.py spec.json`. In a sandbox, install
   Pillow first if needed (`pip install pillow`). Show the images. Adjust colours,
   font or layout until they are happy.
3. **Test post.** Follow `skills/social-posts/SKILL.md` end to end on one real
   topic. Save it in Publer **as a draft only**. Ask them to look at it in Publer.

## Stage 6. Make it reusable

Set it up so a new chat can use it with one sentence.

- **Claude Code**: copy `skills/social-posts` to `~/.claude/skills/social-posts`
  (all projects) or `.claude/skills/social-posts` (this folder only).
- **Claude on the web or desktop**: zip the `skills/social-posts` folder (the folder
  itself at the top of the zip). They upload it in Customize (or Settings), Skills,
  Upload skill, and keep the Publer connector on.
- **ChatGPT**: zip the `skills/social-posts` folder the same way. They upload it in
  Plugins, Skills, Create, Upload from your computer, and keep the Publer app
  connected. If their plan has no Skills, make a **Project** instead: paste the
  `SKILL.md` text (without its top block) into the project's instructions, add the
  zip to the project's files, and tell it to unzip the zip with its code tool first.

Then tell them how to use it. In both Claude and ChatGPT a skill is started by
typing `/` and picking it from the list:

> In a new chat, type `/social-posts` and then what to post about, such as
> `/social-posts https://yourwebsite.com/blog/latest`. You get the posts and images
> to check. Nothing goes out until you say "schedule it".

And how to change things later: `/social-posts update my brand`.

Have them try `/` once now, so they see the skill in the list.

Finally, say what you set up in a short list, and anything left for them to do.
