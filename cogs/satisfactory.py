import logging
import asyncio
import subprocess
from discord.ext.commands import Cog, command
from library import *
from common import bot

logging = logging.getLogger('bot.' + __name__)


class Satisfactory(Cog):

    @command()
    @authorized_rebooter()
    async def satisfactory(self, ctx: Context, *args):
        """reboot - trust authorized rebooter"""
        await do_send_message(bot.get_channel(154337182717444096), "rebooting satisfactory server now")
        subprocess.run(
            ["sudo", "-u", "sfserver", "/home/sfserver/sfserver", "monitor"]
        )
        print("yes")
        pass

    @satisfactory.error
    async def reboot_vote(self, ctx: Context, *args):
        """reboot - vote"""
        await do_send_message(bot.get_channel(154337182717444096), "youre not my real dad")
        print("time to vote lolx")
        pass
