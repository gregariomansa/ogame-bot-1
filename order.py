from bs4 import BeautifulSoup
import fetch
import wait
import data
import login
import re

def init_build(name):
    print 'Next mine: %s' % name
    page = data.get_page(name)
    fetch.navigate_to(page)
    costs = data.build_cost(name)
    depot = check_storage(costs)
    if depot is None:
        flag = buildable(costs)
        if flag == 1:
            build(name)
        elif flag == 2:
            wait.wait_time = data.when_buildable(costs)
        else:
            costs = data.build_cost('ene_mine')
            if buildable(costs) == 1:
                build('ene_mine')
            else:
                wait.wait_time = data.when_buildable(costs)
    else:
        costs = data.build_cost('deu_depot')
        if buildable(costs) == 1:
            build('deu_depot')
        else:
            wait.wait_time = data.when_buildable(costs)

def buildable(costs):
    resources = fetch.res_avail
    if resources[3] >= costs[3]:
        if resources[0] >= costs[0] and resources[1] >= costs[1] and resources[2] >= costs[2]:
            return 1
        else:
            print 'Not enough resources'
            return 2
    else:
        print 'Not enough energy'
        return 3

def build(name):
    page = data.get_page(name)
    soup = fetch.navigate_to(page)
    if queue_empty(soup):
        button_id = data.get_button(name)
        button = str(soup.find(id=button_id))
        link = re.search('Request\(\'(.+?)\',', button).group(1).replace("amp;","")
        html = login.browser.open(link)
        soup = BeautifulSoup(html)
        button = str(soup.find(id=button_id))
        check = re.search('class="on"', button).group(0)
        if check:
            print 'Building %s' % name
            wait.wait_time = data.build_time(name)
        else:
            print 'Unexpected error'
    else:
        print 'Queue is not empty'

def queue_empty(soup):
    buttons = str(soup.find(id='buttonz'))
    occupied = re.search('timeLink', buttons)
    return not occupied

def check_storage(costs):
    avail = fetch.res_avail
    depot = fetch.res_depot
    if avail[0] >= depot[0] or avail[1] >= depot[1] or avail[2] >= depot[2]:
        print 'Depot limit reached'
        if avail[0] >= depot[0]:
            return 'met_depot'
        elif avail[1] >= depot[1]:
            return 'cry_depot'
        else:
            return 'deu_depot'
    elif costs[0] > depot[0] or costs[1] > depot[1] or costs[2] > depot[2]:
        print 'Not enough depot'
        if costs[0] > depot[0]:
            return 'met_depot'
        elif costs[1] > depot[1]:
            return 'cry_depot'
        else:
            return 'deu_depot'
    else:
        return None
