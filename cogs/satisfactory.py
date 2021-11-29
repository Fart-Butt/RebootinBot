import logging
import asyncio
import subprocess
from discord.ext.commands import Cog, command, group
from library import *
from common import bot

logging = logging.getLogger('bot.' + __name__)


class Satisfactory(Cog):

    @group(invoke_without_command=True)
    @authorized_rebooter()
    async def satisfactory(self, ctx: Context, *args):
        """reboot - trust authorized rebooter"""

    @satisfactory.command()
    async def reboot(self):
        await do_send_message(bot.get_channel(154337182717444096), "rebooting satisfactory server now")
        subprocess.run(
            ["sudo", "-u", "sfserver", "/home/sfserver/sfserver", "stop"]
        )
        subprocess.run(
            ["sudo", "-u", "sfserver", "/home/sfserver/sfserver", "start"]
        )
        print("yes")
        pass

    @satisfactory.command()
    async def update(self):
        subprocess.run(
            ["sudo", "-u", "sfserver", "/home/sfserver/sfserver", "stop"]
        )
        subprocess.run(
            ["sudo", "-u", "sfserver", "/home/sfserver/sfserver", "validate"]
        )
        subprocess.run(
            ["sudo", "-u", "sfserver", "/home/sfserver/sfserver", "start"]
        )
        pass

    @satisfactory.error
    async def reboot_vote(self, ctx: Context, *args):
        """reboot - vote"""
        await do_send_message(bot.get_channel(154337182717444096), "youre not my real dad")
        print("time to vote lolx")
        pass

    @command()
    @authorized_rebooter()
    async def satistest(self, ctx: Context, *args):
        subprocess.run(
            ["sudo", "-u", "sfserver", "echo", "test"]
        )
