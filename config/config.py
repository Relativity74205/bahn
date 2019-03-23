DB_URL = {'url': 'sqlite:///database.db'}

URLS = {'default_plan': '/timetables/v1/plan/',
        'station': '/timetables/v1/station/',
        'betriebsstellen': '/betriebsstellen/v1/betriebsstellen',
        'base': 'https://api.deutschebahn.com',
        'full_changes': '/timetables/v1/fchg/',
        'recent_changes': '/timetables/v1/rchg/'}

bahnhof_dict = {'Köln Hbf': {'abbrev': 'KK', 'eva': '8000207'},
                'Düsseldorf Hbf': {'abbrev': 'KD', 'eva': '8000085'},
                'Duisburg Hbf': {'abbrev': 'EDG', 'eva': '8000086'},
                'Essen Hbf': {'abbrev': 'EE', 'eva': '8000098'},
                'Oberhausen Hbf': {'abbrev': 'EOB', 'eva': '8000286'},
                'Bochum Hbf': {'abbrev': 'EBO', 'eva': '8000041'},
                'Dortmund Hbf': {'abbrev': 'EDO', 'eva': '8000080'},
                'Neuss Hbf': {'abbrev': 'KN', 'eva': '8000274'},
                'Krefeld Hbf': {'abbrev': 'KKR', 'eva': '8000211'},
                'Mülheim (Ruhr) Hbf': {'abbrev': 'EMLR', 'eva': '8000259'},
                'Düsseldorf Flughafen': {'abbrev': 'KDFF', 'eva': '8000082'}}

train_event_keys = {'arrival': 'ar',
                    'departure': 'dp',
                    'line': '@l',
                    'id': '@id',
                    'trip_type': {'para1': 'tl',
                                  'para2': '@t'},
                    'filter_flags': {'para1': 'tl',
                                     'para2': '@f'},
                    'owner': {'para1': 'tl',
                              'para2': '@o'},
                    'train_type': {'para1': 'tl',
                                   'para2': '@c'},
                    'train_number': {'para1': 'tl',
                                     'para2': '@n'},
                    'arrival_line': {'para1': 'ar',
                                     'para2': '@l'},
                    'arrival_datetime': {'para1': 'ar',
                                         'para2': '@pt'},
                    'arrival_platform': {'para1': 'ar',
                                         'para2': '@pp'},
                    'arrival_path': {'para1': 'ar',
                                     'para2': '@ppth'},
                    'arrival_cancellation_time': {'para1': 'ar',
                                                  'para2': '@clt'},
                    'changed_arrival_datetime': {'para1': 'ar',
                                                 'para2': '@ct'},
                    'changed_arrival_platform': {'para1': 'ar',
                                                 'para2': '@cp'},
                    'changed_arrival_path': {'para1': 'ar',
                                             'para2': '@cpth'},
                    'changed_arrival_status': {'para1': 'ar',
                                               'para2': '@cs'},
                    'departure_line': {'para1': 'dp',
                                       'para2': '@l'},
                    'departure_datetime': {'para1': 'dp',
                                           'para2': '@pt'},
                    'departure_platform': {'para1': 'dp',
                                           'para2': '@pp'},
                    'departure_path': {'para1': 'dp',
                                       'para2': '@ppth'},
                    'departure_cancellation_time': {'para1': 'dp',
                                                    'para2': '@clt'},
                    'changed_departure_datetime': {'para1': 'dp',
                                                   'para2': '@ct'},
                    'changed_departure_platform': {'para1': 'dp',
                                                   'para2': '@cp'},
                    'changed_departure_path': {'para1': 'dp',
                                               'para2': '@cpth'},
                    'changed_departure_status': {'para1': 'dp',
                                                 'para2': '@cs'}
                    }


connectionStatus = {'w': 'WAITING',  # This (regular) connection is waiting.
                    'n': 'TRANSITION',  # This (regular) connection CANNOT wait.
                    'a': 'ALTERNATIVE'  # This is an alternative (unplanned) connection that has been introduced as a replacement for one regular connection that cannot wait. The connections "tl" (triplabel) attribute might in this case refer to the replaced connection (or more specifi-cally the trip from that connection). Alternative connections are always waiting (they are re-moved otherwise).
                    }

# t
message_type = {'h': 'HIM',  # A HIM message (generated through the Hafas Information Manager)
                'q': 'QUALITY CHANGE',  # A message about a quality change
                'f': 'FREE',  # A free text message.
                'd': 'CAUSE OF DELAY',  # A message about the cause of a delay.
                'i': 'IBIS',  # An IBIS message (generated from IRIS-AP).
                'u': 'UNASSIGNED IBIS MESSAGE',  # An IBIS message (generated from IRIS-AP) not yet assigned to a train.
                'r': 'DISRUPTION',  # A major disruption.
                'c': 'CONNECTION'  # A connection.
                }

priority = {1: 'HIGH',
            2: 'MEDIUM',
            3: 'LOW',
            4: 'DONE'}

distributorType = {'s': 'CITY',
                   'r': 'REGION',
                   'f': 'LONG DISTANCE',
                   'x': 'OTHER'
                   }

eventStatus = {'p': 'PLANNED',  # The event was planned. This status is also used when the cancellation of an
               # event has been revoked
               'a': 'ADDED',  # The event was added to the planned data (new stop)
               'c': 'CANCELLED'  # The event was canceled(as changedstatus, can apply to planned and added stops)
               }

delaySource = {'L': 'LEIBIT',  # LeiBit / LeiDis.
               'NA': 'RISNE AUT',  # IRIS-NE(automatisch).
               'NM': 'RISNE MAN',  # IRIS-NE(manuell).
               'V': 'VDV',  # Prognosen durch dritte EVU über VDVin.
               'IA': 'ISTP AUT',  # ISTP automatisch
               'IM': 'ISTP MAN',  # ISTP manuell.
               'A': 'AUTOMATIC PROGNOSIS'  # Automatische Prognose durch Prognoseautomat.
               }

filterFlag = {'D': 'EXTERNAL',
              'F': 'LONG_DISTANCE',
              'N': 'REGIONAL',
              'S': 'SBAHN'
              }

# TODO
junction_type = None

# TODO
referenceTripRelation = None
referenceTrip = None
