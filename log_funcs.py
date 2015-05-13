''' Functions for logging used throughout fetcher code '''

import logging

# legiscan content

def bill_data(data):
    ''' Checks if bill data is corrupt and raises warning to log file if needed '''
    if type(data) != dict or data["status"] != "OK" or len(data) != 2:
        logging.warning('Legiscan data type not dict (type = %s) \
         or data["status"] not "OK" (status = %s) \
         or len(data) not 2 (len(data) = %s)' \
        , type(data), data["status"], len(data))

# bill parsing

def has_bills(bill_list):
    ''' Checks that bill list has data, raises warning to log if doesn't '''
    if len(bill_list) == 0 or type(bill_list) != list:
        logging.warning('bills object not list (type = %s), \
        or len(bills) = 0 (len(bills) = %s)', type(bill_list), len(bill_list))

# db access

def log_count_decorate(function):
    ''' Counts how many times a function was called and raises logging if necessary '''
    def wrapped_f(*args, **kwargs):
        ''' Does the actual work '''
        wrapped_f.called += 1
        if function.__name__ == 'modify_one'  and wrapped_f.called > 1:
            logging.error("Database update_log updated more than once during one " \
                "fetcher call, updated %s times", wrapped_f.called)
        elif function.__name__ == 'modify_many' and wrapped_f.called > 2:
            logging.error("Database updated desc and log more than once each during one " \
                "fetcher call, updated %s times", wrapped_f.called)
        elif function.__name__ == 'select':
            if wrapped_f.called > 3000:
                logging.error("Database 'selected' more times than conceivable during one " \
                    "fetcher call, selected %s times", wrapped_f.called)
            elif wrapped_f.called > 1000:
                logging.warning("Database 'selected' suspicious number of times during one " \
                    "fetcher call, selected %s times", wrapped_f.called)
            elif wrapped_f.called > 500:
                logging.info("Database 'selected' many times during one fetcher call, " \
                    "selected %s times", wrapped_f.called)
        return function(*args, **kwargs)
    wrapped_f.called = 0
    wrapped_f.__name__ = function.__name__
    return wrapped_f

# timestamp functionality

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





