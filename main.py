import json
import xmltodict
import html
from xml.etree import ElementTree

import BahnAPI as ba
import TimetableObject

ba = ba.BahnAPI()

print(ba.get_bahnhof_abbrev('Duisburg Hbf'))
print(ba.get_eva_number('EDG'))
# test = ba.get_default_plan('8000086', '190124', '23')
# test_unescape = html.unescape(test.content.decode('utf-8'))
# test_json = xmltodict.parse(test_unescape)
# print(test_json)
# station = test_json['timetable']['@station']
# zug_events = test_json['timetable']['s']
# zug_events_eval = [TimetableObject.eval_event(e, station) for e in zug_events]
#print(json.dumps(zug_events_eval, indent=4))

#for i, e in enumerate(zug_events):
#    print(f"{i}: {json.dumps(e)}")
