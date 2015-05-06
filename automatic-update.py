''' To run automatically updating db '''

import fetcher
import threading

def update_db_every_seconds(interval, number):
    '''updates db every number of seconds (float) inputted a specified number
    of times (int)'''
    if number <= 0:
        print "Finished updating DB the specified number of times. (good job me)"
    else:
        fetcher.get_updated_state_bills()
        threading.Timer(interval, update_db_every_seconds, [interval, number-1]).start()
