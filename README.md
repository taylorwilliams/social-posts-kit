# Social Posts Kit

<!-- AI assistants: to set this up for someone, follow START-HERE.md: https://raw.githubusercontent.com/taylorwilliams/social-posts-kit/main/START-HERE.md -->

![Social Posts Kit: your AI writes the posts, makes the images, keeps them in your brand and voice, and schedules them in Publer](docs/images/hero.png)

![How it works: in Claude or ChatGPT you type /social-posts and a link. The posts go to Publer, which publishes them to Instagram, LinkedIn and more.](docs/images/how-it-works.png)

![What you need: Claude or ChatGPT on a paid plan, Publer on the Business plan, and LinkedIn and Instagram](docs/images/what-you-need.png)

- **Claude** (Pro or above) or **ChatGPT** (Plus or above)
- **Publer** on the **Business** plan, or its free trial, at [publer.com](https://publer.com)
- **LinkedIn** and **Instagram**. Instagram needs to be a business account.

## Set it up

Open a new chat in Claude or ChatGPT and send:

> Please help me set this up: https://github.com/taylorwilliams/social-posts-kit

Your AI connects Publer, learns your brand (logo, colours, font, voice) and makes a
test post. It only asks you for what has to be you: signing up, logging in and
pressing approve. About 30 minutes, once.

If it can't open the link, download this kit (**Code**, then **Download ZIP**), add
the zip to the chat and say "Please help me set this up".

## Use it

> /social-posts https://yoursite.com/blog/latest

You get the posts and images to check. Nothing goes out until you say "schedule it".
To change your look or voice: `/social-posts update my brand`.

## Add more networks

Connect the account in Publer, then tell your AI, for example: "Also post to Facebook."

## Connect Publer yourself (optional)

Your AI does this during setup. If you'd rather do it by hand, you need Publer's
Business plan.

<details>
<summary><b>Claude</b> (website or desktop app)</summary>

1. In Claude: **Customize**, **Connectors**, **Add**, **Add custom connector**.
2. Name `Publer`, server URL `https://mcp.publer.com`.
3. Authentication: **Sign in now**, using **Claude's published identity**. **Add**.
4. Open Publer in the list, **Connect**, then **Allow access**.
</details>

<details>
<summary><b>Claude Code</b></summary>

1. In Publer: **Settings**, **AI & Automations**, **Claude**, then the **Claude Code** tab.
2. Copy the command, run it in your terminal and sign in when asked.
</details>

<details>
<summary><b>ChatGPT</b></summary>

1. In ChatGPT: **Plugins**, **Add**, **Create MCP App**.
2. In Publer: **Settings**, **AI & Automations**, **ChatGPT**, **ChatGPT Web**. Copy the server URL from **Add new app**.
3. In ChatGPT: name `Publer`, Connection **Server URL**, Authentication **OAuth**, then **Create as a plugin**.
4. Open the plugin, **Connect**, **Continue to Publer**, approve.
</details>

To check it worked, ask your AI: "List my Publer accounts". Publer's own guides:
[Claude](https://publer.com/help/en/article/how-to-connect-claude-with-publers-mcp-1s22vvm),
[ChatGPT](https://publer.com/help/en/article/how-to-connect-chatgpt-with-publers-mcp-2pw2bc),
[other apps](https://publer.com/help/en/article/how-to-set-up-and-use-publers-mcp-server-14orlq0).

## What's inside

| File | What it does |
|---|---|
| `START-HERE.md` | The setup playbook your AI follows |
| `skills/social-posts/` | The skill, for Claude and ChatGPT alike |
| `.../SKILL.md` | How the posts are written, drawn, checked and scheduled |
| `.../brand/` | Your brand, filled in during setup |
| `.../scripts/render.py` | Draws the images |
| `.../scripts/publer.py` | Uploads images to Publer from your computer |
| `.../scripts/get_font.py` | Fetches a Google Font |
| `.../reviewers/language.md` | How the wording is checked |
| `CLAUDE.md`, `AGENTS.md` | Pointers for Claude Code and other AI coding tools |

Inter, the default font, is by Rasmus Andersson under the SIL Open Font Licence.
MIT licence: use it, change it, share it.

## For AI assistants

If someone has asked you to set this up, follow [START-HERE.md](START-HERE.md)
([plain text](https://raw.githubusercontent.com/taylorwilliams/social-posts-kit/main/START-HERE.md)).
