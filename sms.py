import datetime

from twilio.rest import Client

SID = 'AC9242730e7817ba318ccf149906f42668'
AUTH_TOKEN = '85b69c06a249e72186ca0b4c8aa8beb7'

cl = Client(SID, AUTH_TOKEN)

body = "It's yo kid bday"


def convert_phone_num_to_valid_format(phone_num):
    phone_num = [c for c in phone_num if str.isdigit(c)]

    if phone_num[0] == '0':
        phone_num[0] = '+381'

    return "".join(phone_num)


def format_date(date_string):
    if isinstance(date_string, datetime.datetime):
        return int(date_string.day), int(date_string.month), int(date_string.year)

    date = date_string.split('.')
    date = [d.strip() for d in date]

    while date.count(''):
        date.remove('')

    if len(date) != 3:
        return None, None, None

    return int(date[0]), int(date[1]), int(date[2])
