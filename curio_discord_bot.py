"""
CURIO — Discord Companion Bot
Automated link collecting, curating, and organizing for CURIO.
100% Free & Local.
"""

import os
import sys
import io
import re
import json
import time
import asyncio
from datetime import datetime, timezone

if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

CONFIG_FILE = "bot_config.json"
INBOX_FILE = "curio_inbox.json"
DEFAULT_PORT = 8765

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
    if not os.path.exists(CONFIG_FILE):
        default_cfg = {
            "discord_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
            "channel_name": "curio-inbox",
            "gemini_api_key": ""
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_cfg, f, indent=2)
        return default_cfg
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

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
    return url_pattern.findall(text)

async def scrape_web_metadata(url):
    """Scrapes OpenGraph and standard HTML metadata from URL."""
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
                    return {"title": url, "description": "", "image": "", "site_name": ""}
                
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
                else:
                    title = url
                    
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
        return {"title": url, "description": "", "image": "", "site_name": ""}

async def ai_curate(url, meta, api_key, available_drawers):
    """Uses Google Gemini free tier to classify drawer, extract tags, and summarize."""
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        # Fallback keyword categorization without AI
        return heuristic_curate(url, meta, available_drawers)
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
You are the AI archivist for CURIO, a game development and digital creator catalog.
Analyze this bookmarked resource:
URL: {url}
Page Title: {meta.get('title', '')}
Site Name: {meta.get('site_name', '')}
Meta Description: {meta.get('description', '')}

Select the best matching Drawer from this list:
{json.dumps(available_drawers)}

Produce a JSON response with:
1. "drawer": The chosen drawer name from the list (or a crisp new 2-4 word category if none fit).
2. "tags": An array of 3 to 6 lowercase alphanumeric tags describing tech, domain, and format (e.g. ["godot", "shader", "open-source", "3d"]).
3. "notes": A clear, informative 2-sentence summary highlighting what this resource is and how a creator/developer would use it.
4. "rating": An integer rating from 3 to 5 based on utility.

Respond ONLY with valid JSON.
"""
        response = None
        for model_name in ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]:
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
        return {
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
    # Tag extraction based on common keywords
    keywords = ["shader", "glsl", "godot", "unity", "unreal", "blender", "audio", "sfx", 
                "synth", "pixel-art", "vector", "svg", "ui", "font", "texture", "3d", "2d", 
                "engine", "open-source", "github", "tutorial", "tool"]
    for kw in keywords:
        if kw in full_text:
            tags.add(kw)
    if not tags:
        tags.add("bookmark")
        
    drawer = "Reference & Docs"
    if any(k in full_text for k in ["shader", "glsl", "hlsl", "vfx"]):
        drawer = "Shaders & Tech Art"
    elif any(k in full_text for k in ["engine", "game dev", "godot", "unity", "unreal", "bevy", "raylib"]):
        drawer = "Game Design & Engines"
    elif any(k in full_text for k in ["audio", "sound", "music", "synth", "vst", "sfx"]):
        drawer = "Audio & Soundtracks"
    elif any(k in full_text for k in ["pixel", "sprite", "animation"]):
        drawer = "Pixel Art & Animation"
    elif any(k in full_text for k in ["vector", "svg", "logo", "icon"]):
        drawer = "Vector & Graphic Design"
    elif any(k in full_text for k in ["paint", "brush", "illustration", "draw"]):
        drawer = "Digital Art & Illustration"
    elif any(k in full_text for k in ["ai", "hdr", "generator", "llm"]):
        drawer = "HDR, Panorama & AI Tools"
        
    notes = meta.get("description") or f"Curated from {url}"
    return {
        "drawer": drawer,
        "tags": list(tags)[:5],
        "notes": notes,
        "rating": 4
    }

def git_sync_push(item_title="Discord update"):
    """Auto-commits and pushes curio_inbox.json to GitHub repository."""
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
    site = web.TCPSite(runner, "127.0.0.1", port)
    await site.start()
    print(f"[API] CURIO Local Sync API running at http://127.0.0.1:{port}/api/inbox")

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
    is_target_channel = (message.channel.name.lower() == target_channel if hasattr(message.channel, "name") else False)
    is_dm = isinstance(message.channel, discord.DMChannel)
    
    if not (is_target_channel or is_dm):
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
        msg = await message.reply("🔄 Pushing local catalog to GitHub...")
        success = await asyncio.to_thread(git_sync_push, "Manual sync command")
        if success:
            await msg.edit(content="✅ **Successfully synced to GitHub!** You can now tap **Sync** on your phone.")
        else:
            await msg.edit(content="⚠️ Could not push to GitHub. Check your git credentials or network.")
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
    added_items = []
    
    for url in urls:
        print(f"[*] Processing link: {url}")
        meta = await scrape_web_metadata(url)
        curation = await ai_curate(url, meta, config.get("gemini_api_key"), inbox.get("drawers", DEFAULT_DRAWERS))
        
        # Ensure the drawer exists in drawers list
        if curation["drawer"] not in inbox["drawers"]:
            inbox["drawers"].append(curation["drawer"])
            
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        item_id = f"item-discord-{int(time.time()*1000)}"
        
        item = {
            "id": item_id,
            "title": meta["title"] or url,
            "drawer": curation["drawer"],
            "status": "to-explore",
            "tags": curation["tags"],
            "rating": curation["rating"],
            "notes": curation["notes"],
            "link": url,
            "logo": meta["image"] or "",
            "gallery": [meta["image"]] if meta["image"] else [],
            "dateAdded": now_iso,
            "dateModified": now_iso
        }
        
        inbox["items"].append(item)
        added_items.append(item)
        
    save_inbox(inbox)
    
    # Auto-push to GitHub repository
    if added_items:
        first_title = added_items[0]["title"]
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

async def main():
    token = config.get("discord_token", "").strip()
    if not token or token == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n" + "!" * 60)
        print(" [ACTION REQUIRED] Discord Bot Token not set!")
        print(f" Please open: {os.path.abspath(CONFIG_FILE)}")
        print(" and paste your Bot Token into the 'discord_token' field.")
        print("!" * 60 + "\n")
        return

    # Start local sync HTTP server in background
    await start_local_api(DEFAULT_PORT)
    
    # Start Discord Bot
    await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
