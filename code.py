import aiohttp
import asyncio
import random

class Pokemon:
    pokemons = {}

    def __init__(self, trainer_name):
        self.trainer_name = trainer_name
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.image_url = None
        self.hp = None
        self.attack = None
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
                    self.hp = data['stats'][0]['base_stat']
                    self.attack = data['stats'][1]['base_stat']
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
- Atak: {self.attack}
- Defans: {self.defense}
- Hız: {self.speed}
- Ağırlık: {self.weight}
- Resim URL: {self.image_url}
"""

# Ana çalışma bloğu
if __name__ == "__main__":
    async def main():
        x = Pokemon("Ash")
        await x.initialize()
        print(x.info())
    
    asyncio.run(main())
