from Character import Character
from Items import Potion, Pokeball
import random
from utils import *

RESULTS = {1 : "Your pokemon wins", 2 : "Wild pokemon wins", 3 : "Trainer run away", 4 : "Wild pokemon caught", 5 : "Battle continues", 6 : "Go back"}

class Battle:
    def __init__(self, trainer_pokemon, wild_pokemon, type_effectiveness):
        self.type_effectiveness = type_effectiveness
        self.trainer_pokemon = trainer_pokemon    
        self.wild_pokemon = wild_pokemon
        
        
    def runBattle(self):
        # start with the choice of the trainer
        res = RESULTS[5]
        count = 0
        while res == RESULTS[5] or res == RESULTS[6]:
            if res == RESULTS[5]:
                print(self.trainer_pokemon.getName() + " HP: " + str(self.trainer_pokemon.getC_HP()))
                print(self.wild_pokemon.getName() + " HP: " + str(self.wild_pokemon.getC_HP()))
            
            # alwyas fight
            res = self.fight()
            count = count + 1
        
        if res == RESULTS[1]:
            result_fight = "starter_win"
            self.wild_pokemon.setC_HP(0.0)
        else:
            result_fight = "starter_lose"
            self.trainer_pokemon.setC_HP(0.0)
            
        return {"fight_results" : result_fight, "n_turns" : count, "starter_final_hp" : self.trainer_pokemon.getC_HP(), "wild_final_hp" : self.wild_pokemon.getC_HP()}
            
    def fight(self):
        # take the random move for both pokemon
        [idx_move_t, move_type_t] = self.getIdxPokemonMove(self.trainer_pokemon)
        [idx_move_w, move_type_w] = self.getIdxPokemonMove(self.wild_pokemon)
        
        effect_t = computeEffectiveness(move_type_t, self.wild_pokemon.getType(), self.type_effectiveness)
        effect_w = computeEffectiveness(move_type_w, self.trainer_pokemon.getType(), self.type_effectiveness)
        
        # check the velocity of the pokemon
        if self.trainer_pokemon.getBaseStats().getSpeed() > self.wild_pokemon.getBaseStats().getSpeed():
            self.trainer_pokemon.useMove(idx_move_t, self.wild_pokemon, effect_t, False)
            if self.wild_pokemon.getC_HP() > 0:
                self.wild_pokemon.useMove(idx_move_w, self.trainer_pokemon, effect_w, False)
            else:
                return RESULTS[1]
        else:
            self.wild_pokemon.useMove(idx_move_w, self.trainer_pokemon, effect_w, False)
            if self.trainer_pokemon.getC_HP() > 0:
                self.trainer_pokemon.useMove(idx_move_t, self.wild_pokemon, effect_t, False)
            else:
                return RESULTS[2]
            
        if self.trainer_pokemon.getC_HP() <= 0:
            return RESULTS[2]
        elif self.wild_pokemon.getC_HP() <= 0:
            return RESULTS[1]
            
        return RESULTS[5]
    
    def getIdxPokemonMove(self, pokemon):
        all_moves = pokemon.getMoves()
        
        idx_move = random.randint(0, len(all_moves) - 1)
        
        return [idx_move, all_moves[idx_move].getType()]
