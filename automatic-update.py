''' To run automatically updating db '''

import fetcher
import threading
import logging

def update_db_every_seconds(interval, number):
    '''updates db every number of seconds (float) inputted a specified number
    of times (int)'''
    logging.basicConfig(filename='fetcher.log', level=logging.DEBUG, \
						format='%(asctime)s %(message)s')
    logging.info('Started update_db_every_seconds()')
    if number <= 0:
        logging.info("Finished update_db_every_seconds")
    else:
        fetcher.get_updated_state_bills()
        threading.Timer(interval, update_db_every_seconds, [interval, number-1]).start()

update_db_every_seconds(10, 1)
