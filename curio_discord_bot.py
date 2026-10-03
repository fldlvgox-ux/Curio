"""
CURIO — Discord Companion Bot
Automated link collecting, curating, and organizing for CURIO.
Works both locally (PC) and in the cloud (Render, Koyeb, etc.).
"""

import os
import sys
import io
import re
import json
import time
import asyncio
import base64
from datetime import datetime, timezone

if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', write_through=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', write_through=True)
    except Exception:
        pass

import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

CONFIG_FILE = "bot_config.json"
INBOX_FILE = "curio_inbox.json"
DEFAULT_PORT = int(os.environ.get("PORT", 8765))

# Cloud mode: detected when DISCORD_TOKEN env var is set, or no .git directory exists (cloud container/host)
CLOUD_MODE = bool(os.environ.get("DISCORD_TOKEN") or not os.path.exists(".git") or os.environ.get("GITHUB_TOKEN"))
GITHUB_REPO = os.environ.get("GITHUB_REPO", "fldlvgox-ux/Curio")
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{INBOX_FILE}"

DEFAULT_DRAWERS = [
    "Game Design & Engines",
    "Shaders & Tech Art",
    "Audio & Soundtracks",
    "Reference & Docs",
    "Photo Editing & RAW",
    "Digital Art & Illustration",
    "Vector & Graphic Design",
    "Publishing & Layout",
    "Photo Management & Viewers",
    "Pixel Art & Animation",
    "HDR, Panorama & AI Tools"
]

def load_config():
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass

    # Environment variables override or provide defaults for cloud hosting
    merged = {
        "discord_token": os.environ.get("DISCORD_TOKEN") or cfg.get("discord_token", ""),
        "channel_name": os.environ.get("CHANNEL_NAME") or cfg.get("channel_name", "curio-index"),
        "gemini_api_key": os.environ.get("GEMINI_API_KEY") or cfg.get("gemini_api_key", ""),
        "github_token": os.environ.get("GITHUB_TOKEN") or cfg.get("github_token", ""),
    }

    if CLOUD_MODE:
        print("[Config] Cloud mode active — using environment variables & API sync")
    return merged

def load_inbox():
    if not os.path.exists(INBOX_FILE):
        return {"version": "2.0", "drawers": DEFAULT_DRAWERS, "items": []}
    try:
        with open(INBOX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "items" not in data:
                data["items"] = []
            if "drawers" not in data:
                data["drawers"] = DEFAULT_DRAWERS
            return data
    except Exception:
        return {"version": "2.0", "drawers": DEFAULT_DRAWERS, "items": []}

def save_inbox(data):
    with open(INBOX_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_urls(text):
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    raw_urls = url_pattern.findall(text)
    filtered = []
    for u in raw_urls:
        u = u.rstrip(".,;!?:)>]}")
        # Skip Discord internal links, channels, attachments, CDN, invites, etc.
        if re.search(r'https?://(?:[a-zA-Z0-9-]+\.)?(?:discord\.com|discordapp\.com|discord\.gg|media\.discordapp\.net|cdn\.discordapp\.com)', u, re.IGNORECASE):
            continue
        filtered.append(u)
    return filtered

async def scrape_web_metadata(url):
    """Scrapes OpenGraph, oEmbed, and standard HTML metadata from URL."""
    # Special Handler: YouTube (oEmbed API for exact title & HD thumbnail + description scraping)
    if "youtube.com/watch" in url or "youtu.be/" in url or "youtube.com/shorts/" in url:
        title = ""
        author = "YouTube Creator"
        thumb = ""
        desc = ""
        
        # Pre-generate standard YouTube thumbnail from video ID
        yt_id_match = re.search(r'(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
        video_id = yt_id_match.group(1) if yt_id_match else ""
        if video_id:
            thumb = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
            
        try:
            oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
            timeout = aiohttp.ClientTimeout(total=8)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(oembed_url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        title = data.get("title", "")
                        author = data.get("author_name", "YouTube Creator")
                        oembed_thumb = data.get("thumbnail_url", "")
                        if oembed_thumb:
                            thumb = oembed_thumb
        except Exception as yt_err:
            print(f"[YouTube oEmbed Error] {yt_err}")

        # Clean title if it contains generic "- YouTube"
        if title:
            title = re.sub(r'\s*-\s*YouTube$', '', title, flags=re.IGNORECASE).strip()
        if not title or title.lower() in ["- youtube", "youtube"]:
            title = ""

        # Also extract video description & title from page source if needed
        try:
            yt_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.get(url, headers=yt_headers) as html_resp:
                    if html_resp.status == 200:
                        yt_html = await html_resp.text(errors="ignore")
                        if not title:
                            tm = re.search(r'"title":\{"runs":\[\{"text":"(.*?)"\}\]', yt_html) or re.search(r'<title>(.*?)</title>', yt_html)
                            if tm:
                                cand_title = tm.group(1).replace("- YouTube", "").strip()
                                if cand_title and cand_title.lower() != "youtube":
                                    title = cand_title
                        m = re.search(r'"shortDescription":"(.*?)"', yt_html)
                        if m:
                            raw_desc = m.group(1).encode('utf-8').decode('unicode_escape')
                            desc = raw_desc[:1500]
        except Exception as e:
            print(f"[YouTube Desc Scrape Error]: {e}")

        return {
            "title": title or (f"YouTube Video ({video_id})" if video_id else "YouTube Video"),
            "description": desc or f"Video by {author} on YouTube.",
            "image": thumb,
            "site_name": "YouTube"
        }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, allow_redirects=True) as resp:
                if resp.status >= 400:
                    slug_name = [p for p in url.split("/") if p and not p.startswith("http") and "." not in p]
                    fallback_title = slug_name[-1].replace("-", " ").replace("_", " ").title() if slug_name else url
                    return {"title": fallback_title, "description": "", "image": "", "site_name": ""}
                
                content_type = resp.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    return {"title": url.split("/")[-1] or url, "description": f"File type: {content_type}", "image": "", "site_name": ""}
                
                html = await resp.text(errors="replace")
                soup = BeautifulSoup(html, "html.parser")
                
                # Title
                title = ""
                og_title = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "twitter:title"})
                if og_title and og_title.get("content"):
                    title = og_title["content"].strip()
                elif soup.title and soup.title.string:
                    title = soup.title.string.strip()
                elif soup.find("h1"):
                    title = soup.find("h1").get_text().strip()
                else:
                    slug_parts = [p for p in url.split("/") if p and not p.startswith("http") and "." not in p]
                    title = slug_parts[-1].replace("-", " ").replace("_", " ").title() if slug_parts else url
                    
                # Description
                description = ""
                og_desc = (soup.find("meta", property="og:description") or 
                           soup.find("meta", attrs={"name": "description"}) or 
                           soup.find("meta", attrs={"name": "twitter:description"}))
                if og_desc and og_desc.get("content"):
                    description = og_desc["content"].strip()
                
                # Image
                image = ""
                og_img = (soup.find("meta", property="og:image") or 
                          soup.find("meta", attrs={"name": "twitter:image"}))
                if og_img and og_img.get("content"):
                    img_url = og_img["content"].strip()
                    if img_url.startswith("//"):
                        img_url = "https:" + img_url
                    elif img_url.startswith("/"):
                        from urllib.parse import urljoin
                        img_url = urljoin(url, img_url)
                    image = img_url
                    
                site_name = ""
                og_site = soup.find("meta", property="og:site_name")
                if og_site and og_site.get("content"):
                    site_name = og_site["content"].strip()
                    
                return {
                    "title": title,
                    "description": description,
                    "image": image,
                    "site_name": site_name
                }
    except Exception as e:
        print(f"[Scraper Error] {url}: {e}")
        slug_parts = [p for p in url.split("/") if p and not p.startswith("http") and "." not in p]
        fallback_title = slug_parts[-1].replace("-", " ").replace("_", " ").title() if slug_parts else url
        return {"title": fallback_title, "description": "", "image": "", "site_name": ""}

async def ai_curate(url, meta, api_key, available_drawers):
    """Uses Google Gemini free tier to classify drawer, extract tags, and summarize."""
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        # Fallback keyword categorization without AI
        return heuristic_curate(url, meta, available_drawers)
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
You are the AI archivist for CURIO, a curated catalog for game developers, digital creators, and tech enthusiasts.
Analyze this bookmarked resource:
URL: {url}
Page Title: {meta.get('title', '')}
Site Name: {meta.get('site_name', '')}
Description/Content: {meta.get('description', '')}

CRITICAL INSTRUCTION FOR VIDEOS / SHOWCASES:
If this link is a YouTube video, review, or article featuring a specific software, tool, app, plugin, or asset:
- Focus on the SOFTWARE / APP ITSELF being demonstrated, not just that it's a video.
- In "title", give the clean, accurate name of the software/tool (e.g. "ASYAR App", "Alt+Tab Window Delayer"). Do NOT use "- YouTube" or generic titles!
- In "notes", explain what the featured software does, its primary benefits, and why a user/creator would want it.
- In "tags", extract tags relevant to the featured software (e.g. its name, domain, what it replaces, OS platform, and features).
- In "drawer", pick the category that best fits the software or its domain.

Select the best matching Drawer from this list:
{json.dumps(available_drawers)}

Produce a JSON response with:
1. "title": A clean, concise title/name for the tool, app, or article (e.g. "Alt+Tab Window Delayer", "ASYAR Launcher"). If the page title is a raw URL or "- YouTube", provide an accurate name based on the content.
2. "drawer": The chosen drawer name from the list (or a crisp new 2-4 word category if none fit).
3. "tags": An array of 3 to 6 lowercase alphanumeric tags describing tech, domain, and format (e.g. ["asyar", "raycast", "productivity", "open-source"]).
4. "notes": A clear, informative 2-sentence summary highlighting the core software/tool and what it enables creators to do.
5. "rating": An integer rating from 3 to 5 based on utility.

Respond ONLY with valid JSON.
"""
        response = None
        for model_name in ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]:
            try:
                response = await asyncio.to_thread(
                    client.models.generate_content,
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    break
            except Exception as model_err:
                print(f"[Model {model_name} warning]: {model_err}")
                continue

        if not response or not response.text:
            return heuristic_curate(url, meta, available_drawers)
        
        text = response.text.strip()
        # Clean potential markdown fences
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n", "", text)
            text = re.sub(r"\n```$", "", text)
        data = json.loads(text)
        curated_title = data.get("title", "").strip()
        if curated_title and curated_title.lower() not in ["- youtube", "youtube"]:
            final_title = curated_title
        else:
            final_title = meta.get("title", "")

        return {
            "title": final_title,
            "drawer": data.get("drawer", "Reference & Docs"),
            "tags": data.get("tags", ["resource"]),
            "notes": data.get("notes", meta.get("description", "")),
            "rating": int(data.get("rating", 4))
        }
    except Exception as e:
        print(f"[Gemini AI Fallback]: {e}")
        return heuristic_curate(url, meta, available_drawers)

def heuristic_curate(url, meta, available_drawers):
    """Fallback classification when no AI key is provided."""
    full_text = f"{url} {meta.get('title', '')} {meta.get('description', '')}".lower()
    
    tags = set()
    # Tag extraction based on common keywords with strict word boundaries
    keywords = ["shader", "glsl", "godot", "unity", "unreal", "blender", "audio", "sfx", 
                "synth", "pixel-art", "vector", "svg", "ui", "font", "texture", "3d", "2d", 
                "engine", "open-source", "github", "tutorial", "tool"]
    for kw in keywords:
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, full_text):
            tags.add(kw)
    if not tags:
        tags.add("bookmark")
        
    drawer = "Reference & Docs"
    if any(re.search(r'\b' + re.escape(k) + r'\b', full_text) for k in ["shader", "glsl", "hlsl", "vfx"]):
        drawer = "Shaders & Tech Art"
    elif any(re.search(r'\b' + re.escape(k) + r'\b', full_text) for k in ["engine", "game dev", "godot", "unity", "unreal", "bevy", "raylib"]):
        drawer = "Game Design & Engines"
    elif any(re.search(r'\b' + re.escape(k) + r'\b', full_text) for k in ["audio", "sound", "music", "synth", "vst", "sfx"]):
        drawer = "Audio & Soundtracks"
    elif any(re.search(r'\b' + re.escape(k) + r'\b', full_text) for k in ["pixel", "sprite", "animation"]):
        drawer = "Pixel Art & Animation"
    elif any(re.search(r'\b' + re.escape(k) + r'\b', full_text) for k in ["vector", "svg", "logo", "icon"]):
        drawer = "Vector & Graphic Design"
    elif any(re.search(r'\b' + re.escape(k) + r'\b', full_text) for k in ["paint", "brush", "illustration", "draw"]):
        drawer = "Digital Art & Illustration"
    elif any(re.search(r'\b' + re.escape(k) + r'\b', full_text) for k in ["ai", "hdr", "generator", "llm"]):
        drawer = "HDR, Panorama & AI Tools"
        
    notes = meta.get("description") or f"Curated from {url}"
    return {
        "title": meta.get("title", ""),
        "drawer": drawer,
        "tags": list(tags)[:5],
        "notes": notes,
        "rating": 4
    }

async def github_api_push(inbox_data, item_title="Discord update"):
    """Push curio_inbox.json to GitHub using REST API (for cloud deployment)."""
    github_token = config.get("github_token", "") or os.environ.get("GITHUB_TOKEN", "")
    if not github_token:
        print("[GitHub API] No GITHUB_TOKEN set — skipping push")
        return False

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CURIO-Bot"
    }

    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Get current file SHA (required for updates)
            sha = None
            async with session.get(GITHUB_API_URL, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    sha = data.get("sha")

            # Encode new content
            content_bytes = json.dumps(inbox_data, indent=2, ensure_ascii=False).encode("utf-8")
            content_b64 = base64.b64encode(content_bytes).decode("ascii")

            # Push update
            payload = {
                "message": f"Curate: {item_title[:45]}",
                "content": content_b64,
                "branch": "main"
            }
            if sha:
                payload["sha"] = sha

            async with session.put(GITHUB_API_URL, headers=headers, json=payload) as resp:
                if resp.status in (200, 201):
                    print(f"[GitHub API] Pushed inbox to GitHub: {item_title[:35]}")
                    return True
                else:
                    err = await resp.text()
                    print(f"[GitHub API Warning] Status {resp.status}: {err[:150]}")
                    return False
    except Exception as e:
        print(f"[GitHub API Exception]: {e}")
        return False

def git_sync_push(item_title="Discord update"):
    """Auto-commits and pushes curio_inbox.json to GitHub repository (local mode only)."""
    try:
        import subprocess
        subprocess.run(["git", "add", INBOX_FILE], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", f"Curate: {item_title[:45]}"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, check=False)
        if res.returncode == 0:
            print(f"[Git Sync] Synced inbox to GitHub: {item_title[:35]}")
            return True
        else:
            print(f"[Git Sync Warning] Push skipped or error: {res.stderr.strip()[:100]}")
            return False
    except Exception as e:
        print(f"[Git Sync Exception]: {e}")
        return False

# -------------------------------------------------------------
# Local HTTP Server for CURIO Ingestion
# -------------------------------------------------------------
async def start_local_api(port=DEFAULT_PORT):
    app = web.Application()
    
    async def get_inbox_handler(request):
        inbox = load_inbox()
        return web.json_response(inbox, headers={"Access-Control-Allow-Origin": "*"})

    async def clear_inbox_handler(request):
        inbox = load_inbox()
        count = len(inbox.get("items", []))
        inbox["items"] = []
        save_inbox(inbox)
        return web.json_response({"status": "cleared", "cleared_count": count}, headers={"Access-Control-Allow-Origin": "*"})

    async def options_handler(request):
        return web.Response(headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        })

    app.router.add_get("/api/inbox", get_inbox_handler)
    app.router.add_post("/api/inbox/clear", clear_inbox_handler)
    app.router.add_options("/api/inbox", options_handler)
    app.router.add_options("/api/inbox/clear", options_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    host = "0.0.0.0" if CLOUD_MODE else "127.0.0.1"
    site = web.TCPSite(runner, host, port)
    await site.start()
    print(f"[API] CURIO Sync API running at http://{host}:{port}/api/inbox")

# -------------------------------------------------------------
# Discord Bot Core
# -------------------------------------------------------------
config = load_config()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!curio ", intents=intents)

@bot.event
async def on_ready():
    print(f"\n==========================================")
    print(f" [ONLINE] CURIO Bot Logged in as: {bot.user.name}")
    print(f" [LISTENING] Watching for links in channel: #{config.get('channel_name', 'curio-inbox')}")
    print(f" [INBOX] Saving items to: {os.path.abspath(INBOX_FILE)}")
    print(f"==========================================\n")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
        
    target_channel = config.get("channel_name", "curio-inbox").lower()
    ch_name = getattr(message.channel, "name", "").lower()
    is_target_channel = (ch_name == target_channel or "curio" in ch_name or "inbox" in ch_name or "index" in ch_name)
    is_dm = isinstance(message.channel, discord.DMChannel)
    
    print(f"[Discord Event] Received message in #{ch_name or 'DM'} from {message.author}: {message.content[:60]}", flush=True)

    if not (is_target_channel or is_dm):
        print(f"[*] Ignored message (channel #{ch_name} doesn't match target '{target_channel}')", flush=True)
        await bot.process_commands(message)
        return
        
    content_lower = message.content.strip().lower()

    # Discord Commands: export or sync
    if content_lower in ["!curio export", "export", "!export"]:
        if os.path.exists(INBOX_FILE):
            inbox_count = len(load_inbox().get("items", []))
            await message.reply(
                f"📦 **Here is your CURIO Inbox backup ({inbox_count} items)!**\n"
                f"You can import this directly into CURIO on your phone or PC via **Import JSON**.",
                file=discord.File(INBOX_FILE, filename="curio_inbox.json")
            )
        else:
            await message.reply("Inbox is currently empty.")
        return

    if content_lower in ["!curio sync", "sync", "!sync"]:
        msg = await message.reply("🔄 Pushing catalog to GitHub...")
        if CLOUD_MODE:
            success = await github_api_push(load_inbox(), "Manual sync command")
        else:
            success = await asyncio.to_thread(git_sync_push, "Manual sync command")
        if success:
            await msg.edit(content="✅ **Successfully synced to GitHub!** You can now tap **Sync** on your phone.")
        else:
            await msg.edit(content="⚠️ Could not push to GitHub. Check your git credentials or network.")
        return

    if content_lower in ["!curio clean", "!curio clear", "!clean", "!clear"]:
        inbox = load_inbox()
        orig_count = len(inbox.get("items", []))
        if content_lower in ["!curio clear", "!clear"]:
            inbox["items"] = []
            save_inbox(inbox)
            if CLOUD_MODE:
                await github_api_push(inbox, "Clear inbox queue")
            else:
                await asyncio.to_thread(git_sync_push, "Clear inbox queue")
            await message.reply(f"🧹 **Cleared all {orig_count} items from CURIO inbox queue.**")
            return
        else:
            # Clean invalid / duplicate items
            cleaned = []
            seen_links = set()
            for it in inbox.get("items", []):
                lnk = it.get("link", "")
                tit = it.get("title", "").strip()
                if not lnk or lnk in seen_links:
                    continue
                if any(x in lnk for x in ["discord.com/channels/", "discord.com/attachments/", "discord.gg/"]):
                    continue
                if tit in ["- YouTube", "YouTube"] or tit == lnk:
                    slug_parts = [p for p in lnk.split("/") if p and not p.startswith("http") and "." not in p]
                    it["title"] = slug_parts[-1].replace("-", " ").replace("_", " ").title() if slug_parts else tit
                seen_links.add(lnk)
                cleaned.append(it)
            inbox["items"] = cleaned
            save_inbox(inbox)
            if CLOUD_MODE:
                await github_api_push(inbox, "Cleaned inbox queue")
            else:
                await asyncio.to_thread(git_sync_push, "Cleaned inbox queue")
            await message.reply(f"✨ **Cleaned inbox:** pruned from {orig_count} down to {len(cleaned)} unique valid items.")
            return

    urls = extract_urls(message.content)
    if not urls:
        await bot.process_commands(message)
        return
        
    try:
        await message.add_reaction("⏳")
    except Exception:
        pass
        
    inbox = load_inbox()
    existing_links = {it.get("link") for it in inbox.get("items", []) if it.get("link")}
    added_items = []
    
    for url in urls:
        if url in existing_links:
            print(f"[*] Skipping duplicate link already in inbox: {url}")
            continue

        print(f"[*] Processing link: {url}")
        meta = await scrape_web_metadata(url)
        curation = await ai_curate(url, meta, config.get("gemini_api_key"), inbox.get("drawers", DEFAULT_DRAWERS))
        
        # Ensure the drawer exists in drawers list
        if curation["drawer"] not in inbox["drawers"]:
            inbox["drawers"].append(curation["drawer"])
            
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        item_id = f"item-discord-{int(time.time()*1000)}"
        
        final_title = curation.get("title") or meta.get("title") or ""
        if not final_title or final_title.startswith("http") or final_title.lower() in ["- youtube", "youtube"]:
            slug_parts = [p for p in url.split("/") if p and not p.startswith("http") and "." not in p]
            final_title = slug_parts[-1].replace("-", " ").replace("_", " ").title() if slug_parts else url

        item = {
            "id": item_id,
            "title": final_title,
            "drawer": curation["drawer"],
            "status": "to-explore",
            "tags": curation["tags"],
            "rating": curation["rating"],
            "notes": curation["notes"],
            "link": url,
            "logo": meta.get("image", ""),
            "gallery": [meta["image"]] if meta.get("image") else [],
            "dateAdded": now_iso,
            "dateModified": now_iso
        }
        
        inbox["items"].append(item)
        existing_links.add(url)
        added_items.append(item)
        
    save_inbox(inbox)
    
    # Auto-push to GitHub repository
    if added_items:
        first_title = added_items[0]["title"]
        if CLOUD_MODE:
            asyncio.create_task(github_api_push(inbox, first_title))
        else:
            asyncio.create_task(asyncio.to_thread(git_sync_push, first_title))

    try:
        await message.remove_reaction("⏳", bot.user)
        await message.add_reaction("✅")
    except Exception:
        pass
        
    # Send confirmation embed back to Discord
    for item in added_items:
        embed = discord.Embed(
            title=f"📥 Curated: {item['title'][:250]}",
            url=item['link'],
            description=item['notes'],
            color=0x06B6D4 # CURIO Cyan
        )
        embed.add_field(name="Drawer", value=f"📁 `{item['drawer']}`", inline=True)
        embed.add_field(name="Rating", value="⭐" * item['rating'], inline=True)
        tags_str = " ".join([f"`#{t}`" for t in item['tags']])
        embed.add_field(name="Tags", value=tags_str or "`#resource`", inline=False)
        if item['logo']:
            embed.set_thumbnail(url=item['logo'])
        embed.set_footer(text=f"CURIO Catalog • Queued: {len(inbox['items'])} • Synced to GitHub")
        await message.reply(embed=embed)

async def cloud_bootstrap_inbox():
    """On cloud startup, fetch existing inbox from GitHub so we don't lose data."""
    github_token = config.get("github_token", "") or os.environ.get("GITHUB_TOKEN", "")
    if not github_token:
        return
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CURIO-Bot"
    }
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(GITHUB_API_URL, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content_b64 = data.get("content", "")
                    content_bytes = base64.b64decode(content_b64)
                    inbox_data = json.loads(content_bytes.decode("utf-8"))
                    save_inbox(inbox_data)
                    count = len(inbox_data.get("items", []))
                    print(f"[Cloud Bootstrap] Loaded {count} existing items from GitHub")
                else:
                    print(f"[Cloud Bootstrap] No existing inbox on GitHub (status {resp.status}), starting fresh")
    except Exception as e:
        print(f"[Cloud Bootstrap] Could not fetch inbox: {e}")

async def main():
    token = config.get("discord_token", "").strip()
    if not token or token == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n" + "!" * 60)
        print(" [ACTION REQUIRED] Discord Bot Token not set!")
        if CLOUD_MODE:
            print(" Set the DISCORD_TOKEN environment variable.")
        else:
            print(f" Please open: {os.path.abspath(CONFIG_FILE)}")
            print(" and paste your Bot Token into the 'discord_token' field.")
        print("!" * 60 + "\n")
        return

    if CLOUD_MODE:
        print("[Mode] CLOUD — using env vars + GitHub API")
        # Fetch existing inbox from GitHub (ephemeral filesystem)
        await cloud_bootstrap_inbox()
        # Start health-check HTTP server (Render needs a port listener)
        await start_local_api(DEFAULT_PORT)
    else:
        print("[Mode] LOCAL — using bot_config.json + git CLI")
        # Start local sync HTTP server in background
        await start_local_api(DEFAULT_PORT)
    
    # Start Discord Bot
    await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
