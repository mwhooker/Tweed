import time
from supay import Daemon
from tweed import Tweed

def run():
    initial_program_setup()
    daemon = Daemon(name='tweed')
    daemon.start()
    do_tweed_loop()

def stop():
    daemon.stop()


def do_tweed_loop():
    while True:
        tweed.close_friend_gap()
        time.sleep(20)


def initial_program_setup():
    global tweed 
    tweed = Tweed()

def program_cleanup():
    return


def reload_program_config():
    return


if __name__ == '__main__':
    initial_program_setup()
    do_tweed_loop()
