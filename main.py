import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name

    if author not in Pokemon.pokemons:
        sınıf = random.randint(1, 3)
        if sınıf == 1:
            pokemon = Pokemon(author)
        elif sınıf == 2:
            pokemon = Fighter(author)
        elif sınıf == 3:
            pokemon = Wizard(author)

        await pokemon.initialize()
        await ctx.send(await pokemon.info())

        if pokemon.image_url:
            embed = discord.Embed()
            embed.set_image(url=pokemon.image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten bir Pokémon’unuz var!")

@bot.command()
async def saldır(ctx, target: discord.Member):
    attacker_name = ctx.author.name
    target_name = target.name

    if attacker_name in Pokemon.pokemons and target_name in Pokemon.pokemons:
        ben = Pokemon.pokemons[attacker_name]
        dusman = Pokemon.pokemons[target_name]

        sonuc = await ben.attack(dusman)
        await ctx.send(sonuc)

        if dusman.hp <= 0:
            await ctx.send(f"💀 {dusman.name} savaş dışı kaldı!")
            iyilesme = dusman.heal()
            await ctx.send(f"🔁 {target_name}'in Pokémon'u iyileştirildi:\n{iyilesme}")

        if ben.hp <= 0:
            await ctx.send(f"💀 {ben.name} da savaş dışı kaldı!")
            iyilesme = ben.heal()
            await ctx.send(f"🔁 {attacker_name}'in Pokémon'u iyileştirildi:\n{iyilesme}")
    else:
        await ctx.send("İki eğitmenin de Pokémon'u olmalı! `!go` komutunu kullan.")

@bot.command()
async def iyileştir(ctx):
    trainer = ctx.author.name
    if trainer in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[trainer]
        mesaj = pokemon.heal()
        await ctx.send(f"🩺 Pokémon iyileştirildi:\n{mesaj}")
    else:
        await ctx.send("Önce bir Pokémon oluşturmalısın! `!go` komutunu kullan.")

bot.run(token)
