from discord.ext.commands import Context, check
import asyncio
import random as rand


def authorized_rebooter():
    def predicate(ctx: Context):
        authorized_roles = [779435362170306621, 405241383385825290, 405414728551366688]
        for i in authorized_roles:
            if ctx.message.author in ctx.guild.get_role(i).members:
                return True
        return False

    return check(predicate)

async def do_send_message(channel, message):
    # this shit sends the messages to the peeps
    await asyncio.sleep(2)
    async with channel.typing():
        await asyncio.sleep(rand.randint(2, 5))
        msg = await channel.send(message)  # dont remove await from here or this shit will break
        return msg