import operator
import fetch

INDEXES = {'met_mine': 0, 'cry_mine': 1, 'deu_mine': 2, 'ene_mine': 3, 'met_depot': 4, 'cry_depot': 5, 'deu_depot': 6}
MINE_BUTTONS = {'met_mine': 'button1', 'cry_mine': 'button2', 'deu_mine': 'button3', 'ene_mine': 'button4'}
DEPOT_BUTTONS = {'met_depot': 'button7', 'cry_depot': 'button8', 'deu_depot': 'button9'}
MET_BASE_COST = [60, 48, 225, 75, 1000, 1000, 1000]
CRY_BASE_COST = [15, 24, 75, 30, 0, 500, 1000]
DEU_BASE_COST = [0, 0, 0, 0, 0, 0, 0]
ENE_BASE_COST = [10, 10, 20, 0, 0, 0, 0, 0]
COST_FACTOR = [1.5, 1.6, 1.5, 1.5, 2.0, 2.0, 2.0]
UNI_SPEED = 1

def get_page(name):
    if 'mine' in name or 'depot' in name:
        return 'resources'

def get_button(name):
    if 'mine' in name:
        return MINE_BUTTONS[name]
    elif 'depot' in name:
        return DEPOT_BUTTONS[name]

def energy_cost(idx, level):
    next_cost = ENE_BASE_COST[idx] * (level + 1) * pow(1.1, level + 1)
    curr_cost = ENE_BASE_COST[idx] * level * pow(1.1, level)
    return int(next_cost - curr_cost)

def build_cost(name):
    idx = INDEXES[name]
    level = get_level(name, idx)
    met = int(MET_BASE_COST[idx] * pow(COST_FACTOR[idx], level))
    cry = int(CRY_BASE_COST[idx] * pow(COST_FACTOR[idx], level))
    deu = int(DEU_BASE_COST[idx] * pow(COST_FACTOR[idx], level))
    ene = energy_cost(idx, level)
    return [met, cry, deu, ene]

def build_time(name):
    idx = INDEXES[name]
    level = get_level(name, idx)
    met = int(MET_BASE_COST[idx] * pow(COST_FACTOR[idx], level))
    cry = int(CRY_BASE_COST[idx] * pow(COST_FACTOR[idx], level))
    seconds = int(3600 * (met + cry) / (2500 * max(4 - level / 2, 1) * (1 + fetch.stats_lvl[0]) * pow(2, fetch.stats_lvl[5])))
    seconds /= UNI_SPEED
    print 'Finished in %dh %dmin %ds' % (seconds / 3600, seconds % 3600 / 60, seconds % 60)
    return seconds

def when_buildable(costs):
    diff = map(operator.sub, costs, fetch.res_avail)
    prods = [x + 0.1 for x in fetch.res_avail]  # Avoid division by 0
    hours = map(operator.truediv, diff, prods)
    seconds = max(hours) * 3600
    print 'Available in %dh %dmin %ds' % (seconds / 3600, seconds % 3600 / 60, seconds % 60)
    return seconds

def get_level(name, idx):
    if 'mine' in name:
        return fetch.mines_lvl[idx]
    elif 'depot' in name:
        return fetch.depot_lvl[idx - 4]