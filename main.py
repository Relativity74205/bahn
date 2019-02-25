import json
import xmltodict
import html
from xml.etree import ElementTree

import BahnAPI as ba
import Timetable as tt

ba = ba.BahnAPI()
tt = tt.Timetable(ba)
test = tt.get_default_plan('Duisburg Hbf', 19, 2, 26, 12)
print(json.dumps(test, indent=4))

#print(ba.get_bahnhof_abbrev('Duisburg Hbf'))
#print(ba.get_eva_number('EDG'))
# test = ba.get_default_plan('8000086', '190226', '12')
# #test = ba.get_full_changes('8000086')
# test_unescape = html.unescape(test.content.decode('utf-8'))
# test_json = xmltodict.parse(test_unescape)
# print(test_json)
# station = test_json['timetable']['@station']
# zug_events = test_json['timetable']['s']
# zug_events_eval = [TimetableObject.eval_default_plan(e, station) for e in zug_events]
# print(json.dumps(zug_events_eval, indent=4))
#
# # for i, e in enumerate(zug_events):
# #     print(f"{i}: {json.dumps(e)}")
