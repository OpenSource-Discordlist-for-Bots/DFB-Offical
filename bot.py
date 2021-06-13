import discord
from discord.ext import commands

import time
from datetime import timedelta
import contextlib
import io

from static import *
from config import *

# Main Bot begins here

bot = commands.Bot(command_prefix = Config.Prefix, intents=discord.Intents.all())
bot.remove_command('help')
startTime = time.time()

# Events

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Discordlist for Bots'))
    print('-- Discordlist for Bots --')
    print('**************************')
    print(f'Python Version: {platform.python_version()}')
    print('Bot started!')
    print('DFB is now ready to use.')
    print(f'Bot Version: {Bot.Version}')
    print('')
    print('-- System Monitor --')
    print('**************************')
    print(f'CPU Usage: {psutil.cpu_percent()}%')
    print(f'OS: {platform.platform()}')
    print(f'Memory Usage: {psutil.virtual_memory()[2]}% | {format(int(get_ram_usage() / 1024 / 1024))} MB')
    print("**************************")
    print('-- Bot Log --')
    print('')
    print(Messages.OnStarted)


@bot.event
async def on_command_error(ctx, error):
    errorEmbed = discord.Embed(title='An Error occurred', description=f'=> {error}', color=discord.Color.red())
    await ctx.send(embed=errorEmbed)
    print(f'[OnError]: {error}')


@bot.event
async def on_member_join(member):
    rank = discord.utils.get(member.guild.roles, id=768940141498204181)
    await member.add_roles(rank)
    print(f'[OnJoined]: {member} joined, and was given the online role')


@bot.event
async def on_member_remove(member):
    print(f'[OnLeft]: {member} has left the server')


@bot.event
async def on_message_delete(message):
    print(f'[OnMessageDeleted]: Message deleted in {message.channel.name}')


@bot.event
async def on_member_update(after, before):
    if not before.bot:
        return

    if str(before.status) == "offline":
        if str(after.status) == "online":
            print(f'[BotOnOffline]: {before.name} is offline!')

# Events

# -- Help Command --

@bot.command()
async def help(ctx):
    if ctx.author.id == 703944517048598568 or ctx.author.id == 775017772358434817 or ctx.author.id == 705557092802625576:
        em = discord.Embed(
            title="Commands for DFB", color=Colors.dfbColor,
            description="**:gear: Moderation**\n"
                        "- `dfb?<emptyCommand>`\n"
                        "`<emptyDescription>`\n\n"
                        "**:hammer_pick: Utilities**\n"
                        "- `dfb?about`\n"
                        "Lets look some useful information about the bot\n\n"
                        "- `dfb?ping`\n"
                        "Shows you the bot ping\n\n"
                        "- `dfb?info`\n"
                        "Lets look info about the concept of DFB\n\n"
                        "**💻 For Developer**\n"
                        "- `dfb?approve <bot> <owner>`\n"
                        "Approves the mentioned bot\n\n"
                        "- `dfb?decline <bot> <owner> <reason>`\n"
                        "Declines the mentioned bot\n\n"
                        "- `dfb?nproc <bot> <owner>`\n"
                        "The mentioned bot won't be certified 'cause some mistakes!\n\n"
                        "- `dfb?certified <owner> <bot>`\n"
                        "Certifies the mentioned bot\n\n"
                        "- `dfb?slink`\n"
                        "Backup-Link for this Server\n\n"
                        "- `dfb?say <msg>`\n"
                        "Botsay Command\n\n"
                        "- `dfb?embedsay <msg>`\n"
                        "Embedbotsay Command\n\n"
                        "- `dfb?eval <code>`\n"
                        "Eval Command for DFB\n\n"
                        "- `dfb?shutdown`\n"
                        "Shutdowns the Bot\n\n"
                        f"**Offical DFB Server » [Invite](https://discord.gg/9Hq7wqsmJy)**",
        )
        em.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=em)

    else:
        em = discord.Embed(
            title="Commands for DFB", color=Colors.dfbColor,
            description="**:gear: Moderation**\n"
                        "- `dfb?<emptyCommand>`\n"
                        "`<emptyDescription>`\n\n"
                        "**:hammer_pick: Utilities**\n"
                        "- `dfb?about`\n"
                        "Lets look some useful information about the bot\n\n"
                        "- `dfb?ping`\n"
                        "Shows you the bot ping\n\n"
                        "- `dfb?info`\n"
                        "Lets look info about the concept of DFB\n\n"
                        f"**Offical DFB Server » [Invite](https://discord.gg/9Hq7wqsmJy)**",
        )
        em.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=em)

# -- Help Command --


# -- Approve and other Botlist Commands --

@bot.command()
@commands.has_permissions(administrator = True)
async def approve(ctx, bot, owner):
    em = discord.Embed(title='Bot approved', description=f'The Bot {bot} by {owner} was approved by <@{ctx.author.id}>! \n Your Bot is now available on the DFB website!', color=Colors.approveColor)
    await ctx.send(embed=em)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def decline(ctx, arg1, arg2, *, arg3):
    em = discord.Embed(title='Bot declined', description=f'The Bot {arg1} by {arg2} was declined by <@{ctx.author.id}> \n \n**Reason** \n{arg3}', color=discord.Color.red())
    await ctx.send(embed=em)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def proc(ctx, bot, owner):
    em = discord.Embed(title='Bot is in certification process', description=f'The Bot {bot} by {owner} is in cerfification process \n \n', color=Colors.procColor)
    await ctx.send(embed=em)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def nproc(ctx, bot, owner):
    em = discord.Embed(title="Bot won't be certified!", description=f"The Bot {bot} by {owner} won't be certified \n \nSorry {owner} but we found a lot of mistakes. So the bot CANNOT be certified!", color=Colors.procColor)
    await ctx.send(embed=em)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def certified(ctx, owner, bot):
    em = discord.Embed(title='Bot has been certified!', description=f'Hey {owner}! We have something big to say you! Your bot, {bot} was cerified by <@{ctx.author.id}>! \nYou are now a certified bot developer and your bot is one of the featured bots!', color=Colors.certColor)
    await ctx.send(embed=em)
    await ctx.message.delete()

# -- Approve and other Botlist Commands --


# -- Standard Commands --

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong 🏓 {round(bot.latency * 1000)}ms")

# -- Standard Commands --


# -- Only Devs --

@bot.command()
@commands.has_role(768938229259960370)
async def slink(ctx):
    await ctx.send(f"> **__Serverbackup__**: https://discord.new/9rPgS6CncCFA")

@bot.command()
async def shutdown(ctx):
    id = str(ctx.author.id)
    if id == '703944517048598568':
        await ctx.send('Shutting down the bot!')
        await ctx.bot.logout()
    else:
        await ctx.send("You dont have sufficient permmisions to perform this action!")


@bot.command()
@commands.has_role(768938229259960370)
async def eval(ctx, *, code):
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        print(f'[OnEvalError]: {e.__class__.__name__}: {e}')
        await ctx.send(f"```\n{e.__class__.__name__}: {e}```")
        return

    tokenembed = discord.Embed(
        title="Wait, what? :thinking:",
        description="You are trying to get the bot token from me...? Not a good idea!",
        color=discord.Color.red()
    )


    if code == "print(Config.Token)":
        await ctx.send(embed=tokenembed)
        print(Messages.OnToken)
        return

    em = discord.Embed(
        title="Eval",
        description=f'**Input**\n```py\n{code}```\n**Output**```{str_obj.getvalue()}```',
        color=discord.Color.blue())
    await ctx.send(embed=em)



@bot.command()
@commands.has_role(768938229259960370)
async def say(ctx, * , args):
    await ctx.send(args)
    await ctx.message.delete()


@bot.command()
@commands.has_role(768938229259960370)
async def embedsay(ctx, * , args):
    em = discord.Embed(description=args)
    await ctx.send(embed=em)
    await ctx.message.delete()
# -- Only Devs --


# -- Utilities --

@bot.command()
async def about(ctx):
    async with ctx.typing():
        em = discord.Embed(title="About the offical DFB!", color=Colors.dfbColor)
        em.add_field(name=f"CPU Usage {Emote.cpu}", value=f"{psutil.cpu_percent(4)} %", inline=False)
        em.add_field(name=f"Memory Usage {Emote.ram}", value=f"{psutil.virtual_memory()[2]} % | {format(int(get_ram_usage() / 1024 / 1024))} MB", inline=True)
        em.add_field(name=f"Python Version {Emote.python}", value=f"{platform.python_version()}", inline=True)
        em.add_field(name=f"Python Compiler {Emote.pyCompiler}", value=f"{platform.python_compiler()}", inline=False)
        em.add_field(name="Bot Version :tools: ", value=f"{Bot.Version}")
        em.add_field(name=f"Uptime :robot:", value=f'{str(timedelta(seconds=int(round(time.time()-startTime))))}', inline=True)
        em.add_field(name=f"Other Informations {Emote.info}", value=f'OS: {platform.system()} ' f' {platform.release()} \n')
        em.add_field(name=f"Github Repository {Emote.github}", value=f'Main: https://github.com/OpenSource-Discordlist-for-Bots \nOffical DFB-OpenSource: https://github.com/OpenSource-Discordlist-for-Bots/DFB-Offical \nDevelopment Repo: https://github.com/Discordlist-for-Bots/dfbOfficalRewrite', inline=False)
    await ctx.send(embed=em)

# -- Utilities --


bot.run(Config.Token)