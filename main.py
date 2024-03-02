import disnake
from disnake.ext import commands


bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all())


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    embed = disnake.Embed(
        title="Новый участник!",
        description=f"{member.name}#{member.discriminator}",
        color=0x008AFF
    )
    embed.set_thumbnail(url=member.author.display_avatar.url)
    await channel.send(embed=embed)
@bot.event
async def on_ready():
    print("Бот готов!")


bot.load_extension('cogs.modals')
bot.load_extension('cogs.clear')
bot.load_extension('cogs.reroll')
bot.run("MTEwMjU3MjMxMzk1NTgwNzI2Mg.GuHuvq.eC_dZUN0gUkIl5C2YYp-wfCffXpmPv-K9w9RBs")
