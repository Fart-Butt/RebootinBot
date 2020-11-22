import logging
import asyncio
import subprocess
from discord.ext.commands import Cog, Context, command
from library import *
from common import bot

logging = logging.getLogger('bot.' + __name__)


class MinecraftCrap(Cog):

    @command()
    @authorized_rebooter()
    async def reboot(self, ctx: Context, *args):
        """reboot - trust authorized rebooter"""
        await do_send_message(bot.get_channel(154337182717444096), "rebooting now")
        subprocess.run(
            ["screen", "-d", "-m", "-S", "rebooter", "/home/taffer/minecraft/Valhelsia_SERVER-2.2.10/restart.sh"]
        )
        print("yes")
        pass

    @reboot.error
    async def reboot_vote(self, ctx: Context, *args):
        """reboot - vote"""
        await do_send_message(bot.get_channel(154337182717444096), "youre not my real dad")
        print("time to vote lolx")
        pass

    @command()
    async def test(self, ctx: Context, *args):
        pass
