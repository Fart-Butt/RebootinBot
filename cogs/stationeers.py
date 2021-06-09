import logging
import subprocess
from discord.ext.commands import Cog, command
from library import *
from common import bot

logging = logging.getLogger('bot.' + __name__)


class Stationeers(Cog):

    @command()
    @authorized_rebooter_stationeers()
    async def stationeers(self, ctx: Context, *args):
        """reboot - trust authorized rebooter"""
        await do_send_message(bot.get_channel(154337182717444096), "rebooting now")
        subprocess.run(
            ["screen", "-d", "-m", "-S", "stationeers", "/home/taffer/stationeers/resume_mars.sh"]
        )
        print("yes")
        pass
