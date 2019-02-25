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
