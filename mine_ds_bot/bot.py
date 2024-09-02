# This example requires the 'message_content' intent.
import discord
import os
from dotenv import load_dotenv

load_dotenv("/home/miha/Documents/practice/mine_ds_bot/.env")
intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    Channel = client.get_channel(1257086733875417108)
    async for message in Channel.history(limit=200):
        content = message.content # get content
        if content == "@everyone Нажми реакцию ✅ чтобы попсать на манкрафт2.0": # если сообщение уже есть -> просто цепляем проверку по id
            print("Already exist")
            return;
        # else:   # пишем сообщение
    Text= "@everyone Нажми реакцию ✅ чтобы попсать на манкрафт2.0"
    Moji = await Channel.send(Text)
    await Moji.add_reaction('✅')


# for cache messages 
# @client.event
# async def on_reaction_add(reaction, user):
#     Channel = client.get_channel(1257086733875417108)
#     # реакцию поставили в нужном канале
#     if reaction.message.channel.id != Channel.id:
#         return
#     if reaction.emoji == "✅":
#       Role = discord.utils.get(user.guild.roles, name="кубы")
#       await user.add_roles(Role)

# for none cache messages
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = payload.member

    join_guild = await client.fetch_guild(payload.guild_id)

    if payload.channel_id != 1257086733875417108:
        return
    
    if str(payload.emoji) == "✅":
        await member.add_roles(join_guild.get_role(1271063922383917086))
    else:
        await message.remove_reaction(payload.emoji, member);

# remove role
@client.event
async def on_raw_reaction_remove(payload):
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id) 
    join_guild = await client.fetch_guild(payload.guild_id)

    if payload.channel_id != 1257086733875417108:
        return
    

    if str(payload.emoji) == "✅":
        await member.remove_roles(join_guild.get_role(1271063922383917086))


client.run(os.getenv("TOKEN"))

