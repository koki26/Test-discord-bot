import discord
from discord.ext import commands, tasks
import os, asyncio, threading, random
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

reminders = []
scheduled_announcements = []
polls = {}  # poll_msg_id: {question, options, votes: {user:emoji}}

# --- Bot Events ---
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    check_reminders.start()
    check_announcements.start()

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"Welcome {member.mention}! 🎉")

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"{member.name} left 😢")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if any(message.content.count(c) > 10 for c in message.content):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, stop spamming!")
    await bot.process_commands(message)

# --- Moderation Commands ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned!")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.name} got the {role.name} role!")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"{role.name} removed from {member.name}")

# --- Utility Commands ---
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 {round(bot.latency*1000)}ms")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member}'s Info", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles if r.name!="@everyone"]))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"{g.name} Info", color=discord.Color.green())
    embed.add_field(name="Members", value=g.member_count)
    embed.add_field(name="Owner", value=g.owner)
    embed.add_field(name="Created at", value=g.created_at.strftime("%Y-%m-%d"))
    await ctx.send(embed=embed)

# --- Reminders ---
@bot.command()
async def remind(ctx, time: int, *, task):
    remind_time = datetime.now() + timedelta(minutes=time)
    reminders.append((ctx.author, task, remind_time))
    await ctx.send(f"Okay {ctx.author.mention}, I will remind you in {time} minutes!")

@tasks.loop(seconds=60)
async def check_reminders():
    now = datetime.now()
    for r in reminders[:]:
        if now >= r[2]:
            await r[0].send(f"⏰ Reminder: {r[1]}")
            reminders.remove(r)

# --- Scheduled Announcements ---
@tasks.loop(seconds=60)
async def check_announcements():
    now = datetime.now()
    for a in scheduled_announcements[:]:
        if now >= a['time']:
            channel = bot.get_channel(a['channel_id'])
            await channel.send(a['message'])
            scheduled_announcements.remove(a)

# --- Polls ---
@bot.command()
async def poll(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Need at least 2 options!")
        return
    msg = f"**{question}**\n"
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    for i,opt in enumerate(options):
        msg += f"{emojis[i]} - {opt}\n"
    poll_msg = await ctx.send(msg)
    polls[poll_msg.id] = {"question": question, "options": options, "votes": {}}
    for i in range(len(options)):
        await poll_msg.add_reaction(emojis[i])

# --- Fun ---
@bot.command()
async def joke(ctx):
    jokes = ["Why do programmers prefer dark mode? Because light attracts bugs!",
             "I told my computer I needed a break, it said no problem – it needed one too!"]
    await ctx.send(random.choice(jokes))

# --- Web Dashboard ---
app = Flask(__name__)

from flask import render_template

@app.route('/')
def dashboard():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return "Bot is not connected to the server.", 500

    members = [{"id": m.id, "name": m.name, "roles": [r.name for r in m.roles if r.name != "@everyone"]} for m in guild.members]
    roles = [{"id": r.id, "name": r.name} for r in guild.roles if r.name != "@everyone"]

    # Latency in milliseconds
    latency = round(bot.latency * 1000)  # bot.latency is in seconds

    return render_template("dashboard.html", members=members, roles=roles, latency=latency)


@app.route('/')
def index():
    guild = bot.get_guild(GUILD_ID)
    members = [{"id": m.id, "name": m.name, "roles": [r.name for r in m.roles if r.name!="@everyone"]} for m in guild.members]
    roles = [{"id": r.id, "name": r.name} for r in guild.roles if r.name!="@everyone"]
    return render_template("dashboard.html", members=members, roles=roles)

@app.route('/role', methods=['POST'])
def assign_role():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return "Bot is not connected to the server.", 500

    user_id = int(request.form.get('user_id'))
    role_id = int(request.form.get('role_id'))

    member = guild.get_member(user_id)
    if member is None:
        return f"Member with ID {user_id} not found.", 404

    role = guild.get_role(role_id)
    if role is None:
        return f"Role with ID {role_id} not found.", 404

    # Run the coroutine safely
    fut = asyncio.run_coroutine_threadsafe(member.add_roles(role), bot.loop)
    try:
        fut.result(timeout=5)
    except Exception as e:
        return str(e), 500

    return jsonify({"success": True, "message": f"Role {role.name} assigned to {member.name}."})

from flask import request, jsonify

@app.route('/poll', methods=['POST'])
def create_poll():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return jsonify({"error": "Bot not connected"}), 500

    channel_id = request.form.get('channel_id', '').strip()
    question = request.form.get('question', '').strip()
    options = request.form.get('options', '').strip()

    if not channel_id or not question or not options:
        return jsonify({"error": "Channel ID, question, and options are required"}), 400

    try:
        channel_id = int(channel_id)
    except ValueError:
        return jsonify({"error": "Channel ID must be a number"}), 400

    channel = guild.get_channel(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found in this server"}), 404

    options_list = [opt.strip() for opt in options.split(',') if opt.strip()]
    if len(options_list) < 2:
        return jsonify({"error": "Please provide at least 2 options"}), 400

    poll_text = f"📊 **{question}**\n"
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    for i, option in enumerate(options_list):
        if i >= len(emojis):
            break
        poll_text += f"{emojis[i]} {option}\n"

    async def send_poll():
        msg = await channel.send(poll_text)
        for i in range(len(options_list)):
            await msg.add_reaction(emojis[i])
        return msg

    fut = asyncio.run_coroutine_threadsafe(send_poll(), bot.loop)
    try:
        fut.result(timeout=10)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"success": True, "message": f"Poll created successfully in <#{channel_id}>!"})



@app.route('/stats')
def stats():
    guild = bot.get_guild(GUILD_ID)
    online = sum(1 for m in guild.members if m.status!=discord.Status.offline)
    return jsonify({"members": guild.member_count, "online": online, "latency": round(bot.latency*1000)})

def run_web():
    app.run(port=5000)

threading.Thread(target=run_web).start()
bot.run(TOKEN)
