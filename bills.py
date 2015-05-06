''' Parsing through bill objects to distill tuples '''
import timestamp
import db

class StateBillsObject(object):
    ''' API bill object parsing class '''

    def __init__(self, raw_data, state):
        ''' get API object to parse '''
        self.raw_data = raw_data
        self.state = state
        self.session_id = raw_data["masterlist"]["session"]["session_id"]
        del raw_data["masterlist"]["session"]
        self.bill_list = raw_data["masterlist"].values()
        self.desc = []
        self.log = []

    def all_state_bills(self):
        ''' Takes state for request object and returns two tuples objects '''
        for bill in self.bill_list:
            bill = clean_bill_dates(bill)
            desc = self.distill_desc(bill, self.state)
            self.desc.append(desc)
            log = distill_log(bill)
            self.log.append(log)
        self.desc, self.log = tuple(self.desc), tuple(self.log)

    def updated_state_bills(self, updated):
        ''' Takes state for request object and db last update and returns
        info since update in two tuples '''
        questionable_bills_desc = []
        for bill in self.bill_list:
            bill = clean_bill_dates(bill)
            bill_date = timestamp.is_real_date(bill["last_action_date"], 1)
            if bill_date > updated:
                log = distill_log(bill)
                self.log.append(log)
                status = bill["status"]
                status_date = timestamp.is_real_date(bill["status_date"], 1)
                if status_date == bill_date:
                    if int(status) == 1: # new bill
                        desc = self.distill_desc(bill, self.state)
                        self.desc.append(desc)
                    else:                # Maybe new bill (questionable)
                        bill_desc = self.distill_desc(bill, self.state)
                        questionable_bills_desc.append(bill_desc)
        self.log = tuple(self.log)
        new_bills = check_questionable_bills(questionable_bills_desc)
        self.desc = tuple(self.desc) + tuple(new_bills)
        '''
        print "inputting %s bills on (%s) % (state, datetime.datetime.now())
        '''

    def distill_desc(self, bill, state):
        '''takes bill and returns billDesc Tuple'''
        bill_desc = {
            "state": state,
            "bill_id":bill["bill_id"],
            "session_id": self.session_id,
            "number": bill["number"],
            "title": bill["title"],
            "description": bill["description"]
            }
        return bill_desc

'''
PROBLEM
def check_questionable_bills(data):
    ''' checks whether each questionable bill already exists in db'''
    new_bills = []
    for bill in data:
        in_db = billdb.get_bill_id(bill["bill_id"])  # not in db => new bill
        if not in_db:
            new_bills.append(bill)
    new_bills = tuple(new_bills)
    return new_bills
'''

def distill_log(bill):
    '''takes bill and returns billLog Tuple'''
    bill_log = {
        "bill_id": bill["bill_id"],
        "status_date": bill["status_date"],
        "status": bill["status"],
        "last_action_date": bill["last_action_date"],
        "last_action": bill["last_action"]
        }
    return bill_log


def clean_bill_dates(bill):
    ''' Makes sure bill is either None or datetime object if needed '''
    bill["status_date"] = timestamp.is_real_date(bill["status_date"])
    bill["last_action_date"] = timestamp.is_real_date(bill["last_action_date"])
    return bill