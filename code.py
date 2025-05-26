import aiohttp
import asyncio
import random

def rastgele_sayi(minimum, maksimum):
    return random.randint(minimum, maksimum)

class Pokemon:
    pokemons = {}

    def __init__(self, trainer_name):
        self.trainer_name = trainer_name
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.image_url = None
        self.hp = rastgele_sayi(100, 200)
        self.power = rastgele_sayi(20, 50)
        self.defense = None
        self.speed = None
        self.weight = None
        self.type = None

        if trainer_name not in Pokemon.pokemons:
            Pokemon.pokemons[trainer_name] = self
        else:
            self = Pokemon.pokemons[trainer_name]

    async def initialize(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['name']
                    self.image_url = data['sprites']['other']['official-artwork']['front_default']
                    self.defense = data['stats'][2]['base_stat']
                    self.speed = data['stats'][5]['base_stat']
                    self.weight = data['weight']
                    self.type = data['types'][0]['type']['name']
                else:
                    self.name = "Pikachu"

    def info(self):
        return f"""🧾 Pokémon Bilgisi:
- Adı: {self.name}
- Tipi: {self.type}
- HP: {self.hp}
- Güç: {self.power}
- Defans: {self.defense}
- Hız: {self.speed}
- Ağırlık: {self.weight}
- Resim URL: {self.image_url}
"""

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = rastgele_sayi(1, 5)
            if chance == 1:
                return f"🛡️ Sihirbaz Pokémon @{enemy.trainer_name}, sihirli kalkan kullandı! Saldırı etkisiz."

        hasar = round(self.power * (1 - enemy.defense / (enemy.defense + 100)))
        if enemy.hp > hasar:
            enemy.hp -= hasar
            return f"⚔️ @{self.trainer_name}, @{enemy.trainer_name}’a {hasar} hasar verdi! Kalan HP: {enemy.hp}"
        else:
            enemy.hp = 0
            return f"🏆 @{self.trainer_name}, @{enemy.trainer_name}’ı yendi!"

    def heal(self):
        eski_hp = self.hp
        eski_power = self.power
        self.hp = rastgele_sayi(100, 200)
        self.power = rastgele_sayi(20, 50)
        return f"🩺 {self.name} iyileştirildi! (HP: {eski_hp} → {self.hp}, Güç: {eski_power} → {self.power})"

class Wizard(Pokemon):
    def __init__(self, trainer_name):
        super().__init__(trainer_name)
        self.hp += 40

    async def attack(self, enemy):
        return await super().attack(enemy)

    def info(self):
        return "🧙‍♂️ Sihirbaz pokémonunuz var.\n" + super().info()

class Fighter(Pokemon):
    def __init__(self, trainer_name):
        super().__init__(trainer_name)
        self.power += 20

    async def attack(self, enemy):
        super_power = rastgele_sayi(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\n💥 Dövüşçü Pokémon süper saldırı kullandı! Ekstra güç: {super_power}"

    def info(self):
        return "🥋 Dövüşçü pokémonunuz var.\n" + super().info()

# 🧪 Savaş Simülasyonu
async def savas_yap(p1, p2):
    print("⚔️ Savaş Başlıyor!\n")
    round_number = 1
    while p1.hp > 0 and p2.hp > 0:
        print(f"--- Raund {round_number} ---")
        result1 = await p1.attack(p2)
        print(result1)
        if p2.hp <= 0:
            print(f"\n🎉 {p1.name} savaşı kazandı!")
            break

        result2 = await p2.attack(p1)
        print(result2)
        if p1.hp <= 0:
            print(f"\n🎉 {p2.name} savaşı kazandı!")
            break

        round_number += 1
        await asyncio.sleep(1)

# 🧬 Pokémon Oluşturma (Süper güç şansını azaltarak)
async def pokemon_olustur(trainer_name):
    chance = random.randint(1, 10)
    if chance <= 6:
        pokemon = Pokemon(trainer_name)
    elif chance <= 8:
        pokemon = Wizard(trainer_name)
    else:
        pokemon = Fighter(trainer_name)
    await pokemon.initialize()
    return pokemon

# Ana Çalışma
if __name__ == "__main__":
    async def main():
        ash = await pokemon_olustur("Ash")
        misty = await pokemon_olustur("Misty")

        print(ash.info())
        print(misty.info())

        await savas_yap(ash, misty)

        # Savaş sonrası iyileştirme
        print("\n🏥 Savaş Sonrası İyileştirme:")
        print(ash.heal())
        print(misty.heal())

    asyncio.run(main())
