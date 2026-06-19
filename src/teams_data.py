# -*- coding: utf-8 -*-
# Datos reales por equipo: ranking FIFA (11 jun 2026), historial mundialista,
# via de clasificacion. Fuentes: Wikipedia "2026 FIFA World Cup Group X",
# ESPN/Wego FIFA ranking (11 jun 2026), NBC Sports standings (17 jun 2026).

# rank: posicion FIFA al 11-jun-2026 (fuente: blog.wego.com/fifa-world-cup-rankings, ESPN)
RANK = {
"ARG":1,"ESP":2,"FRA":3,"ENG":4,"POR":5,"BRA":6,"MAR":7,"NED":8,"BEL":9,"GER":10,
"CRO":11,"COL":13,"MEX":14,"SEN":15,"URU":16,"USA":17,"JPN":18,"SUI":19,"IRN":20,
"TUR":22,"ECU":23,"AUT":24,"KOR":25,"AUS":27,"ALG":28,"EGY":29,"CAN":30,"NOR":31,
"CIV":33,"PAN":34,"SWE":38,"CZE":40,"PAR":41,"SCO":42,"TUN":45,"COD":46,"UZB":50,
"QAT":56,"IRQ":57,"RSA":60,"KSA":61,"JOR":63,"BIH":64,"CPV":67,"GHA":73,"CUW":82,
"HAI":83,"NZL":85,
}

# Perfil de estilo por equipo (independiente del ranking):
# ATT  = multiplicador ofensivo  (1.0=normal, >1=más goles, <1=menos goles)
# DEF  = multiplicador defensivo (1.0=normal, >1=defensa sólida→rival marca menos, <1=defensa porosa)
# CARD = tendencia a tarjetas    (1.0=normal, >1=más tarjetas, <1=más limpios)
# CORN = tendencia a corners     (1.0=normal, >1=más corners, <1=menos corners)
#
# Criterios reales usados:
# - ATT alta: equipos con atacantes de nivel mundial, historial goleador reciente
# - DEF alta: equipos que conceden pocos goles históricamente en torneos
# - CARD alta: equipos de juego físico o con historial de sanciones en Mundiales
# - CORN alta: equipos con dominio posesional y que centran mucho
STYLE = {
#        ATT   DEF   CARD  CORN
"ARG": (1.30, 1.10, 1.15, 1.05),  # Campeón vigente, Messi, muy agresivo
"ESP": (1.05, 1.20, 0.85, 1.20),  # Posesión, pressing, pocas tarjetas
"FRA": (1.35, 1.10, 1.05, 1.10),  # Mbappé, Dembélé, potencia ofensiva
"ENG": (1.20, 1.15, 1.00, 1.20),  # Kane, centros constantes
"POR": (1.25, 1.05, 1.00, 1.10),  # Ronaldo, Bruno, alta producción ofensiva
"BRA": (1.30, 1.00, 1.10, 1.15),  # Vinícius, Rodrygo, ritmo alto
"MAR": (0.85, 1.40, 1.10, 0.90),  # Bloque bajo, defensa excepcional, pocos corners
"NED": (1.25, 1.00, 1.05, 1.20),  # Gakpo, Depay, muchos centros
"BEL": (1.10, 1.05, 1.00, 1.05),  # De Bruyne, veteranos, efectivos
"GER": (1.35, 0.95, 0.90, 1.25),  # Musiala, Wirtz, muy ofensivos
"CRO": (1.00, 1.10, 1.05, 1.00),  # Modrić, control, equilibrado
"COL": (1.15, 1.00, 1.15, 1.05),  # Luis Díaz, James, enérgico
"MEX": (1.00, 1.05, 1.20, 1.00),  # Presión local, juego físico
"SEN": (1.05, 1.05, 1.20, 1.00),  # Mané, físicos, agresivos
"URU": (0.90, 1.30, 1.25, 0.90),  # Defensa histórica, muy físicos
"USA": (1.05, 1.05, 1.05, 1.05),  # Pulisic, equilibrados como anfitrión
"JPN": (1.05, 1.15, 0.80, 0.95),  # Disciplinados, pocos corners y tarjetas
"SUI": (0.95, 1.20, 0.90, 1.00),  # Sólidos, compactos, poco espectaculares
"IRN": (0.85, 1.25, 1.35, 0.85),  # Bloque defensivo, muy físicos, pocos corners
"TUR": (1.05, 1.00, 1.35, 1.00),  # Kenan Yıldız, muy físicos
"ECU": (1.00, 1.05, 1.10, 1.00),  # Caicedo, Plata, equilibrado
"AUT": (1.10, 1.00, 1.10, 1.05),  # Arnautović, Sabitzer, energético
"KOR": (1.05, 1.05, 1.20, 1.00),  # Son, presión alta, agresivos
"AUS": (1.00, 1.05, 1.15, 1.00),  # Sime Vrsaljko, físicos
"ALG": (0.95, 1.10, 1.15, 0.95),  # Mahrez, organizado y físico
"EGY": (0.90, 1.15, 1.15, 0.95),  # Salah, contraataque y bloque
"CAN": (1.05, 1.00, 1.05, 1.10),  # Davies, cruzados, anfitrión
"NOR": (1.20, 0.95, 0.95, 1.05),  # Haaland, muy atacante
"CIV": (1.10, 0.95, 1.20, 1.05),  # Haller, físicos, agresivos
"PAN": (0.80, 1.15, 1.30, 0.85),  # Defensivos, muy físicos
"SWE": (1.10, 1.05, 1.00, 1.05),  # Isak, Kulusevski, eficaces
"CZE": (1.00, 1.05, 1.00, 1.05),  # Schick, organizado
"PAR": (0.90, 1.15, 1.20, 0.90),  # Almirón, bloque y físico
"SCO": (1.00, 1.05, 1.15, 1.05),  # McTominay, aguerridos
"TUN": (0.85, 1.20, 1.20, 0.90),  # Defensivos, muy físicos
"COD": (0.90, 1.10, 1.25, 0.90),  # Wissa, físicos, defensivos
"UZB": (0.85, 1.05, 1.10, 0.90),  # Debutante, compacto
"QAT": (0.80, 1.00, 1.05, 0.90),  # Sin historial, poco creativo
"IRQ": (0.85, 1.00, 1.30, 0.90),  # Vuelve tras 40 años, muy físico
"RSA": (0.90, 1.05, 1.15, 0.95),  # Físicos, organizado
"KSA": (0.90, 1.05, 1.20, 0.90),  # Al-Dawsari, bloque físico
"JOR": (0.80, 1.05, 1.15, 0.85),  # Debut, organizado y físico
"BIH": (0.95, 1.00, 1.15, 0.95),  # Džeko, físico europeo
"CPV": (0.85, 1.10, 1.10, 0.85),  # Debut, compacto
"GHA": (1.00, 1.00, 1.15, 1.00),  # Kudus, atlético
"CUW": (0.80, 0.85, 1.05, 0.90),  # Debut, poca experiencia defensiva
"HAI": (0.80, 0.90, 1.10, 0.85),  # Histórica fragilidad defensiva
"NZL": (0.85, 1.05, 1.00, 0.90),  # Wood, organizado
}

# nombre visible en espanol, codigo FIFA 3 letras, confederacion, emoji bandera
TEAMS = {
"MEX": {"name":"México","conf":"CONCACAF","flag":"🇲🇽","host":True},
"RSA": {"name":"Sudáfrica","conf":"CAF","flag":"🇿🇦"},
"KOR": {"name":"Corea del Sur","conf":"AFC","flag":"🇰🇷"},
"CZE": {"name":"Chequia","conf":"UEFA","flag":"🇨🇿"},
"CAN": {"name":"Canadá","conf":"CONCACAF","flag":"🇨🇦","host":True},
"BIH": {"name":"Bosnia y Herzegovina","conf":"UEFA","flag":"🇧🇦"},
"QAT": {"name":"Catar","conf":"AFC","flag":"🇶🇦"},
"SUI": {"name":"Suiza","conf":"UEFA","flag":"🇨🇭"},
"BRA": {"name":"Brasil","conf":"CONMEBOL","flag":"🇧🇷"},
"MAR": {"name":"Marruecos","conf":"CAF","flag":"🇲🇦"},
"HAI": {"name":"Haití","conf":"CONCACAF","flag":"🇭🇹"},
"SCO": {"name":"Escocia","conf":"UEFA","flag":"🏴"},
"USA": {"name":"Estados Unidos","conf":"CONCACAF","flag":"🇺🇸","host":True},
"PAR": {"name":"Paraguay","conf":"CONMEBOL","flag":"🇵🇾"},
"AUS": {"name":"Australia","conf":"AFC","flag":"🇦🇺"},
"TUR": {"name":"Turquía","conf":"UEFA","flag":"🇹🇷"},
"GER": {"name":"Alemania","conf":"UEFA","flag":"🇩🇪"},
"CUW": {"name":"Curazao","conf":"CONCACAF","flag":"🇨🇼"},
"CIV": {"name":"Costa de Marfil","conf":"CAF","flag":"🇨🇮"},
"ECU": {"name":"Ecuador","conf":"CONMEBOL","flag":"🇪🇨"},
"NED": {"name":"Países Bajos","conf":"UEFA","flag":"🇳🇱"},
"JPN": {"name":"Japón","conf":"AFC","flag":"🇯🇵"},
"SWE": {"name":"Suecia","conf":"UEFA","flag":"🇸🇪"},
"TUN": {"name":"Túnez","conf":"CAF","flag":"🇹🇳"},
"BEL": {"name":"Bélgica","conf":"UEFA","flag":"🇧🇪"},
"EGY": {"name":"Egipto","conf":"CAF","flag":"🇪🇬"},
"IRN": {"name":"Irán","conf":"AFC","flag":"🇮🇷"},
"NZL": {"name":"Nueva Zelanda","conf":"OFC","flag":"🇳🇿"},
"ESP": {"name":"España","conf":"UEFA","flag":"🇪🇸"},
"CPV": {"name":"Cabo Verde","conf":"CAF","flag":"🇨🇻"},
"KSA": {"name":"Arabia Saudita","conf":"AFC","flag":"🇸🇦"},
"URU": {"name":"Uruguay","conf":"CONMEBOL","flag":"🇺🇾"},
"FRA": {"name":"Francia","conf":"UEFA","flag":"🇫🇷"},
"SEN": {"name":"Senegal","conf":"CAF","flag":"🇸🇳"},
"IRQ": {"name":"Irak","conf":"AFC","flag":"🇮🇶"},
"NOR": {"name":"Noruega","conf":"UEFA","flag":"🇳🇴"},
"ARG": {"name":"Argentina","conf":"CONMEBOL","flag":"🇦🇷"},
"ALG": {"name":"Argelia","conf":"CAF","flag":"🇩🇿"},
"AUT": {"name":"Austria","conf":"UEFA","flag":"🇦🇹"},
"JOR": {"name":"Jordania","conf":"AFC","flag":"🇯🇴"},
"POR": {"name":"Portugal","conf":"UEFA","flag":"🇵🇹"},
"COD": {"name":"R.D. del Congo","conf":"CAF","flag":"🇨🇩"},
"UZB": {"name":"Uzbekistán","conf":"AFC","flag":"🇺🇿"},
"COL": {"name":"Colombia","conf":"CONMEBOL","flag":"🇨🇴"},
"ENG": {"name":"Inglaterra","conf":"UEFA","flag":"🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
"CRO": {"name":"Croacia","conf":"UEFA","flag":"🇭🇷"},
"GHA": {"name":"Ghana","conf":"CAF","flag":"🇬🇭"},
"PAN": {"name":"Panamá","conf":"CONCACAF","flag":"🇵🇦"},
}

for code, d in TEAMS.items():
    d["rank"] = RANK[code]
    d.setdefault("host", False)

# Historial mundialista real: apariciones (incluyendo 2026), ultima participacion
# previa, mejor resultado historico. Fuentes: Wikipedia "2026 FIFA World Cup
# Group X", FIFA.com "Team profile and history", ESPN Group guides.
HIST = {
"MEX": ("18ª", "2022", "Cuartos de final (1970, 1986, como anfitrión)"),
"RSA": ("4ª", "2010", "Fase de grupos (mejor presentación, anfitrión 2010)"),
"KOR": ("12ª", "2022", "4° puesto (2002, co-anfitrión)"),
"CZE": ("11ª", "2006", "Subcampeón (1934 y 1962, como Checoslovaquia)"),
"CAN": ("3ª", "2022", "Fase de grupos (mejor resultado histórico)"),
"BIH": ("2ª", "2014", "Fase de grupos (única vez, 2014)"),
"QAT": ("2ª", "2022", "Fase de grupos (anfitrión 2022, sin victorias)"),
"SUI": ("13ª", "2022", "Cuartos de final (1934, 1938, 1954)"),
"BRA": ("23ª", "2022", "Campeón (1958, 1962, 1970, 1994, 2002) — 5 títulos"),
"MAR": ("7ª", "2022", "4° puesto (2022, mejor histórico africano)"),
"HAI": ("2ª", "1974", "Fase de grupos (única vez, 1974)"),
"SCO": ("9ª", "1998", "Fase de grupos (nunca superada)"),
"USA": ("12ª", "2022", "4° puesto (1930, primer Mundial)"),
"PAR": ("9ª", "2010", "Cuartos de final (2010)"),
"AUS": ("7ª", "2022", "Octavos de final (2006, 2022)"),
"TUR": ("3ª", "2002", "3er puesto (2002)"),
"GER": ("20ª", "2022", "Campeón (1954, 1974, 1990, 2014) — 4 títulos"),
"CUW": ("1ª (debut)", "—", "Sin historial — primer Mundial"),
"CIV": ("4ª", "2014", "Fase de grupos (nunca superada)"),
"ECU": ("5ª", "2022", "Octavos de final (2006)"),
"NED": ("11ª", "2022", "Subcampeón (1974, 1978, 2010) — 3 finales sin título"),
"JPN": ("8ª", "2022", "Octavos de final (2002, 2010, 2018, 2022)"),
"SWE": ("13ª", "2018", "Subcampeón (1958, como anfitrión)"),
"TUN": ("7ª", "2022", "Fase de grupos (nunca superada)"),
"BEL": ("15ª", "2022", "3er puesto (2018)"),
"EGY": ("4ª", "2018", "Fase de grupos (nunca superada)"),
"IRN": ("7ª", "2022", "Fase de grupos (nunca superada)"),
"NZL": ("3ª", "2010", "Fase de grupos (invicto en 2010, eliminado igual)"),
"ESP": ("17ª", "2022", "Campeón (2010) — 1 título"),
"CPV": ("1ª (debut)", "—", "Sin historial — primer Mundial"),
"KSA": ("7ª", "2022", "Octavos de final (1994)"),
"URU": ("14ª", "2022", "Campeón (1930, 1950) — 2 títulos, los más antiguos"),
"FRA": ("17ª", "2022", "Campeón (1998, 2018) — 2 títulos, subcampeón 2006 y 2022"),
"SEN": ("4ª", "2022", "Cuartos de final (2002)"),
"IRQ": ("2ª", "1986", "Fase de grupos (única vez, 1986) — vuelve tras 40 años"),
"NOR": ("4ª", "1998", "Octavos de final (1938, 1998) — vuelve tras 28 años"),
"ARG": ("19ª", "2022", "Campeón (1978, 1986, 2022) — 3 títulos, vigente campeón"),
"ALG": ("5ª", "2014", "Octavos de final (2014)"),
"AUT": ("8ª", "1998", "4° puesto (1934, 1954) — vuelve tras 28 años"),
"JOR": ("1ª (debut)", "—", "Sin historial — primer Mundial"),
"POR": ("9ª", "2022", "3er puesto (1966, 2006)"),
"COD": ("2ª", "1974", "Fase de grupos (como Zaire, única vez, 1974)"),
"UZB": ("1ª (debut)", "—", "Sin historial — primer Mundial"),
"COL": ("7ª", "2018", "Cuartos de final (2014)"),
"ENG": ("17ª", "2022", "Campeón (1966) — 1 título"),
"CRO": ("7ª", "2022", "Subcampeón (2018), 3er puesto (2022)"),
"GHA": ("5ª", "2022", "Cuartos de final (2010)"),
"PAN": ("2ª", "2018", "Fase de grupos (única vez, 2018)"),
}

# Via de clasificacion (dato real, breve)
QUAL = {
"MEX":"Anfitrión — clasificación automática (14 feb 2023)",
"RSA":"1° del Grupo C de CAF, por delante de Nigeria",
"KOR":"1° del Grupo B de AFC, invicto en toda la fase",
"CZE":"2° en su grupo UEFA; ganó el repechaje a Irlanda y Dinamarca por penales",
"CAN":"Anfitrión — clasificación automática",
"BIH":"Vía repechaje europeo (play-off UEFA)",
"QAT":"Vía repechaje de AFC",
"SUI":"1° de su grupo de clasificación UEFA",
"BRA":"Clasificó directo por Conmebol",
"MAR":"1° de su grupo de clasificación de CAF",
"HAI":"Vía repechaje intercontinental — clasificación histórica",
"SCO":"2° de su grupo UEFA; venció el repechaje, fin de 28 años de ausencia",
"USA":"Anfitrión — clasificación automática",
"PAR":"Clasificó directo por Conmebol",
"AUS":"1° de su grupo final de clasificación de AFC",
"TUR":"2° de su grupo UEFA; venció a Kosovo en el repechaje",
"GER":"1° de su grupo de clasificación UEFA",
"CUW":"Vía repechaje de Concacaf — debut histórico (la federación más pequeña en jugar un Mundial)",
"CIV":"1° de su grupo de clasificación de CAF",
"ECU":"Clasificó directo por Conmebol",
"NED":"1° de su grupo de clasificación UEFA",
"JPN":"1° de su grupo final de clasificación de AFC",
"SWE":"Vía repechaje europeo (play-off UEFA)",
"TUN":"1° de su grupo de clasificación de CAF",
"BEL":"1° de su grupo de clasificación UEFA",
"EGY":"1° de su grupo de clasificación de CAF",
"IRN":"1° de su grupo final de clasificación de AFC",
"NZL":"Representante único de Oceanía (OFC)",
"ESP":"1° de su grupo de clasificación UEFA",
"CPV":"1° de su grupo de clasificación de CAF — debut histórico",
"KSA":"Vía repechaje de AFC",
"URU":"Clasificó directo por Conmebol",
"FRA":"1° de su grupo de clasificación UEFA",
"SEN":"1° de su grupo de clasificación de CAF",
"IRQ":"Vía repechaje intercontinental — vuelve tras 40 años",
"NOR":"1° de su grupo de clasificación UEFA — vuelve tras 28 años",
"ARG":"1° de la fase clasificatoria de Conmebol, como vigente campeón",
"ALG":"1° de su grupo de clasificación de CAF",
"AUT":"2° de su grupo UEFA; venció el repechaje — vuelve tras 28 años",
"JOR":"Vía repechaje intercontinental — debut histórico",
"POR":"1° de su grupo de clasificación UEFA",
"COD":"Vía repechaje intercontinental",
"UZB":"Vía repechaje intercontinental — debut histórico",
"COL":"Clasificó directo por Conmebol, de regreso tras perderse 2022",
"ENG":"1° de su grupo de clasificación UEFA, invicto",
"CRO":"1° de su grupo de clasificación UEFA",
"GHA":"1° de su grupo de clasificación de CAF",
"PAN":"Vía repechaje intercontinental",
}

# Forma reciente / dato concreto reciente (real, verificado por busqueda).
RECENT_NOTE = {
"MEX":"Venció 2–0 a Sudáfrica en el partido inaugural del Mundial (11 jun)",
"RSA":"Cayó 0–2 ante México en su debut (11 jun)",
"KOR":"Ganó 2–1 a Chequia con doblete de remontada (11 jun)",
"CZE":"Cayó 1–2 ante Corea del Sur tras ir arriba en el marcador (11 jun)",
"CAN":"Empató 1–1 con Bosnia y Herzegovina en su debut (12 jun)",
"BIH":"Empató 1–1 con Canadá en su debut mundialista (12 jun)",
"QAT":"Empató 1–1 con Suiza en su debut (13 jun)",
"SUI":"Empató 1–1 con Catar en su debut (13 jun)",
"BRA":"Empató 1–1 con Marruecos en su debut (13 jun)",
"MAR":"Empató 1–1 con Brasil en su debut (13 jun)",
"HAI":"Cayó 0–1 ante Escocia en su debut histórico (13 jun)",
"SCO":"Venció 1–0 a Haití en su regreso tras 28 años (13 jun)",
"USA":"Venció a Paraguay en el debut como anfitrión (12 jun)",
"PAR":"Cayó ante Estados Unidos en su debut (12 jun)",
"AUS":"Sorprendió y venció a Turquía en su debut (13 jun)",
"TUR":"Cayó ante Australia en su debut (13 jun)",
"GER":"Goleó 7–1 a Curazao en su debut (14 jun)",
"CUW":"Cayó 1–7 ante Alemania en su histórico debut mundialista (14 jun)",
"CIV":"Venció 1–0 a Ecuador en su debut (14 jun)",
"ECU":"Cayó 0–1 ante Costa de Marfil en su debut (14 jun)",
"NED":"Empató 2–2 con Japón en su debut (14 jun)",
"JPN":"Empató 2–2 con Países Bajos en un partido vibrante (14 jun)",
"SWE":"Goleó 5–1 a Túnez en su debut (14 jun)",
"TUN":"Cayó 1–5 ante Suecia en su debut (14 jun)",
"BEL":"Empató 1–1 con Egipto en su debut (15 jun)",
"EGY":"Empató 1–1 con Bélgica en su debut (15 jun)",
"IRN":"Empató 2–2 con Nueva Zelanda en partido vistoso (15 jun)",
"NZL":"Empató 2–2 con Irán en su regreso al Mundial (15 jun)",
"ESP":"Empató 0–0 con Cabo Verde en su debut (15 jun)",
"CPV":"Empató 0–0 con España en su histórico debut (15 jun)",
"KSA":"Empató 1–1 con Uruguay en su debut (15 jun)",
"URU":"Empató 1–1 con Arabia Saudita en su debut (15 jun)",
"FRA":"Venció 3–1 a Senegal; Mbappé llegó a ser su máximo goleador histórico (16 jun)",
"SEN":"Cayó 1–3 ante Francia en su debut (16 jun)",
"IRQ":"Cayó 1–4 ante Noruega en su regreso tras 40 años (16 jun)",
"NOR":"Goleó 4–1 a Irak con doblete de Haaland en su debut histórico (16 jun)",
"ARG":"Venció 3–0 a Argelia con hat-trick de Messi en su debut (16 jun)",
"ALG":"Cayó 0–3 ante Argentina en su debut (16 jun)",
"AUT":"Venció 3–1 a Jordania, su primer triunfo en partido inaugural en 28 años (17 jun)",
"JOR":"Cayó 1–3 ante Austria en su histórico debut mundialista (17 jun)",
"POR":"Empató 1–1 con R.D. del Congo en su debut, con gol de João Neves (17 jun)",
"COD":"Empató 1–1 con Portugal en su histórico debut, con gol de Yoane Wissa (17 jun)",
"UZB":"Cayó 1–3 ante Colombia en su histórico debut mundialista (17 jun)",
"COL":"Venció 3–1 a Uzbekistán en su regreso al Mundial, gol de Luis Díaz (17 jun)",
"ENG":"Venció 4–2 a Croacia con doblete de Harry Kane (17 jun)",
"CRO":"Cayó 2–4 ante Inglaterra tras ir igualando dos veces (17 jun)",
"GHA":"Venció 1–0 a Panamá con gol de Yirenkyi en el último minuto (17 jun)",
"PAN":"Cayó 0–1 ante Ghana en los últimos minutos (17 jun)",
}

# Jugador clave (figura real conocida de la plantilla 2026, sin inventar % de gol)
PLAYERS = {
"MEX":"Raúl Jiménez","RSA":"Lyle Foster","KOR":"Son Heung-min","CZE":"Patrik Schick",
"CAN":"Alphonso Davies","BIH":"Edin Džeko","QAT":"Akram Afif","SUI":"Granit Xhaka",
"BRA":"Vinícius Júnior","MAR":"Achraf Hakimi","HAI":"Duckens Nazon","SCO":"Scott McTominay",
"USA":"Christian Pulisic","PAR":"Miguel Almirón","AUS":"Mathew Leckie","TUR":"Kenan Yıldız",
"GER":"Jamal Musiala","CUW":"Leandro Bacuna","CIV":"Sébastien Haller","ECU":"Moisés Caicedo",
"NED":"Cody Gakpo","JPN":"Takefusa Kubo","SWE":"Alexander Isak","TUN":"Hannibal Mejbri",
"BEL":"Kevin De Bruyne","EGY":"Mohamed Salah","IRN":"Mehdi Taremi","NZL":"Chris Wood",
"ESP":"Lamine Yamal","CPV":"Ryan Mendes","KSA":"Salem Al-Dawsari","URU":"Federico Valverde",
"FRA":"Kylian Mbappé","SEN":"Sadio Mané","IRQ":"Ayman Hussein","NOR":"Erling Haaland",
"ARG":"Lionel Messi","ALG":"Riyad Mahrez","AUT":"Marko Arnautović","JOR":"Yazan Al-Naimat",
"POR":"Cristiano Ronaldo","COD":"Yoane Wissa","UZB":"Eldor Shomurodov","COL":"Luis Díaz",
"ENG":"Harry Kane","CRO":"Luka Modrić","GHA":"Mohammed Kudus","PAN":"José Fajardo",
}
