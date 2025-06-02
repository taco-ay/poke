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

        Pokemon.pokemons[trainer_name] = self

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
                    self.name = "pikachu"

    async def info(self):
        return f"""🧾 Pokémon Bilgisi:
- Adı: {self.name}
- Tipi: {self.type}
- HP: {self.hp}
- Güç: {self.power}
- Defans: {self.defense}
- Hız: {self.speed}
- Ağırlık: {self.weight}
"""

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            if rastgele_sayi(1, 5) == 1:
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
        return f"{self.name} iyileşti! (HP: {eski_hp} → {self.hp}, Güç: {eski_power})"

class Wizard(Pokemon):
    def __init__(self, trainer_name):
        super().__init__(trainer_name)
        self.hp += 40

    async def info(self):
        return "🧙‍♂️ Sihirbaz Pokémon:\n" + await super().info()

class Fighter(Pokemon):
    def __init__(self, trainer_name):
        super().__init__(trainer_name)
        self.power += 20

    async def attack(self, enemy):
        ekstra = rastgele_sayi(0, 5)
        self.power += ekstra
        sonuc = await super().attack(enemy)
        self.power -= ekstra
        return sonuc + f"\n💥 Dövüşçü Pokémon süper saldırı yaptı! Ekstra güç: {ekstra}"

    async def info(self):
        return "🥋 Dövüşçü Pokémon:\n" + await super().info()
