import re
from bs4 import BeautifulSoup
import login
import wait

base_url = 'http://' + login.uni_url + '/game/index.php?page='
res_avail = []
res_produ = []
res_depot = []
mines_lvl = []
depot_lvl = []
stats_lvl = []

def get_data():
    clear_data()
    get_resources()
    get_res_levels()
    get_stat_levels()

def clear_data():
    del res_avail[:], res_produ[:], res_depot[:]
    del mines_lvl[:], depot_lvl[:], stats_lvl[:]

def get_resources():
    global res_avail, res_produ, res_depot
    soup = navigate_to('overview')
    tooltip = str(soup.find(id='resources'))
    numbers = re.findall('\+?\d*\.?\d+&', tooltip)
    numbers = numbers[:20]
    numbers = [n.replace('&', '') for n in numbers]
    numbers = [n.replace('+', '') for n in numbers]
    numbers = [n.replace('.', '') for n in numbers]
    numbers = map(int, numbers)
    for i in range(0, 12, 4):
        res_avail.append(numbers[i])
        res_depot.append(numbers[i + 1])
        res_produ.append(numbers[i + 2])
    numbers = numbers[12:]
    res_avail.append(numbers[0])
    res_produ.append(numbers[1])


def get_res_levels():
    global mines_lvl, depot_lvl
    soup = navigate_to('resources')
    mines_lvl = list_levels(soup, 'building')
    depot_lvl = list_levels(soup, 'storage')

def get_stat_levels():
    global stats_lvl
    soup = navigate_to('station')
    stats_lvl = list_levels(soup, 'stationbuilding')

def navigate_to(page):
    wait.small()
    if page not in login.browser.geturl():
        login.browser.open(base_url + page)
    html = login.browser.response()
    soup = BeautifulSoup(html)
    return soup

def list_levels(soup, list_id):
    list = str(soup.find(id=list_id).findAll('span', {'class':'level'}))
    levels = re.findall('\d+', list)
    levels = map(int, levels)
    return levels
