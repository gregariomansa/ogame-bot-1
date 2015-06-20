import random
import time

MIN_MINUTES = 5
MAX_MINUTES = 15
wait_time = 0

def small():
    time.sleep(random.uniform(0.1, 1))

def medium():
    time.sleep(random.uniform(3, 5))

def cycle():
    global wait_time
    if wait_time == 0:
        seconds = random.randint(MIN_MINUTES, MAX_MINUTES) * 60;
    else:
        seconds = wait_time
        wait_time = 0
    print 'Waiting %dh %dmin %ds' % (seconds / 3600, seconds % 3600 / 60, seconds % 60)
    medium()
    while seconds > 0:
        time.sleep(1)
        print 'Next pull in: {}\r'.format(int(seconds)),
        seconds -= 1