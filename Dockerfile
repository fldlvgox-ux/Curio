FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY curio_discord_bot.py .
COPY curio_inbox.json* ./

# Environment variables (set these in your hosting dashboard)
# DISCORD_TOKEN     - Your Discord bot token
# GEMINI_API_KEY    - Google Gemini API key
# GITHUB_TOKEN      - GitHub Personal Access Token (repo scope)
# CHANNEL_NAME      - Discord channel name (default: curio-index)
# PORT              - HTTP port (default: 8765)

CMD ["python", "-u", "curio_discord_bot.py"]
