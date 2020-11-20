import datetime
import logging
from pathlib import Path
from secrets import bot_key
import discord
from discord.ext.commands import Bot
from cogs.minecraft_rebooter import MinecraftCrap
intents = discord.Intents.default()
intents.members = True
LOGDIR = Path('logs')

def setup_logger() -> logging.Logger:
    """Create and return the master Logger object."""
    LOGDIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    logfile = LOGDIR / f'{timestamp}.log'
    logger = logging.getLogger('bot')  # the actual logger instance
    logger.setLevel(logging.DEBUG)  # capture all log levels
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)  # log levels to be shown at the console
    file_log = logging.FileHandler(logfile)
    file_log.setLevel(logging.DEBUG)  # log levels to be written to file
    formatter = logging.Formatter('{asctime} - {name} - {levelname} - {message}', style='{')
    console_log.setFormatter(formatter)
    file_log.setFormatter(formatter)
    logger.addHandler(console_log)
    logger.addHandler(file_log)
    return logger

log = setup_logger()

bot = Bot(description="a bot for minecraft", command_prefix="&", pm_help=False, intents=intents)

@bot.event
async def on_ready():
    log.info('Use this link to invite {}:'.format(bot.user.name))
    log.info('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    log.info('--------')
    log.info('You are running Rebootin Butt 0.0.1')
    log.info('Created by Poop Poop')
    log.info('--------')

bot.add_cog(MinecraftCrap(bot))
bot.run(bot_key)
