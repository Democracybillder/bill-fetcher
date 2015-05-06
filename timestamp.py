''' Handles datetime objects'''
import datetime

def is_real_date(date_text, convert=0):
    ''' Checks if date given is real or corrupt, convert string to datetime if needed'''
    try:
        date = datetime.datetime.strptime(str(date_text), '%Y-%m-%d')
        if convert == 1:
            return date
        else:
            return date_text
    except ValueError:
        return None

def clean_bill_dates(bill):
    ''' Makes sure bill is either None or datetime object if needed '''
    bill["status_date"] = is_real_date(bill["status_date"])
    bill["last_action_date"] = is_real_date(bill["last_action_date"])
    return bill
    