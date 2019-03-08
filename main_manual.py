import json
import xmltodict
import html
from xml.etree import ElementTree

import BahnAPI as ba
import Timetable as tt

ba = ba.BahnAPI()
tt = tt.Timetable(ba)
station = 'Duisburg Hbf'
dp = tt.get_timetable_json(station, 19, 2, 27, 22)
print(dp[0])
a = 1

#print(json.dumps(test, indent=4))

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

test = '''<?xml version='1.0' encoding='UTF-8'?>
<timetable station='Duisburg Hbf'>
  <s id="8596623342920653849-1903011637-20">
    <tl f="F" t="p" o="80" c="IC" n="1952"/>
    <ar pt="1903012238" pp="4" ppth="Leipzig Hbf|Wei&#223;enfels|Naumburg(Saale)Hbf|Apolda|Weimar|Erfurt Hbf|Gotha|Eisenach|Bebra|Kassel-Wilhelmsh&#246;he|Warburg(Westf)|Altenbeken|Paderborn Hbf|Lippstadt|Soest|Hamm(Westf)|Dortmund Hbf|Bochum Hbf|Essen Hbf"/>
    <dp pt="1903012241" pp="4" ppth="D&#252;sseldorf Hbf|K&#246;ln Hbf"/>
  </s>
  <s id="6835474460040764971-1903012122-6">
    <tl f="N" t="p" o="800349" c="RE" n="11249"/>
    <ar pt="1903012159" pp="8" l="42" ppth="M&#246;nchengladbach Hbf|Viersen|Krefeld Hbf|Krefeld-Uerdingen|Rheinhausen"/>
    <dp pt="1903012202" pp="8" l="42" ppth="M&#252;lheim(Ruhr)Hbf|Essen Hbf|Gelsenkirchen Hbf|Wanne-Eickel Hbf|Recklinghausen S&#252;d|Recklinghausen Hbf|Marl-Sinsen|Haltern am See"/>
  </s>
  <s id="-331635205007869265-1903012051-16">
    <tl f="N" t="p" o="800301" c="RE" n="10141"/>
    <ar pt="1903012236" pp="12" l="1" ppth="Aachen Hbf|Aachen-Rothe Erde|Stolberg(Rheinl)Hbf|Eschweiler Hbf|Langerwehe|D&#252;ren|Horrem|K&#246;ln-Ehrenfeld|K&#246;ln Hbf|K&#246;ln Messe/Deutz|K&#246;ln-M&#252;lheim|Leverkusen Mitte|D&#252;sseldorf-Benrath|D&#252;sseldorf Hbf|D&#252;sseldorf Flughafen"/>
    <dp pt="1903012238" pp="12" l="1" ppth="M&#252;lheim(Ruhr)Hbf|Essen Hbf|Wattenscheid|Bochum Hbf|Dortmund Hbf|Dortmund-Scharnhorst|Dortmund-Kurl|Kamen-Methler|Kamen|Nordb&#246;gge|Hamm(Westf)"/>
  </s>
  <s id="2175718612520707906-1903012117-17">
    <tl f="S" t="p" o="800337" c="S" n="30286"/>
    <ar pt="1903012227" pp="1" l="2" ppth="Dortmund Hbf|Dortmund-Dorstfeld|Dortmund-Wischlingen|Dortmund-Huckarde|Dortmund-Westerfilde|Dortmund-Nette/Oestrich|Dortmund-Mengede|Castrop-Rauxel Hbf|Herne|Wanne-Eickel Hbf|Gelsenkirchen Hbf|Essen-Zollverein Nord|Essen-Altenessen|Essen-Bergeborbeck|Essen-Dellwig|Oberhausen Hbf"/>
  </s>
  <s id="-6701603224073703776-1903012203-9">
    <tl f="D" t="p" o="R2" c="ERB" n="89900"/>
    <ar pt="1903012250" pp="2" l="RE3" ppth="Dortmund Hbf|Dortmund-Mengede|Castrop-Rauxel Hbf|Herne|Wanne-Eickel Hbf|Gelsenkirchen Hbf|Essen-Altenessen|Oberhausen Hbf"/>
    <dp pt="1903012253" pp="2" l="RE3" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf"/>
  </s>
  <s id="-8488844539277976383-1903011809-10">
    <tl f="F" t="p" o="80" c="ICE" n="552"/>
    <ar pt="1903012247" pp="4" ppth="Berlin Ostbahnhof|Berlin Hbf|Berlin-Spandau|Hannover Hbf|Bielefeld Hbf|Hamm(Westf)|Dortmund Hbf|Bochum Hbf|Essen Hbf"/>
    <dp pt="1903012249" pp="4" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf|K&#246;ln Hbf"/>
  </s>
  <s id="1292350979413584298-1903012145-3">
    <tl f="D" t="p" o="R2" c="ERB" n="89899"/>
    <ar pt="1903012203" pp="10" l="RE3" ppth="D&#252;sseldorf Hbf|D&#252;sseldorf Flughafen"/>
    <dp pt="1903012210" pp="10" l="RE3" ppth="Oberhausen Hbf|Essen-Altenessen|Gelsenkirchen Hbf|Wanne-Eickel Hbf|Herne|Castrop-Rauxel Hbf|Dortmund-Mengede|Dortmund Hbf"/>
  </s>
  <s id="9181013359929896705-1903012048-8">
    <tl f="N" t="p" o="800306" c="RE" n="10637"/>
    <ar pt="1903012212" pp="11" l="6" ppth="K&#246;ln/Bonn Flughafen|K&#246;ln Messe/Deutz|K&#246;ln Hbf|Dormagen|Neuss Hbf|D&#252;sseldorf Hbf|D&#252;sseldorf Flughafen"/>
    <dp pt="1903012215" pp="11" l="6" ppth="M&#252;lheim(Ruhr)Hbf|Essen Hbf|Wattenscheid|Bochum Hbf|Dortmund Hbf|Kamen|Hamm(Westf)|Heessen|Ahlen(Westf)|Neubeckum|Oelde|Rheda-Wiedenbr&#252;ck|G&#252;tersloh Hbf|Isselhorst-Avenwedde|Brackwede|Bielefeld Hbf"/>
  </s>
  <s id="3736117015423388331-1903011751-9">
    <tl f="F" t="p" o="80" c="ICE" n="526"/>
    <ar pt="1903012249" pp="13" ppth="M&#252;nchen Hbf|N&#252;rnberg Hbf|W&#252;rzburg Hbf|Aschaffenburg Hbf|Frankfurt(Main)Hbf|Frankfurt(M) Flughafen Fernbf|K&#246;ln Messe/Deutz Gl.11-12|D&#252;sseldorf Hbf"/>
    <dp pt="1903012251" pp="13" ppth="Essen Hbf|Bochum Hbf|Dortmund Hbf"/>
  </s>
  <s id="3742440961287674842-1903011809-10">
    <tl f="F" t="p" o="80" c="ICE" n="542"/>
    <ar pt="1903012247" pp="4" wings="-8488844539277976383-1903011809" ppth="Berlin Ostbahnhof|Berlin Hbf|Berlin-Spandau|Hannover Hbf|Bielefeld Hbf|Hamm(Westf)|Dortmund Hbf|Bochum Hbf|Essen Hbf"/>
    <dp pt="1903012249" pp="4" wings="-8488844539277976383-1903011809" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf|K&#246;ln Hbf"/>
  </s>
  <s id="-2782820331228224710-1903012037-27">
    <tl f="N" t="p" o="800333" c="RB" n="10392"/>
    <ar pt="1903012224" pp="6" l="33" ppth="Aachen Hbf|Aachen Schanz|Aachen West|Kohlscheid|Herzogenrath|&#220;bach-Palenberg|Geilenkirchen|Lindern|Brachelen|H&#252;ckelhoven-Baal|Erkelenz|Herrath|Wickrath|Rheydt Hbf|M&#246;nchengladbach Hbf|Viersen|Anrath|Forsthaus|Krefeld Hbf|Krefeld-Oppum|Krefeld-Linn|Krefeld-Uerdingen|Krefeld-Hohenbudberg Chempark|Rheinhausen|Rheinhausen Ost|Duisburg-Hochfeld S&#252;d"/>
  </s>
  <s id="-7845869387457096376-1903012036-16">
    <tl f="N" t="p" o="800349" c="RE" n="11244"/>
    <ar pt="1903012158" pp="6" l="42" ppth="M&#252;nster(Westf)Hbf|M&#252;nster-Albachten|B&#246;sensell|Nottuln-Appelh&#252;lsen|Buldern|D&#252;lmen|Sythen|Haltern am See|Marl-Sinsen|Recklinghausen Hbf|Recklinghausen S&#252;d|Wanne-Eickel Hbf|Gelsenkirchen Hbf|Essen Hbf|M&#252;lheim(Ruhr)Hbf"/>
    <dp pt="1903012200" pp="6" l="42" ppth="Rheinhausen|Krefeld-Uerdingen|Krefeld Hbf|Viersen|M&#246;nchengladbach Hbf"/>
  </s>
  <s id="4951073163485216552-1903012221-1">
    <tl f="N" t="p" o="800337" c="RB" n="31988"/>
    <dp pt="1903012221" pp="1" l="37" ppth="Duisburg-Wedau|Duisburg-Bissingheim|Duisburg Entenfang"/>
  </s>
  <s id="6141465498398089617-1903012210-1">
    <tl f="D" t="p" o="N2" c="NWB" n="75122"/>
    <dp pt="1903012210" pp="6" l="RB31" ppth="Rheinhausen|Rumeln|Trompet|Moers|Rheinberg(Rheinl)|Millingen(b Rheinb)|Alpen|Xanten"/>
  </s>
  <s id="7532154069330868321-1903012206-3">
    <tl f="N" t="p" o="800349" c="RE" n="10237"/>
    <ar pt="1903012222" pp="10" l="2" ppth="D&#252;sseldorf Hbf|D&#252;sseldorf Flughafen"/>
    <dp pt="1903012224" pp="10" l="2" ppth="M&#252;lheim(Ruhr)Hbf|Essen Hbf|Gelsenkirchen Hbf|Wanne-Eickel Hbf|Recklinghausen Hbf|Marl-Sinsen|Haltern am See|Sythen|D&#252;lmen|Buldern|Nottuln-Appelh&#252;lsen|B&#246;sensell|M&#252;nster-Albachten|M&#252;nster(Westf)Hbf"/>
  </s>
  <s id="-6259890486057757334-1903012222-6">
    <tl f="N" t="p" o="800349" c="RE" n="11251"/>
    <ar pt="1903012259" pp="8" l="42" ppth="M&#246;nchengladbach Hbf|Viersen|Krefeld Hbf|Krefeld-Uerdingen|Rheinhausen"/>
    <dp pt="1903012302" pp="8" l="42" ppth="M&#252;lheim(Ruhr)Hbf|Essen Hbf|Gelsenkirchen Hbf|Wanne-Eickel Hbf|Recklinghausen S&#252;d|Recklinghausen Hbf|Marl-Sinsen|Haltern am See"/>
  </s>
  <s id="-4807026762141493308-1903012110-15">
    <tl f="N" t="p" o="800349" c="RE" n="10234"/>
    <ar pt="1903012233" pp="3" l="2" ppth="M&#252;nster(Westf)Hbf|M&#252;nster-Albachten|B&#246;sensell|Nottuln-Appelh&#252;lsen|Buldern|D&#252;lmen|Sythen|Haltern am See|Marl-Sinsen|Recklinghausen Hbf|Wanne-Eickel Hbf|Gelsenkirchen Hbf|Essen Hbf|M&#252;lheim(Ruhr)Hbf"/>
    <dp pt="1903012237" pp="3" l="2" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf"/>
  </s>
  <s id="8918669547548118774-1903012153-20">
    <tl f="S" t="p" o="800337" c="S" n="31138"/>
    <ar pt="1903012253" pp="5" l="1" ppth="Dortmund Hbf|Dortmund-Dorstfeld|Dortmund-Dorstfeld S&#252;d|Dortmund Universit&#228;t|Dortmund-Oespel|Dortmund-Kley|Bochum-Langendreer|Bochum-Langendreer West|Bochum Hbf|Bochum-Ehrenfeld|Wattenscheid-H&#246;ntrop|Essen-Eiberg|Essen-Steele Ost|Essen-Steele|Essen Hbf|Essen West|Essen-Frohnhausen|M&#252;lheim(Ruhr)Hbf|M&#252;lheim(Ruhr)Styrum"/>
    <dp pt="1903012255" pp="5" l="1" ppth="Duisburg-Schlenk|Duisburg-Buchholz|Duisburg-Gro&#223;enbaum|Duisburg-Rahm|Angermund|D&#252;sseldorf Flughafen|D&#252;sseldorf-Unterrath|D&#252;sseldorf-Derendorf|D&#252;sseldorf-Zoo|D&#252;sseldorf Wehrhahn|D&#252;sseldorf Hbf|D&#252;sseldorf Volksgarten|D&#252;sseldorf-Oberbilk|D&#252;sseldorf-Eller Mitte|D&#252;sseldorf-Eller|Hilden|Hilden S&#252;d|Solingen Vogelpark|Solingen Hbf"/>
  </s>
  <s id="8939588169016749102-1903012143-20">
    <tl f="S" t="p" o="800337" c="S" n="31139"/>
    <ar pt="1903012237" pp="9" l="1" ppth="Solingen Hbf|Solingen Vogelpark|Hilden S&#252;d|Hilden|D&#252;sseldorf-Eller|D&#252;sseldorf-Eller Mitte|D&#252;sseldorf-Oberbilk|D&#252;sseldorf Volksgarten|D&#252;sseldorf Hbf|D&#252;sseldorf Wehrhahn|D&#252;sseldorf-Zoo|D&#252;sseldorf-Derendorf|D&#252;sseldorf-Unterrath|D&#252;sseldorf Flughafen|Angermund|Duisburg-Rahm|Duisburg-Gro&#223;enbaum|Duisburg-Buchholz|Duisburg-Schlenk"/>
    <dp pt="1903012237" pp="9" l="1" ppth="M&#252;lheim(Ruhr)Styrum|M&#252;lheim(Ruhr)Hbf|Essen-Frohnhausen|Essen West|Essen Hbf|Essen-Steele|Essen-Steele Ost|Essen-Eiberg|Wattenscheid-H&#246;ntrop|Bochum-Ehrenfeld|Bochum Hbf|Bochum-Langendreer West|Bochum-Langendreer|Dortmund-Kley|Dortmund-Oespel|Dortmund Universit&#228;t|Dortmund-Dorstfeld S&#252;d|Dortmund-Dorstfeld|Dortmund Hbf"/>
  </s>
  <s id="-3599056860419824982-1903012044-17">
    <tl f="D" t="p" o="AR" c="ABR" n="20039"/>
    <ar pt="1903012215" pp="2" l="RE19" ppth="Arnhem Centraal|Zevenaar|Emmerich|Praest|Millingen(b Rees)|Empel-Rees|Haldern(Rheinl)|Mehrhoog|Wesel Feldmark|Wesel|Friedrichsfeld(Niederrhein)|Voerde(Niederrhein)|Dinslaken|Oberhausen-Holten|Oberhausen-Sterkrade|Oberhausen Hbf"/>
    <dp pt="1903012216" pp="2" l="RE19" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf"/>
  </s>
  <s id="390871530109954885-1903012217-1">
    <tl f="D" t="p" o="N2" c="NWB" n="91572"/>
    <dp pt="1903012217" pp="3" l="RE10" ppth="Krefeld-Oppum|Krefeld Hbf|Kempen(Niederrhein)|Aldekerk|Nieukerk|Geldern|Kevelaer|Weeze|Goch|Bedburg-Hau|Kleve"/>
  </s>
  <s id="6029799302243282893-1903012201-9">
    <tl f="D" t="p" o="N2" c="NWB" n="75123"/>
    <ar pt="1903012246" pp="8" l="RB31" ppth="Xanten|Alpen|Millingen(b Rheinb)|Rheinberg(Rheinl)|Moers|Trompet|Rumeln|Rheinhausen"/>
  </s>
  <s id="-8661790815112406783-1903012016-19">
    <tl f="N" t="p" o="800305" c="RE" n="28534"/>
    <ar pt="1903012218" pp="13" l="5" ppth="Koblenz Hbf|Koblenz Stadtmitte|Andernach|Bad Breisig|Sinzig(Rhein)|Remagen|Bonn-Bad Godesberg|Bonn UN Campus|Bonn Hbf|Br&#252;hl|K&#246;ln S&#252;d|K&#246;ln Hbf|K&#246;ln Messe/Deutz|K&#246;ln-M&#252;lheim|Leverkusen Mitte|D&#252;sseldorf-Benrath|D&#252;sseldorf Hbf|D&#252;sseldorf Flughafen"/>
    <dp pt="1903012220" pp="13" l="5" ppth="Oberhausen Hbf|Oberhausen-Sterkrade|Oberhausen-Holten|Dinslaken|Voerde(Niederrhein)|Friedrichsfeld(Niederrhein)|Wesel"/>
  </s>
  <s id="-4823698223727131166-1903011749-8">
    <tl f="F" t="p" o="3393" c="THA" n="9473"/>
    <ar pt="1903012201" pp="13" ppth="Paris Nord|Bruxelles Midi|Li&#232;ge-Guillemins|Aachen Hbf|K&#246;ln Hbf|D&#252;sseldorf Hbf|D&#252;sseldorf Flughafen"/>
    <dp pt="1903012203" pp="13" ppth="Essen Hbf|Dortmund Hbf"/>
  </s>
  <s id="7608415713032123239-1903012236-4">
    <tl f="N" t="p" o="800337" c="RB" n="31989"/>
    <ar pt="1903012247" pp="1" l="37" ppth="Duisburg Entenfang|Duisburg-Bissingheim|Duisburg-Wedau"/>
  </s>
  <s id="-6846908653631364088-1903012226-3">
    <tl f="D" t="p" o="AR" c="ABR" n="20040"/>
    <ar pt="1903012243" pp="10" l="RE19" ppth="D&#252;sseldorf Hbf|D&#252;sseldorf Flughafen"/>
    <dp pt="1903012244" pp="10" l="RE19" ppth="Oberhausen Hbf|Oberhausen-Sterkrade|Oberhausen-Holten|Dinslaken|Voerde(Niederrhein)|Friedrichsfeld(Niederrhein)|Wesel|Wesel Feldmark|Mehrhoog|Haldern(Rheinl)|Empel-Rees|Millingen(b Rees)|Praest|Emmerich|Zevenaar|Arnhem Centraal"/>
  </s>
  <s id="-4573949071054960768-1903012121-12">
    <tl f="D" t="p" o="N2" c="NWB" n="91573"/>
    <ar pt="1903012242" pp="11" l="RE10" ppth="Kleve|Bedburg-Hau|Goch|Weeze|Kevelaer|Geldern|Nieukerk|Aldekerk|Kempen(Niederrhein)|Krefeld Hbf|Krefeld-Oppum"/>
  </s>
  <s id="-6673694197880154816-1903012028-20">
    <tl f="N" t="p" o="800306" c="RE" n="10636"/>
    <ar pt="1903012244" pp="5" l="6" ppth="Minden(Westf)|Porta Westfalica|Bad Oeynhausen|L&#246;hne(Westf)|Herford|Bielefeld Hbf|G&#252;tersloh Hbf|Rheda-Wiedenbr&#252;ck|Oelde|Neubeckum|Ahlen(Westf)|Heessen|Hamm(Westf)|Kamen|Dortmund Hbf|Bochum Hbf|Wattenscheid|Essen Hbf|M&#252;lheim(Ruhr)Hbf"/>
    <dp pt="1903012248" pp="5" l="6" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf|Neuss Hbf|Dormagen|K&#246;ln Hbf|K&#246;ln Messe/Deutz|K&#246;ln/Bonn Flughafen"/>
  </s>
  <s id="2804027551570146889-1903012123-20">
    <tl f="S" t="p" o="800337" c="S" n="31136"/>
    <ar pt="1903012223" pp="5" l="1" ppth="Dortmund Hbf|Dortmund-Dorstfeld|Dortmund-Dorstfeld S&#252;d|Dortmund Universit&#228;t|Dortmund-Oespel|Dortmund-Kley|Bochum-Langendreer|Bochum-Langendreer West|Bochum Hbf|Bochum-Ehrenfeld|Wattenscheid-H&#246;ntrop|Essen-Eiberg|Essen-Steele Ost|Essen-Steele|Essen Hbf|Essen West|Essen-Frohnhausen|M&#252;lheim(Ruhr)Hbf|M&#252;lheim(Ruhr)Styrum"/>
    <dp pt="1903012225" pp="5" l="1" ppth="Duisburg-Schlenk|Duisburg-Buchholz|Duisburg-Gro&#223;enbaum|Duisburg-Rahm|Angermund|D&#252;sseldorf Flughafen|D&#252;sseldorf-Unterrath|D&#252;sseldorf-Derendorf|D&#252;sseldorf-Zoo|D&#252;sseldorf Wehrhahn|D&#252;sseldorf Hbf|D&#252;sseldorf Volksgarten|D&#252;sseldorf-Oberbilk|D&#252;sseldorf-Eller Mitte|D&#252;sseldorf-Eller|Hilden|Hilden S&#252;d|Solingen Vogelpark|Solingen Hbf"/>
  </s>
  <s id="-6409669808400248427-1903012116-12">
    <tl f="N" t="p" o="800301" c="RE" n="10142"/>
    <ar pt="1903012220" pp="4" l="1" ppth="Hamm(Westf)|Nordb&#246;gge|Kamen|Kamen-Methler|Dortmund-Kurl|Dortmund-Scharnhorst|Dortmund Hbf|Bochum Hbf|Wattenscheid|Essen Hbf|M&#252;lheim(Ruhr)Hbf"/>
    <dp pt="1903012222" pp="4" l="1" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf|D&#252;sseldorf-Benrath|Leverkusen Mitte|K&#246;ln-M&#252;lheim|K&#246;ln Messe/Deutz|K&#246;ln Hbf|K&#246;ln-Ehrenfeld|Horrem|D&#252;ren|Langerwehe|Eschweiler Hbf|Stolberg(Rheinl)Hbf|Aachen-Rothe Erde|Aachen Hbf"/>
  </s>
  <s id="8790571338720823794-1903011903-17">
    <tl f="D" t="p" o="AR" c="ABR" n="26734"/>
    <ar pt="1903012201" pp="5" l="RE11" ppth="Kassel-Wilhelmsh&#246;he|Hofgeismar|Warburg(Westf)|Willebadessen|Altenbeken|Paderborn Hbf|Lippstadt|Soest|Hamm(Westf)|Kamen|Kamen-Methler|Dortmund Hbf|Bochum Hbf|Wattenscheid|Essen Hbf|M&#252;lheim(Ruhr)Hbf"/>
    <dp pt="1903012207" pp="5" l="RE11" ppth="D&#252;sseldorf Flughafen|D&#252;sseldorf Hbf"/>
  </s>
  <s id="8774020690961627074-1903012211-8">
    <tl f="N" t="p" o="800305" c="RE" n="28537"/>
    <ar pt="1903012244" pp="2" l="5" ppth="Wesel|Friedrichsfeld(Niederrhein)|Voerde(Niederrhein)|Dinslaken|Oberhausen-Holten|Oberhausen-Sterkrade|Oberhausen Hbf"/>
  </s>
  <s id="-3400333582988682192-1903012207-9">
    <tl f="N" t="p" o="800349" c="RE" n="11246"/>
    <ar pt="1903012258" pp="6" l="42" ppth="Haltern am See|Marl-Sinsen|Recklinghausen Hbf|Recklinghausen S&#252;d|Wanne-Eickel Hbf|Gelsenkirchen Hbf|Essen Hbf|M&#252;lheim(Ruhr)Hbf"/>
    <dp pt="1903012300" pp="6" l="42" ppth="Rheinhausen|Krefeld-Uerdingen|Krefeld Hbf|Viersen|M&#246;nchengladbach Hbf"/>
  </s>
  <s id="-1169123823649543597-1903011830-10">
    <tl f="F" t="p" o="80" c="IC" n="2307"/>
    <ar pt="1903012211" pp="4" ppth="Hamburg-Altona|Hamburg Dammtor|Hamburg Hbf|Hamburg-Harburg|Bremen Hbf|Osnabr&#252;ck Hbf|M&#252;nster(Westf)Hbf|Gelsenkirchen Hbf|Essen Hbf"/>
    <dp pt="1903012213" pp="4" ppth="D&#252;sseldorf Hbf|K&#246;ln Hbf|Bonn Hbf|Remagen|Andernach|Koblenz Hbf"/>
  </s>
  <s id="1865767974920281551-1903012235-1">
    <tl f="S" t="p" o="800337" c="S" n="30239"/>
    <dp pt="1903012235" pp="1" l="2" ppth="Oberhausen Hbf|Essen-Dellwig|Essen-Bergeborbeck|Essen-Altenessen|Essen-Zollverein Nord|Gelsenkirchen Hbf|Wanne-Eickel Hbf|Herne|Castrop-Rauxel Hbf|Dortmund-Mengede|Dortmund-Nette/Oestrich|Dortmund-Westerfilde|Dortmund-Huckarde|Dortmund-Wischlingen|Dortmund-Dorstfeld|Dortmund Hbf"/>
  </s>
  <s id="7537395545451740415-1903011728-11">
    <tl f="F" t="p" o="80" c="ICE" n="512"/>
    <ar pt="1903012245" pp="12" ppth="M&#252;nchen Hbf|M&#252;nchen-Pasing|Augsburg Hbf|Ulm Hbf|Stuttgart Hbf|Mannheim Hbf|Frankfurt(M) Flughafen Fernbf|Siegburg/Bonn|K&#246;ln Hbf|D&#252;sseldorf Hbf"/>
    <dp pt="1903012246" pp="12" ppth="Essen Hbf|Gelsenkirchen Hbf|Recklinghausen Hbf|M&#252;nster(Westf)Hbf"/>
  </s>
  <s id="-2579936440583612292-1903012235-1">
    <tl f="N" t="p" o="800333" c="RB" n="10399"/>
    <dp pt="1903012235" pp="6" l="33" ppth="Duisburg-Hochfeld S&#252;d|Rheinhausen Ost|Rheinhausen|Krefeld-Hohenbudberg Chempark|Krefeld-Uerdingen|Krefeld-Linn|Krefeld-Oppum|Krefeld Hbf|Forsthaus|Anrath|Viersen|M&#246;nchengladbach Hbf|Rheydt Hbf|Wickrath|Herrath|Erkelenz|H&#252;ckelhoven-Baal|Brachelen|Lindern|Geilenkirchen|&#220;bach-Palenberg|Herzogenrath|Kohlscheid|Aachen West|Aachen Schanz|Aachen Hbf"/>
  </s>
  <s id="-742913934537156637-1903012113-20">
    <tl f="S" t="p" o="800337" c="S" n="31137"/>
    <ar pt="1903012207" pp="9" l="1" ppth="Solingen Hbf|Solingen Vogelpark|Hilden S&#252;d|Hilden|D&#252;sseldorf-Eller|D&#252;sseldorf-Eller Mitte|D&#252;sseldorf-Oberbilk|D&#252;sseldorf Volksgarten|D&#252;sseldorf Hbf|D&#252;sseldorf Wehrhahn|D&#252;sseldorf-Zoo|D&#252;sseldorf-Derendorf|D&#252;sseldorf-Unterrath|D&#252;sseldorf Flughafen|Angermund|Duisburg-Rahm|Duisburg-Gro&#223;enbaum|Duisburg-Buchholz|Duisburg-Schlenk"/>
    <dp pt="1903012207" pp="9" l="1" ppth="M&#252;lheim(Ruhr)Styrum|M&#252;lheim(Ruhr)Hbf|Essen-Frohnhausen|Essen West|Essen Hbf|Essen-Steele|Essen-Steele Ost|Essen-Eiberg|Wattenscheid-H&#246;ntrop|Bochum-Ehrenfeld|Bochum Hbf|Bochum-Langendreer West|Bochum-Langendreer|Dortmund-Kley|Dortmund-Oespel|Dortmund Universit&#228;t|Dortmund-Dorstfeld S&#252;d|Dortmund-Dorstfeld|Dortmund Hbf"/>
  </s>
</timetable>'''
