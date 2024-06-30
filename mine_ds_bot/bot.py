# This example requires the 'message_content' intent.
import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    Channel = client.get_channel(1257086733875417108)
    async for message in Channel.history(limit=200):
        content = message.content # get content
        if content == "Нажми реакцию ✅ если манкрафтер!": # если сообщение уже есть -> просто цепляем проверку по id
            print("Already exist")
        else:   # пишем сообщение
            Text= "Нажми реакцию ✅ если манкрафтер!"
            Moji = await Channel.send(Text)
            await Moji.add_reaction('✅')
@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel(1257086733875417108)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "✅":
      Role = discord.utils.get(user.guild.roles, name="кубы")
      await user.add_roles(Role)

client.run(os.getenv("TOKEN"))

