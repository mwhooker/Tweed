import time
from supay import Daemon
from tweed import Tweed


 

 def run():
     initial_program_setup()
     daemon = Daemon(name='tweed')
     daemon.start()
     while True:
         do_tweed()
         time.sleep(20)

 def stop():
     daemon.stop()



def do_tweed_loop():
    print "in loop"
    tweed.close_friend_gap()
    

def initial_program_setup():
    print "init"
    global tweed 
    tweed = Tweed()

def program_cleanup():
    return
    

def reload_program_config():
    return
