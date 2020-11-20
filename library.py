from discord.ext.commands import Context, check


def authorized_rebooter():
    def predicate(ctx: Context):
        authorized_roles = [779435362170306621, 405241383385825290, 405414728551366688]
        for i in authorized_roles:
            if ctx.message.author in ctx.guild.get_role(i).members:
                return True
        return False

    return check(predicate)
