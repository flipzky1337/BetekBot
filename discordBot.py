import os

import discord
from discord import app_commands, Member, VoiceState
from dotenv import load_dotenv

import inMemoryData
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class DiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)


intents = discord.Intents.default()
client = DiscordClient(intents=intents)


@client.event
async def on_ready():
    guild = client.get_guild(int(os.getenv('DISCORD_BETEK_GUILD')))
    vcs = guild.voice_channels

    for vc in vcs:
        inMemoryData.generalChannelData[vc.name] = vc.members

    print(inMemoryData.generalChannelData)


@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    if before.channel is None and after.channel is not None:
        if len(after.channel.members) == 1:
            print(f'{member} has joined {after.channel}')
            inMemoryData.channelData[after.channel.id] = {
                'member': member,
                'time': datetime.datetime.now().strftime("%H:%M"),
                'notified_times': 1
            }
            inMemoryData.messageQueueData.append(f'{member.display_name} присоединился к каналу {after.channel.name}')
        else:
            if after.channel.id in inMemoryData.channelData.keys():
                inMemoryData.channelData.pop(after.channel.id)

        if after.channel.name not in inMemoryData.generalChannelData.keys():
            inMemoryData.generalChannelData[after.channel.name] = []

        inMemoryData.generalChannelData[after.channel.name].append(member)

    if before.channel is not None and after.channel is None:
        if before.channel.id in inMemoryData.channelData.keys():
            inMemoryData.messageQueueData.append(
                f'{member.display_name} не дождался собеседника и покинул канал {before.channel.name}')
            inMemoryData.channelData.pop(before.channel.id)

        if before.channel.name in inMemoryData.generalChannelData.keys():
            inMemoryData.generalChannelData[before.channel.name].remove(member)

    if before.channel is not None and after.channel is not None:
        inMemoryData.generalChannelData[before.channel.name].remove(member)
        inMemoryData.generalChannelData[after.channel.name].append(member)


def init():
    client.run(TOKEN)
