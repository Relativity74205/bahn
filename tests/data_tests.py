event_ar = {"@id": "-1489180622575952321-1901232217-17", "tl": {"@f": "S", "@t": "p", "@o": "800337", "@c": "S", "@n": "30288"}, "ar": {"@pt": "1901232327", "@pp": "1", "@l": "2", "@ppth": "Dortmund Hbf|Dortmund-Dorstfeld|Dortmund-Wischlingen|Dortmund-Huckarde|Dortmund-Westerfilde|Dortmund-Nette/Oestrich|Dortmund-Mengede|Castrop-Rauxel Hbf|Herne|Wanne-Eickel Hbf|Gelsenkirchen Hbf|Essen-Zollverein Nord|Essen-Altenessen|Essen-Bergeborbeck|Essen-Dellwig|Oberhausen Hbf"}}
event_dp = {"@id": "1153913907484823289-1901232321-1", "tl": {"@f": "N", "@t": "p", "@o": "800337", "@c": "RB", "@n": "31990"}, "dp": {"@pt": "1901232321", "@pp": "1", "@l": "37", "@ppth": "Duisburg-Wedau|Duisburg-Bissingheim|Duisburg Entenfang"}}
event_ar_dp = {"@id": "-5671486202462405482-1901232245-3", "tl": {"@f": "D", "@t": "p", "@o": "R2", "@c": "ERB", "@n": "89901"}, "ar": {"@pt": "1901232303", "@pp": "10", "@l": "RE3", "@ppth": "D\u00fcsseldorf Hbf|D\u00fcsseldorf Flughafen"}, "dp": {"@pt": "1901232310", "@pp": "10", "@l": "RE3", "@ppth": "Oberhausen Hbf|Essen-Altenessen|Gelsenkirchen Hbf|Wanne-Eickel Hbf|Herne|Castrop-Rauxel Hbf|Dortmund-Mengede|Dortmund Hbf"}}

event_ar_parsed = {
    "station": "Duisburg Hbf",
    "type": "S",
    "train_number": "30288",
    "line": "S2",
    "arrival_date": "2019-01-23",
    "arrival_time": "23:27",
    "arrival_platform": "1",
    "arrival_from": "Dortmund Hbf",
    "departure_date": None,
    "departure_time": None,
    "departure_platform": None,
    "departure_to": "Duisburg Hbf"
}
event_dp_parsed = {
        "station": "Duisburg Hbf",
        "type": "RB",
        "train_number": "31990",
        "line": "RB37",
        "arrival_date": None,
        "arrival_time": None,
        "arrival_platform": None,
        "arrival_from": "Duisburg Hbf",
        "departure_date": "2019-01-23",
        "departure_time": "23:21",
        "departure_platform": "1",
        "departure_to": "Duisburg-Wedau"
    }
event_ar_dp_parsed = {
        "station": "Duisburg Hbf",
        "type": "ERB",
        "train_number": "89901",
        "line": "RE3",
        "arrival_date": "2019-01-23",
        "arrival_time": "23:03",
        "arrival_platform": "10",
        "arrival_from": "D\u00fcsseldorf Hbf",
        "departure_date": "2019-01-23",
        "departure_time": "23:10",
        "departure_platform": "10",
        "departure_to": "Oberhausen Hbf"
    }
