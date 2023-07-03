import datetime
import discord
from discord.ui import Button, View
from discord.ext import commands
import time
import random
import pivnoi_list as p_v
from main import settings


intents = discord.Intents.all()
intents.voice_states = True
bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())


@bot.event
async def on_ready():
    tchk = '.'
    for i in range(3):
        print(tchk, end="")
        time.sleep(1)
    print(f'Авторизован в системе как: [{bot.user.name}], [id:{bot.user.id}]')


@bot.command()
async def menu(ctx):
    button1 = Button(label='Кикнуть', style=discord.ButtonStyle.green, emoji='1️⃣')
    button2 = Button(label='Тайм-аут', style=discord.ButtonStyle.red, emoji='2️⃣')
    button3 = Button(
        label='Профиль VK', style=discord.ButtonStyle.blurple, url='https://vk.com/alexmaslinov', emoji='3️⃣'
                     )

    @bot.event
    async def button_callback(interaction):
        guild = bot.get_guild(settings['serv_id'])
        user = guild.get_member(settings['maslo_id'])
        if user.voice:
            await user.move_to(None)
            await interaction.response.edit_message(content="Маслина ликвидирован!", view=None)

    button1.callback = button_callback    # код до, относится к первой кнопке

    @bot.event
    async def button_callback(interaction):
        guild = bot.get_guild(settings['serv_id'])
        user = guild.get_member(settings['maslo_id'])
        duration = datetime.timedelta(minutes=1)
        if user.voice:
            await user.timeout_for(duration)
            await interaction.response.edit_message(
                content=f"Пользователь {user.mention} отключён на 1 минуту!", view=None
                                                    )

    button2.callback = button_callback   # код до, относится ко второй кнопке

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    await ctx.send(" **```fix\n 💬 Выберите действие относительно Маслины: ```**", view=view)


# @bot.command()
# @commands.has_permissions(kick_members=True)
# async def kick(ctx, member: discord.Member):
#     await member.kick(reason="Reason for kick")
#     await ctx.send(f'{member.mention} был кикнут с сервера.')


@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id == settings['maslo_id']:
        if 'пив' in message.content:
            await message.channel.send(random.choice(p_v.maslina))


bot.run(settings['token'])
