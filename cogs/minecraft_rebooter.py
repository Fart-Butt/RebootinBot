import logging
import asyncio
import subprocess
from discord.ext.commands import Bot, Cog, Context, command, BucketType
from library import *

logging = logging.getLogger('bot.' + __name__)


class MinecraftCrap(Cog):

    @command()
    @authorized_rebooter()
    async def reboot(self, ctx: Context, *args):
        """reboot - trust authorized rebooter"""
        subprocess.run(
            ["screen -dmS rebooter /home/taffer/minecraft/Valhelsia_SERVER-2.2.10/restart.sh"]
        )
        print("yes")
        pass

    @reboot.error
    async def reboot_vote(self, ctx: Context, *args):
        """reboot - vote"""
        print("time to vote lolx")
        pass


    @command()
    async def test(self, ctx: Context, *args):
        subprocess.run(
            ["screen -dmS rebooter /home/taffer/minecraft/Valhelsia_SERVER-2.2.10/restart.sh"]
        )
