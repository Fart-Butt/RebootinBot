import datetime
import logging
from pathlib import Path
from secrets import bot_key, command_prefix, server_rcon_info
import discord
import asyncio
from discord.ext.commands import Bot
from cogs.minecraft_rebooter import MinecraftCrap
from mcrcon import MCRcon
import socket
from library import do_send_message
import subprocess

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

bot = Bot(description="a bot for minecraft", command_prefix=command_prefix, pm_help=False, intents=intents)


@bot.event
async def on_ready():
    log.info('Use this link to invite {}:'.format(bot.user.name))
    log.info('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    log.info('--------')
    log.info('You are running Rebootin Butt 0.1.0')
    log.info('Created by Poop Poop')
    log.info('--------')


async def response_monitor(r):
    if r >= 20:
        # 20 or more no responses from server.
        print('its dead jim')
        subprocess.run(
            ["./home/taffer/minecraft/Valhelsia_SERVER-2.2.10/start.sh"]
        )
        await do_send_message(bot.get_channel(154337182717444096), "I'm rebooting this POS now")
        # lock server in restart mode so monitor does not attempt to start a new instance
        return 2
    else:
        return 0


async def minecraft_server_monitor():
    server_state = 0  # server states: 0= off, 1= on, 2= restarting
    response_counter = 0
    await bot.wait_until_ready()
    log.debug("starting server monitor")
    while not bot.is_closed():
        await asyncio.sleep(10)
        log.debug("running server monitor")
        try:
            with MCRcon(server_rcon_info['ip'], server_rcon_info['password']) as m:
                resp = m.command("/list")
                players = resp.split(": ")[1].split(", ")
                log.debug("found online players: %s" % players)
                if response_counter > 0:
                    response_counter = 0  # reset counter
                    await do_send_message(bot.get_channel(154337182717444096), "The server's back up, nerds")

                server_state = 1
        except Exception:
            if response_counter == 0:
                await do_send_message(bot.get_channel(154337182717444096), "I think the server took a shit")
            response_counter += 1
            log.debug("server offline, counter is %d" % response_counter)
            if not server_state == 2:
                server_state = await response_monitor(response_counter)

bot.add_cog(MinecraftCrap(bot))
socket.setdefaulttimeout(5)
bot.loop.create_task(minecraft_server_monitor())
bot.run(bot_key)
