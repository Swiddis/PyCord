import asyncio
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Empty, Queue

import discord
from discord.ext import commands, tasks

client = discord.Client()
sessions = {}
message_queue = Queue()
tpe = ThreadPoolExecutor()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def poll_output(subp, message):
    for line in iter(subp.stdout.readline, ''):
        msg = f"{message.author.mention}\n> {line}"
        message_queue.put((message.channel, message.author, line))


async def create_session(message):
    if message.author.id in sessions:
        if sessions[message.author.id].poll() is None:
            await message.channel.send("Session open, close with `>stop`")
            return
    program = message.content[4:].strip()
    if not os.path.isfile(f"./programs/{program}.py"):
        await message.channel.send("Invalid program")
        return
    sessions[message.author.id] = subprocess.Popen(
        f"./venv/scripts/python.exe ./programs/{program}.py",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'
    )
    tpe.submit(
        poll_output,
        sessions[message.author.id],
        message
    )
    await message.channel.send("Session started")


async def remove_session(message):
    if message.author.id not in sessions:
        await message.channel.send("Not in a session, start one with `>run`")
        return
    sessions[message.author.id].kill()
    del sessions[message.author.id]
    await message.channel.send("Session removed")


async def send_to_session(message, content):
    if message.author.id not in sessions:
        await message.channel.send("Not in a session, start one with `>run`")
        return
    if sessions[message.author.id].poll() is None:
        sessions[message.author.id].stdin.write(content + "\n")
        sessions[message.author.id].stdin.flush()
    else:
        await message.channel.send("Process has terminated")


async def check_queue(max_wait=3.0):
    lines = {}
    start = time.time()
    while time.time() - start < max_wait:
        await asyncio.sleep(0.2)
        try:
            channel, author, msg = message_queue.get_nowait()
            if author not in lines:
                lines[author] = ("", channel)
            lines[author] = (lines[author][0] + msg, lines[author][1])
        except Empty:
            for line in lines:
                msg = f"{line.mention}\n> {lines[line][0][:-1]}"
                await lines[line][1].send(msg)
            lines = {}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(">run"):
        await create_session(message)
        await check_queue()
    elif message.content.startswith(">stop"):
        await remove_session(message)
    elif message.content.startswith(">"):
        data = message.content[1:].strip()
        await send_to_session(message, data)
        await check_queue()

with open('token.txt', 'r') as token_file:
    token = token_file.read()
client.run(token)
