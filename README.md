# Discord Bot Dashboard – Full-Featured Moderation & Utility Bot

![Discord](https://img.shields.io/badge/Platform-Discord-blue)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20UI-lightgrey)

A **fully-featured Discord bot** with a **web dashboard** for moderation, role management, polls, reminders, announcements, and fun commands. The web UI includes **role assignment**, **live server stats**, and **poll creation & voting**.

---

## Features

- **Moderation**
  - Kick, Ban, Mute
  - Role assignment & removal
  - Anti-spam & filter
- **Utility**
  - Ping, user info, server info
  - Reminders & scheduled announcements
- **Fun**
  - Jokes (not really funny rn but u can edit them if you wanna. Just search "async def joke(ctx):" in bot.py 😉)
- **Web Dashboard**
  - Role management
  - Live server stats (members, online users, bot latency)
  - Poll creation from the dashboard
- Fully responsive **Bootstrap 5** UI
- Easy to extend with more features

---

## Requirements

- Python 3.10+  
- Discord server with bot token  
- Libraries: `discord.py`, `Flask`, `python-dotenv`  
- Modern web browser for dashboard  

---

## Setup Tutorial

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/discord-bot-dashboard.git
cd discord-bot-dashboard
2. Install Python dependencies
pip install -r requirements.txt
```
2. Install Python dependencies
```bash
pip install -r requirements.txt
```

## 3. Edit `.env` file
```txt
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
GUILD_ID=YOUR_SERVER_ID_HERE
```

DISCORD_TOKEN: Your Discord bot token

GUILD_ID: Your Discord server ID (right-click server → “Copy ID”)

NOTE: You got to enable: Presence Intent, Server Members Intent, Message Content Intent. In the bot settings on https://discord.com/developers/applications/

## 4. Run the bot
```bash
python bot.py
```

The bot will connect to Discord

Flask web dashboard will run at http://localhost:5000/

## 5. Access the Dashboard

Open your browser and go to:

http://localhost:5000/

**From the dashboard, you can:**

- Assign roles to members

- Create polls in any channel

- View live server stats

## 6. Optional: Run in the Background

Use a terminal multiplexer like tmux or screen, or deploy to Heroku / VPS for continuous uptime.

## Usage

### Bot Commands (Discord)

| Command | Description |
|---------|-------------|
| `!ping` | Shows bot latency |
| `!userinfo [user]` | Displays user information |
| `!serverinfo` | Displays server information |
| `!kick @user` | Kick a user (requires permission) |
| `!ban @user` | Ban a user (requires permission) |
| `!addrole @user role` | Adds a role to a user |
| `!removerole @user role` | Removes a role from a user |
| `!remind <minutes> <task>` | Sets a reminder for you |
| `!poll <question> <options>` | Creates a poll in Discord |
| `!joke` | Sends a random joke |

### Web Dashboard

| Feature | Description |
|---------|-------------|
| Assign Roles | Select a user and a role from dropdowns and click Assign |
| Create Polls | Enter the Discord **Channel ID**, a question, and comma-separated options; bot posts poll with emoji reactions |
| View Live Stats | See Members, Roles, and Bot latency in milliseconds |



## Contributing

- Fork the repo

- Create a new branch: git checkout -b feature/new-feature

- Commit your changes: git commit -m "Add new feature"

- Push: git push origin feature/new-feature

- Open a Pull Request

---

## Credits

This project was created and maintained by **koki26 / KokilandStudio**.  

Special thanks to:

- [Discord.py](https://discordpy.readthedocs.io/) – For providing the Discord API library  
- [Flask](https://flask.palletsprojects.com/) – For the web dashboard framework  
- [Bootstrap](https://getbootstrap.com/) – For responsive and modern UI design  
- [Python](https://www.python.org/) – For making all of this possible  
- Inspiration from various open-source Discord bots and dashboard projects  

If you use or contribute to this project, please include proper credit.  

---
