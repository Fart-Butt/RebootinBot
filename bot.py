import datetime
import logging
from pathlib import Path

import secrets
from secrets import bot_key, server_rcon_info
import asyncio
from cogs.minecraft import MinecraftCrap
from cogs.stationeers import Stationeers
from cogs.satisfactory import Satisfactory
from mcrcon import MCRcon
import socket
from library import do_send_message
import subprocess
from common import bot
import os

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


@bot.event
async def on_ready():
    log.info('Use this link to invite {}:'.format(bot.user.name))
    log.info('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    log.info('--------')
    log.info('You are running Rebootin Butt 0.2.0')
    log.info('Created by Poop Poop')
    log.info('--------')


async def response_monitor(r):
    if r >= 20:
        # 20 or more no responses from server.
        print('its dead jim')
        subprocess.run("/home/taffer/minecraft/progress/start.sh", shell=True
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
                reboot_monitor_file = Path("/home/taffer/minecraft/progress/reboot.txt")
                if reboot_monitor_file.exists():
                    # this is likely a scheduled reboot, we will mute the channel message but continue
                    # as normal to catch reboot issues
                    # lets delete the file to acknowledge the reboot
                    log.debug("reboot detected")
                    os.remove("/home/taffer/minecraft/progress/reboot.txt")
                else:
                    # probably not a scheduled reboot
                    log.debug("think the server crashed")
                    await do_send_message(bot.get_channel(154337182717444096), "I think the server took a shit")
            response_counter += 1
            log.debug("server offline, counter is %d" % response_counter)
            if not server_state == 2:
                server_state = await response_monitor(response_counter)


if secrets.minecraft == 1:
    # bot.add_cog(MinecraftCrap(bot))
    bot.loop.create_task(minecraft_server_monitor())
if secrets.stationeers == 1:
    bot.add_cog(Stationeers(bot))
if secrets.satisfactory == 1:
    bot.add_cog(Satisfactory(bot))

socket.setdefaulttimeout(5)
bot.run(bot_key)
