import login
import fetch
import order
import wait

MC_DIFF = 3
CD_DIFF = 5

def mine_bot():
    print 'Starting mine bot'
    fetch.get_data()
    print fetch.res_avail
    levels = fetch.mines_lvl
    if levels[0] - levels[1] < MC_DIFF:  		# M mine small
        order.init_build('met_mine')
    elif not levels[0] - MC_DIFF == levels[1]:  # C mine small
        order.init_build('cry_mine')
    else:
        if levels[1] - levels[2] > CD_DIFF:	    # D mine small
            order.init_build('deu_mine')
        else:							        # All in ratio
            order.init_build('met_mine')

def main():
    login.login()
    while True:
        mine_bot()
        wait.cycle()

main()


