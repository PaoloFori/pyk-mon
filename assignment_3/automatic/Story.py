from Battle import Battle, RESULTS
from PokemonCenter import PokemonCenter
from PokemonStore import PokemonStore
import random
from utils import *
import copy

class Story():
    def __init__(self, trainer, pokedex, MN, type_effectiveness):
        print("Start the story.")
        self.trainer = trainer
        self.pokemonCenter = PokemonCenter()
        self.pokemonStore = PokemonStore()
        self.pokedex = pokedex
        self.MN = MN
        self.type_effectiveness = type_effectiveness
        
    def automaticExploration(self, n):
        to_save = []
        for i in range(0, n+1):
            c_to_save = dict()
            print("You found a wild pokemon!")
            opponent_id = random.choice(list(self.pokedex.keys()))
            opponent = copy.deepcopy(self.pokedex[opponent_id])
            chooseRandomMoves(opponent, self.MN)
            c_to_save["trainer_pokemon"] = self.trainer.getSquad().getPokemons()[0]
            c_to_save["wild_pokemon"] = copy.deepcopy(opponent)
            print("A " + opponent.getName() + " appeared!")
            battle = Battle(self.trainer.getSquad().getPokemons()[0], opponent, self.type_effectiveness)
            c_dict  = battle.runBattle() 
            for key in c_dict.keys():
                c_to_save[key] = c_dict[key]
            
            to_save.append(c_to_save)

            self.pokemonCenter.healPokemons(self.trainer.getSquad().getPokemons())

        print("Goodbye.")
        
        return to_save
        