DB_URL = {'url': 'sqlite:///database.db'}

URLS = {'default_plan': '/timetables/v1/plan/',
        'station': '/timetables/v1/station/',
        'betriebsstellen': '/betriebsstellen/v1/betriebsstellen',
        'base': 'https://api.deutschebahn.com',
        'full_changes': '/timetables/v1/fchg/',
        'recent_changes': '/timetables/v1/rchg/'}

bahnhof_dict = {'Duisburg Hbf': {'abbrev': 'EDG',
                                 'eva': '8000086'}}

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
                    'departure_line': {'para1': 'dp',
                                       'para2': '@l'},
                    'departure_datetime': {'para1': 'dp',
                                           'para2': '@pt'},
                    'departure_platform': {'para1': 'dp',
                                           'para2': '@pp'},
                    'departure_path': {'para1': 'dp',
                                       'para2': '@ppth'}
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
