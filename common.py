from secrets import command_prefix
from discord.ext.commands import Bot
import discord

intents = discord.Intents.default()
intents.members = True

bot = Bot(description="a bot for minecraft", command_prefix=command_prefix, pm_help=False, intents=intents)
