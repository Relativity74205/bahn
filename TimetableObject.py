import json


def eval_event(zug_event, station):
    zug_event_keys = zug_event.keys()
    event_evaled = dict()
    event_evaled['station'] = station
    event_evaled['type'] = zug_event['tl']['@c']
    event_evaled['train_number'] = zug_event['tl']['@n']
    event_evaled['line'] = get_line(zug_event)

    if 'ar' in zug_event_keys:
        event_evaled['arrival_date'] = get_date(zug_event['ar']['@pt'])
        event_evaled['arrival_time'] = get_time(zug_event['ar']['@pt'])
        event_evaled['arrival_platform'] = zug_event['ar']['@pp']
        event_evaled['arrival_from'] = get_departure_place(zug_event['ar']['@ppth'])
    else:
        event_evaled['arrival_date'] = None
        event_evaled['arrival_time'] = None
        event_evaled['arrival_platform'] = None
        event_evaled['arrival_from'] = station

    if 'dp' in zug_event_keys:
        event_evaled['departure_date'] = get_date(zug_event['dp']['@pt'])
        event_evaled['departure_time'] = get_time(zug_event['dp']['@pt'])
        event_evaled['departure_platform'] = zug_event['dp']['@pp']
        event_evaled['departure_to'] = get_departure_place(zug_event['dp']['@ppth'])
    else:
        event_evaled['departure_date'] = None
        event_evaled['departure_time'] = None
        event_evaled['departure_platform'] = None
        event_evaled['departure_to'] = station

    return event_evaled


def get_departure_place(ppth):
    try:
        return ppth.split('|')[0]
    except IndexError:
        return None


def get_destination_place(ppth):
    try:
        return ppth.split('|')[-1]
    except IndexError:
        return None


def get_time(pt):
    if len(pt) == 10:
        return pt[6:8] + ':' + pt[8:10]
    else:
        return None


def get_date(pt):
    if len(pt) >= 6:
        return '20' + pt[0:2] + '-' + pt[2:4] + '-' + pt[4:6]
    else:
        return None


def get_train_number(number, train_type):
    if number.isdigit():
        return train_type + number
    else:
        return number


def get_line(zug_event):
    zug_event_keys = zug_event.keys()

    if 'ar' in zug_event_keys and '@l' in zug_event['ar'].keys():
        line = str(zug_event['ar']['@l'])
    elif 'dp' in zug_event_keys and '@l' in zug_event['dp'].keys():
        line = str(zug_event['dp']['@l'])
    else:
        line = str(zug_event['tl']['@c']) + str(zug_event['tl']['@n'])

    if line.isdigit():
        return (zug_event['tl']['@c']) + str(line)
    else:
        return line
