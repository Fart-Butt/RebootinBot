import logging
import asyncio
import subprocess
from discord.ext.commands import Cog, Context, command, BucketType
from discord.ext import commands
from library import *
from common import bot
from mcrcon import MCRcon
from secrets import server_rcon_info

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

    @command()
    @commands.cooldown(1, 30, BucketType.guild)
    async def online(self, ctx: Context, *args):
        with MCRcon(server_rcon_info['ip'], server_rcon_info['password']) as m:
            resp = m.command("/list")
            players = resp.split(": ")[1].split(", ")
            if len(players) > 0:
                await do_send_message(bot.get_channel(154337182717444096), "online players: %s" % ", ".join(players))
            else:
                await do_send_message(bot.get_channel(154337182717444096), "no ones home")
