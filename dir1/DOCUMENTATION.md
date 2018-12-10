# Module: `dir1`
## File: `__init__.py`
Module with helpers for PokemonAgent class.
## File: `calculate.py`
Module for Pokemon Helpers calculations.
### Function: `calculate_stat`
Calculate the value for a given pokemon statistic.

#### Description
Formula from     https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats
#### Arguments:
- base_val
  - Type: int
  - The pokemon's base statistic value in that statistic.
- ev_val
  - Type: int
  - The pokemon's effort values in that statistic
- level
  - Type: int
  - Pokemon's level
#### Returns:
Value for the statistic

### Function: `calculate_hp_stat`
Calculate the value for a pokemon's Hit Points statistic.

#### Description
Formula from     https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats
#### Arguments:
- base_hp
  - Type: int
  - Base HP statistic.
- ev_val
  - Type: int
  - Pokemon's effort values in hitpoints.
- level
  - Type: int
  - Pokemon's level
#### Returns:
Maximum hitpoints for the pokemon.

### Function: `calculate_spe_range`
Calculate the range for a pokemon's speed.
#### Arguments:
- pokmeon_name
  - Type: str
  - The name of the pokemon for whom the range is being calculated.
#### Returns:
Tuple win min/max speed for this Pokemon

### Function: `generate_all_ev_combinations`
Generate all possible stat investment combinations.
#### Arguments:
_None_
#### Returns:
_None_

### Function: `calc_boost_factor`
Calculate the multiplicative modifier for a pokemon's stat.
#### Arguments:
- pokemon
  - Type: Pokemon
  - The pokemon for whom we are calculating.
- stat
  - Type: str
  - The stat for which we are calculating this for.
#### Returns:
The multiplier to apply to that pokemon's stat.

### Function: `calculate_status_damage`
Calculate the % HP to remove as status damage.
#### Arguments:
- pokemon
  - Type: Pokemon or dict
  - The pokemon that this damage is calculated for. pokemon.status is None if no status, otherwise one of the _STATUS variables in the config.
#### Returns:
Float value for the % Damage it will take from status this turn.

### Function: `calculate_modifier`
Calculate the damage modifier for an attack.

#### Description
Factors in STAB, and type effectiveness.
#### Arguments:
- move
  - Type: dict
  - Information on the move being used.
- attacker
  - Type: Pokemon
  - The pokemon using the attack.
- defender
  - Type: Pokemon
  - The pokemon that is recieving the attack.
#### Returns:
The multipler to apply to the damage.

### Function: `calculate_damage`
Calculate damage of a move.
#### Arguments:
- move
  - Type: dict
  - Information on the move being used.
- attacker
  - Type: Pokemon
  - The pokemon using the attack.
- defender
  - Type: Pokemon
  - The pokemon that is recieving the attack.
#### Returns:
The damage dealt by this move, as well as a flag whether or not
        the attack resulted in a critical hit.

## File: `damage_stats.py`
Class for calculating damage stats for a pokemon.

Based on https://www.smogon.com/smog/issue4/damage_stats
### Function: `boost_modifier`
Calcualte the boost modifier for an attack.
#### Arguments:
- attacker
  - Type: dict or Pokemon
  - Attacking Pokemon with boosts. Must support [] lookup.
- defender
  - Type: dict or Pokemon
  - Defending Pokemon with boosts. Must support [] lookup.
#### Returns:
Calculates the ratio of attacking boosts to defending boosts.

### Class: `DamageStatCalc`
Class to estimate damage taken/given.
### Function: `__init__`
Initialize the calculator.
#### Arguments:
_None_
#### Returns:
_None_

### Function: `calculate_range`
Calculate the damage range for a player's attack.
#### Arguments:
- attacker
  - Type: dict or Pokemon
  - Stats and boosts for attacking Pokemon. Must support [] lookup.
- defender
  - Type: dict or Pokemon
  - Stats and boosts for defending Pokemon. Must support [] lookup.
- move
  - Type: dict
  - Dictionary with attacking move's data
- params
  - Type: dict
  - Dictionary with three required keys, 'atk' and 'def', and 'hp' with the kwargs for the estimate_dmg_val calculations.
#### Returns:
Tuple of damage range possible in the form (min, max)

### Function: `estimate_dmg_val`
Estimate the value of a damage_statistic.
#### Arguments:
- stat_val
  - Type: int
  - The pokemon's base value for this statistic.
- is_hp
  - Type: bool
  - Whether or not we are calculating the HP statisitc.
- is_atk
  - Type: bool
  - Whether or not we are calculating an Attack statistic.
- max_evs
  - Type: bool
  - Whether or not this stat has the maximum number of EVs.
- positive_nature
  - Type: bool
  - Whether or not this stat has a positive nature associated with it.
#### Returns:
Calculated Damage Statistic for the stat in question.

### Function: `find_closest_level`
Find the closest value in the keys to this number.

#### Description
Rounds down, so 215 mathces to 200.
#### Arguments:
- number
  - Type: int
  - The number we are looking for a match for.
#### Returns:
Tuple of closest stat value, and the difference.

### Function: `build_stats`
Build the dictionary for the stat numbers.
#### Arguments:
_None_
#### Returns:
_None_

## File: `pkmn_player_gamestate.py`
Class defining an Engine's Game State.
### Function: `contains_switch`
Determine if switching info contains Switch information.
#### Arguments:
- turn_info
  - Type: list
  - List of event that happened that turn.
#### Returns:
Boolean whether or not a switch happened that turn.

### Class: `PokemonPlayerGameState`
Representation of a player's internal game state.
### Function: `__init__`
Initialize this player's internal game state.
#### Arguments:
_None_
#### Returns:
_None_

### Function: `reset_gamestates`
Reset gamestate values for a new battle.
#### Arguments:
_None_
#### Returns:
_None_

### Function: `init_opp_gamestate`
Initialize the investment data for the opponent's team.
#### Arguments:
- opp_team
  - Type: list
  - List with the opponent's Pokemon.
- opp_active
  - Type: Pokemon
  - Opponent's active Pokemon.
#### Returns:
_None_

### Function: `update_gamestate`
Update internal gamestate for self.
#### Arguments:
- my_gamestate
  - Type: dict
  - PokemonEngine representation of player's position. Should have "active" and "team" keys.
- opp_gamestate
  - Type: dict
  - PokemonEngine representation of opponent's position. Only % HP should be viewable, and has "active" and "team" keys.
#### Returns:
_None_

### Function: `new_info`
Get new info for opponent's game_state.

#### Description
Assumes Species Clause is in effect.
#### Arguments:
- turn_info
  - Type: list
  - What happened on that turn, who took what damage.
- my_id
  - Type: str
  - Name corresponding to the "attacker" or "defender" values of this dict. To know which values the method should be looking at in turn_info.
#### Returns:
_None_

### Function: `update_speed_inference`
Infer speed information from the turn info.
#### Arguments:
- turn_info
  - Type: dict
  - Information on a single event of that turn.
- my_id
  - Type: str
  - Name corresponding to the "attacker" or "defender" values of this dict.
#### Returns:
_None_

### Function: `results_attacking`
Generate possible results for when we are attacking.
#### Arguments:
- turn_info
  - Type: dict
  - Information on a single event of that turn.
#### Returns:
Two lists contianing T/F values of opponent's defense investment.

### Function: `results_defending`
Generate possible results for when we are defending.
#### Arguments:
- turn_info
  - Type: dict
  - Information on a single event of that turn.
#### Returns:
Two lists contianing T/F values of opponent's defense investment.

### Function: `valid_results_atk`
Decide which of potential the potential results are valid given damage dealt.
#### Arguments:
- poke_name
  - Type: str
  - Name of the pokemon in question.
- stat
  - Type: str
  - Name of the statistic that this move's damage is calculated from, defense or special defense.
- dmg_pct
  - Type: float
  - How much % damage was done this turn.
- results
  - Type: list
  - Possible defense investment combinations.
- combinations
  - Type: list
  - T/F values corresponding to the defense investment combinations.
#### Returns:
Subset of the results that are possible given the damage dealt.

### Function: `valid_results_def`
Decide which of potential the potential results are valid given damage dealt.
#### Arguments:
- poke_name
  - Type: str
  - Name of the pokemon in question.
- stat
  - Type: str
  - Name of the statistic that this move's damage is calculated from, defense or special defense.
- dmg_pct
  - Type: float
  - How much % damage was done this turn.
- results
  - Type: list
  - Possible defense investment combinations.
- combinations
  - Type: list
  - T/F values corresponding to the defense investment combinations.
#### Returns:
Subset of the results that are possible given the damage dealt.

### Function: `update_atk_inference`
Update the opponent's defense investment information.
#### Arguments:
- turn_info
  - Type: dict
  - Information on damage dealt this turn.
- results
  - Type: list
  - Possible defense investment combinations.
- combinations
  - Type: list
  - T/F values corresponding to the defense investment combinations.
#### Returns:
_None_

### Function: `update_def_inference`
Update the opponent's attack investment information.
#### Arguments:
- turn_info
  - Type: dict
  - Information on damage dealt this turn.
- results
  - Type: list
  - Possible defense investment combinations.
- combinations
  - Type: list
  - T/F values corresponding to the defense investment combinations.
#### Returns:
_None_

### Function: `__getitem__`
Define [] lookup on this object.
#### Arguments:
- key
  - Type: str
  - Attribute of this object to get.
#### Returns:
Attribute of this object at the key.

### Function: `to_json`
Convert this instance to something the interface can use.
#### Arguments:
_None_
#### Returns:
_None_

## File: `pokemon.py`
Class for a pokemon used by a PokemonAgent.
### Function: `default_boosts`
Generate dictionary with default boost levels.
#### Arguments:
_None_
#### Returns:
_None_

### Function: `default_team_spinda`
Generate a Spinda for these players.
#### Arguments:
_None_
#### Returns:
_None_

### Function: `default_team_floatzel`
Generate a FLoatzel for the player.
#### Arguments:
_None_
#### Returns:
_None_

### Function: `default_team_ivysaur`
Generate an Ivysaur for these players.
#### Arguments:
_None_
#### Returns:
_None_

### Class: `Pokemon`
The pokemon class.
### Function: `__init__`
Initialize a pokemon.

#### Description
Make a new instance of species \<name\> with moves \<moves\> at level \<level\> with nature \<quirky\>
#### Arguments:
- name
  - Type: str
  - String corresponding to value in config.POKEMON_DATA
- moves
  - Type: list
  - List of moves corresponding to moves in config.MOVE_DATA
- level
  - Type: int
  - Level of pokemon to be used in calculations
- nature
  - Type: str
  - Pokemon nature to be used to modify stat values.
- evs
  - Type: dict
  - Dictionary of key/value pairs with EVs for each stat. Key should be stat code, value should be number of EVs.
#### Returns:
_None_

### Function: `set_stats`
Calculate stats for the pokemon.
#### Arguments:
- nature
  - Type: str
  - Nature of the pokemon to modify stats.
- evs
  - Type: dict
  - Dictionary with EVs for this Pokemon.
#### Returns:
_None_

### Function: `effective_stat`
Calculate this pokemon's effective stat after boosts.
#### Arguments:
- stat
  - Type: str
  - Statistic to get the value for.
#### Returns:
Pokemon's stat factoring in boosts and status effects.

### Function: `get`
Extend __getitem__ to have defaults.
#### Arguments:
- key
  - Type: str
  - Attribute of this object to get. default: What to return if there is no such key.
#### Returns:
Value of this object's key, if it exists. If not, return value
        specified in default.

### Function: `__getitem__`
Define [] operating on this object.
#### Arguments:
- key
  - Type: str
  - Attribute of this object to get.
#### Returns:
Value of this object's key.

### Function: `__contains__`
Define 'in' operator on this object.
#### Arguments:
- key
  - Type: str
  - Attribute to theck this object for.
#### Returns:
True if this object has 'key' as an attribute.

### Function: `to_json`
Return JSON serializable version of self.
#### Arguments:
_None_
#### Returns:
_None_

