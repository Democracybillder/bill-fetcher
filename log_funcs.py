''' Functions for logging used throughout fetcher code '''

import logging

def logging_data(data):
    ''' Checks if data is corrupt and raises warning to log file if needed '''
    if type(data) != dict or data["status"] != "OK" or len(data) != 2:
        logging.warning('Legiscan data type not dict (type = %s) \
         or data["status"] not "OK" (status = %s) \
         or len(data) not 2 (len(data) = %s)' \
        , type(data), data["status"], len(data))

def logging_bills(bill_list):
    ''' Checks that bill list has data, raises warning to log if doesn't '''
    if len(bill_list) == 0 or type(bill_list) != list:
        logging.warning('bills object not list (type = %s), \
        or len(bills) = 0 (len(bills) = %s)', type(bill_list), len(bill_list))

'''
def log_count_decorate(func):
    ''' Counts how many times a function was called and raises logging if necessary '''
    def wrapper(*args, **kwargs):
        ''' Does the actual work of the decorating function '''
        wrapper.called += 1
        if wrapper.called % 10 == 0:
            logging.info("%s has been called %s times", func, wrapper.called)
            if wrapper.called == 150:
                logging.warning("Abnormal number of words")
        return func(*args, **kwargs)
    wrapper.called = 0
    wrapper.__name__ = func.__name__
    return wrapper
'''

def none_counter(count, total):
    ''' Raises logging if abnormal number of 'None's desgnated for dates using timestamp '''
    print 'none_counter activated'
    ratio = float(count) / float(total)
    if ratio > 0.8:
        logging.error("timestamp designating unfathomable " \
        "ratio of dates as 'None' (ratio = %s)", ratio)
    elif ratio > 0.5:
        logging.warning("timestamp designating abnormal " \
        "ratio of dates as 'None' (ratio = %s)", ratio)
    elif ratio > 0.3:
        logging.info("timestamp has designated a somewhat high " \
        "ratio (ratio of %s) of bills as 'None'", ratio)





