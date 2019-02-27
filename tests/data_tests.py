token = 'asd'

bahnhof = 'Duisburg Hbf'
betriebsstelle_response = [{'abbrev': 'EDG', 'name': 'Duisburg Hbf', 'short': 'Duisburg Hbf'}]
bahnhof_abbrev = 'EDG'

eva_number_response_content = b'<stations>\n\n<station name="Duisburg Hbf" eva="8000086" ds100="EDG" db="true" creationts="19-01-14 15:35:34.347"/>\n\n</stations>\n'
eva_number = '8000086'

event_ar = {"@id": "-1489180622575952321-1901232217-17", "tl": {"@f": "S", "@t": "p", "@o": "800337", "@c": "S", "@n": "30288"}, "ar": {"@pt": "1901232327", "@pp": "1", "@l": "2", "@ppth": "Dortmund Hbf|Dortmund-Dorstfeld|Dortmund-Wischlingen|Dortmund-Huckarde|Dortmund-Westerfilde|Dortmund-Nette/Oestrich|Dortmund-Mengede|Castrop-Rauxel Hbf|Herne|Wanne-Eickel Hbf|Gelsenkirchen Hbf|Essen-Zollverein Nord|Essen-Altenessen|Essen-Bergeborbeck|Essen-Dellwig|Oberhausen Hbf"}}
event_dp = {"@id": "1153913907484823289-1901232321-1", "tl": {"@f": "N", "@t": "p", "@o": "800337", "@c": "RB", "@n": "31990"}, "dp": {"@pt": "1901232321", "@pp": "1", "@l": "37", "@ppth": "Duisburg-Wedau|Duisburg-Bissingheim|Duisburg Entenfang"}}
event_ar_dp = {"@id": "-5671486202462405482-1901232245-3", "tl": {"@f": "D", "@t": "p", "@o": "R2", "@c": "ERB", "@n": "89901"}, "ar": {"@pt": "1901232303", "@pp": "10", "@l": "RE3", "@ppth": "D\u00fcsseldorf Hbf|D\u00fcsseldorf Flughafen"}, "dp": {"@pt": "1901232310", "@pp": "10", "@l": "RE3", "@ppth": "Oberhausen Hbf|Essen-Altenessen|Gelsenkirchen Hbf|Wanne-Eickel Hbf|Herne|Castrop-Rauxel Hbf|Dortmund-Mengede|Dortmund Hbf"}}

event_ar_parsed = {
    "station": "Duisburg Hbf",
    "train_type": "S",
    "train_number": "30288",
    "line": "S2",
    "planed_arrival_date": "2019-01-23",
    "planed_arrival_time": "23:27",
    "planed_arrival_platform": "1",
    "planed_arrival_from": "Dortmund Hbf",
    "planed_departure_date": None,
    "planed_departure_time": None,
    "planed_departure_platform": None,
    "planed_departure_to": "Duisburg Hbf"
}
event_dp_parsed = {
        "station": "Duisburg Hbf",
        "train_type": "RB",
        "train_number": "31990",
        "line": "RB37",
        "planed_arrival_date": None,
        "planed_arrival_time": None,
        "planed_arrival_platform": None,
        "planed_arrival_from": "Duisburg Hbf",
        "planed_departure_date": "2019-01-23",
        "planed_departure_time": "23:21",
        "planed_departure_platform": "1",
        "planed_departure_to": "Duisburg Entenfang"
    }
event_ar_dp_parsed = {
        "station": "Duisburg Hbf",
        "train_type": "ERB",
        "train_number": "89901",
        "line": "RE3",
        "planed_arrival_date": "2019-01-23",
        "planed_arrival_time": "23:03",
        "planed_arrival_platform": "10",
        "planed_arrival_from": "D\u00fcsseldorf Hbf",
        "planed_departure_date": "2019-01-23",
        "planed_departure_time": "23:10",
        "planed_departure_platform": "10",
        "planed_departure_to": "Dortmund Hbf"
    }
