import time
from tweed import Tweed


def do_tweed_loop():
    print "in loop"
    while True:
        tweed.close_friend_gap()
        time.sleep(20)
    

def initial_program_setup():
    tweed = Tweed()

def program_cleanup():
    return
    

def reload_program_config():
    return
