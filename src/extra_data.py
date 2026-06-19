# -*- coding: utf-8 -*-
"""
Datos recopilados el 18-jun-2026 para agregar al sitio.
Fuentes: Sofascore (clima), Wikipedia (grupos/H2H), Yahoo/ESPN (resultados).
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1. CLIMA POR SEDE  (fuente: sofascore.com/news/expected-world-cup-weather)
#    roof: True  = techo retráctil + clima controlado
#    temp_c: temperatura media en ºC en junio-julio
#    humid: humedad media %
#    note_es: descripción en español para mostrar en el sitio
# ─────────────────────────────────────────────────────────────────────────────
VENUE_WEATHER = {
    "Mexico City": {
        "roof": False,
        "temp_c": 26,
        "humid": 67,
        "note_es": "Aire libre · 26 °C · Alt. 2.240 m · Inicio temporada de lluvias"
    },
    "Guadalajara": {
        "roof": False,
        "temp_c": 30,
        "humid": 63,
        "note_es": "Aire libre · 30 °C · Alt. 1.580 m · Posible lluvia (temporada húmeda)"
    },
    "Monterrey": {
        "roof": False,
        "temp_c": 36,
        "humid": 65,
        "note_es": "Aire libre · 36 °C · Verano muy caluroso — condiciones exigentes"
    },
    "Toronto": {
        "roof": False,
        "temp_c": 24,
        "humid": 55,
        "note_es": "Aire libre · 24 °C · Condiciones cómodas para jugar"
    },
    "Vancouver": {
        "roof": True,
        "temp_c": 19,
        "humid": 62,
        "note_es": "Techo retráctil · Clima controlado · 19 °C exterior"
    },
    "San Francisco": {
        "roof": False,
        "temp_c": 26,
        "humid": 60,
        "note_es": "Aire libre · 26 °C · Condiciones frescas y cómodas"
    },
    "Los Angeles": {
        "roof": True,   # SoFi tiene techo pero lados abiertos
        "temp_c": 24,
        "humid": 76,
        "note_es": "Techo con lados abiertos · 24 °C · Condiciones agradables"
    },
    "Seattle": {
        "roof": False,
        "temp_c": 22,
        "humid": 67,
        "note_es": "Aire libre · 22 °C · Clima templado y seco en verano"
    },
    "New York/NJ": {
        "roof": False,
        "temp_c": 29,
        "humid": 64,
        "note_es": "Aire libre · 29 °C · Sede de la gran final (19 jul)"
    },
    "Boston": {
        "roof": False,
        "temp_c": 28,
        "humid": 70,
        "note_es": "Aire libre · 28 °C · Veranos moderados"
    },
    "Philadelphia": {
        "roof": False,
        "temp_c": 31,
        "humid": 70,
        "note_es": "Aire libre · 31 °C · Calor húmedo similar a Nueva York"
    },
    "Miami": {
        "roof": False,
        "temp_c": 32,
        "humid": 75,
        "note_es": "Aire libre · 32 °C · Calor húmedo · Tormentas vespertinas frecuentes"
    },
    "Atlanta": {
        "roof": True,
        "temp_c": 32,
        "humid": 74,
        "note_es": "Techo retráctil · Clima controlado · 32 °C exterior"
    },
    "Houston": {
        "roof": True,
        "temp_c": 35,
        "humid": 76,
        "note_es": "Techo retráctil · Clima controlado · 35 °C exterior con 76% humedad"
    },
    "Dallas": {
        "roof": True,
        "temp_c": 36,
        "humid": 60,
        "note_es": "Techo retráctil · Clima controlado · 36 °C exterior"
    },
    "Kansas City": {
        "roof": False,
        "temp_c": 31,
        "humid": 67,
        "note_es": "Aire libre · 31 °C · Sede de cuartos de final (11 jul)"
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. RESULTADOS REALES YA JUGADOS (actualizado al 18-jun-2026, J2 en curso)
#    Formato: (goles_home, goles_away) o None si aún no se jugó
#    Fuentes: Yahoo Sports, ESPN, BBC Sport
# ─────────────────────────────────────────────────────────────────────────────
REAL_SCORES = {
    # Jornada 1 (todos jugados)
    ("MEX","RSA"): (2, 0),
    ("KOR","CZE"): (2, 1),
    ("CAN","BIH"): (1, 1),
    ("QAT","SUI"): (1, 1),
    ("BRA","MAR"): (1, 1),
    ("HAI","SCO"): (0, 1),
    ("USA","PAR"): (1, 0),   # marcador confirmado por ESPN/Yahoo (USA ganó)
    ("AUS","TUR"): (1, 0),   # marcador confirmado (AUS ganó)
    ("GER","CUW"): (7, 1),
    ("CIV","ECU"): (1, 0),
    ("NED","JPN"): (2, 2),
    ("SWE","TUN"): (5, 1),
    ("BEL","EGY"): (1, 1),
    ("IRN","NZL"): (2, 2),
    ("ESP","CPV"): (0, 0),
    ("KSA","URU"): (1, 1),
    ("FRA","SEN"): (3, 1),
    ("IRQ","NOR"): (1, 4),
    ("ARG","ALG"): (3, 0),
    ("AUT","JOR"): (3, 1),
    ("POR","COD"): (1, 1),
    ("UZB","COL"): (1, 3),
    ("ENG","CRO"): (4, 2),
    ("GHA","PAN"): (1, 0),
    # Jornada 2 en curso hoy 18-jun (CZE vs RSA en progreso, resto aún no jugados)
    ("CZE","RSA"): (1, 1),   # empate al descanso, partido en progreso → marcar como "en curso"
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. HEAD-TO-HEAD EN MUNDIALES — para los 72 cruces de fase de grupos
#    Fuente: páginas Wikipedia "2026 FIFA World Cup Group X"
#    Formato: "descripción breve en español"
#    "Primera vez" si nunca se han enfrentado en un Mundial
# ─────────────────────────────────────────────────────────────────────────────
H2H_WC = {
    # GRUPO A
    ("MEX","RSA"): "Se han enfrentado 4 veces; el más reciente fue el empate 1-1 en el partido inaugural del Mundial 2010 (cuando Sudáfrica fue anfitrión)",
    ("KOR","CZE"): "3 partidos previos; el más reciente fue una victoria 2-1 de Corea en un amistoso de 2016",
    ("CZE","RSA"): "Solo se enfrentaron en la Copa Confederaciones 1997 (2-2). Primer cruce en un Mundial",
    ("MEX","KOR"): "15 partidos, 2 en Mundiales: México ganó 3-1 en 1998 y 2-1 en 2018",
    ("CZE","MEX"): "Solo 1 partido previo (Chequia ganó 2-1 en un amistoso de 2000). Nota: Checoslovaquia jugó vs México en 1962 (México ganó 3-1)",
    ("RSA","KOR"): "Primera vez que se enfrentan en un Mundial",

    # GRUPO B
    ("CAN","BIH"): "Solo se han enfrentado en un amistoso (Canadá ganó 2-0 en 2022). Primera vez en un Mundial",
    ("QAT","SUI"): "1 partido previo (amistoso 2018, Catar ganó 1-0). Primera vez en un Mundial",
    ("SUI","BIH"): "Solo 1 amistoso previo (Bosnia ganó 2-0 en 2016). Primera vez en un Mundial",
    ("CAN","QAT"): "2 partidos previos (amistosos). Primera vez en un Mundial",
    ("SUI","CAN"): "Primer enfrentamiento entre estas selecciones",
    ("BIH","QAT"): "Se han visto dos veces: Catar ganó 2-0 (2000) y empataron 1-1 (2010). Primera vez en un Mundial",

    # GRUPO C
    ("BRA","MAR"): "3 partidos, incluyendo 1 en el Mundial: Brasil ganó 3-0 en 1998. Marruecos obtuvo su primera victoria en 2023 (2-1 en amistoso)",
    ("HAI","SCO"): "Primera vez que se enfrentan",
    ("SCO","MAR"): "Solo se han visto en el Mundial 1998: Marruecos ganó 3-0 en la última jornada del grupo",
    ("BRA","HAI"): "3 partidos previos; el más reciente fue la histórica goleada 7-1 de Brasil en la Copa América Centenario 2016",
    ("SCO","BRA"): "10 partidos, 4 en Mundiales: empate 0-0 en 1974, Brasil ganó 4-1 (1982), 1-0 (1990) y 2-1 en el partido inaugural de 1998",
    ("MAR","HAI"): "Primera vez que se enfrentan",

    # GRUPO D
    ("USA","PAR"): "9 partidos, 1 en el Mundial: EEUU ganó 3-0 en la primera edición de 1930",
    ("AUS","TUR"): "5 partidos previos; el más reciente fue una victoria 1-0 de Australia (amistoso 2010). Primera vez en un Mundial",
    ("TUR","PAR"): "Primera vez que se enfrentan",
    ("USA","AUS"): "4 partidos; el más reciente fue una victoria 2-1 de EEUU (amistoso 2025). Primera vez en un Mundial",
    ("TUR","USA"): "Primera vez que se enfrentan en un Mundial",
    ("PAR","AUS"): "5 partidos previos. Primera vez en un Mundial",

    # GRUPO E
    ("GER","CUW"): "Nunca se habían enfrentado. Debut histórico de Curazao en un Mundial",
    ("CIV","ECU"): "1 amistoso previo (empate 2-2 en 2009). Primera vez en un Mundial",
    ("GER","CIV"): "1 amistoso previo (Alemania ganó tras un partido disputado). Primera vez en un Mundial",
    ("ECU","CUW"): "Nunca se habían enfrentado",
    ("ECU","GER"): "2 partidos: Alemania ganó 3-0 en el Mundial 2006 (de local) y 4-2 en amistoso de 2013",
    ("CUW","CIV"): "Nunca se habían enfrentado",

    # GRUPO F
    ("NED","JPN"): "3 partidos incluyendo 1 en el Mundial: Países Bajos ganó 1-0 en el Mundial 2010. Empate 2-2 en el último amistoso de 2013",
    ("SWE","TUN"): "3 partidos previos; el más reciente fue un empate 1-1 en amistoso de 2009. Primera vez en un Mundial",
    ("NED","SWE"): "Primera vez que se enfrentan en un Mundial",
    ("TUN","JPN"): "6 partidos; Japón ganó 2-0 en el Mundial 2002 (que coanfitrionearon). Japón también ganó 2-0 en su último encuentro (2023)",
    ("JPN","SWE"): "Primera vez que se enfrentan en un Mundial",
    ("TUN","NED"): "3 partidos previos. Primera vez en un Mundial",

    # GRUPO G
    ("BEL","EGY"): "4 partidos; el más reciente fue una victoria 2-1 de Egipto (amistoso 2022). Primera vez en un Mundial",
    ("IRN","NZL"): "2 partidos; Irán ganó 3-0 en la última Copa AFC-OFC. Primera vez en un Mundial",
    ("BEL","IRN"): "Nunca se habían enfrentado",
    ("NZL","EGY"): "3 partidos previos; el más reciente fue una victoria 1-0 de Egipto (Copa FIFA Series 2024). Primera vez en un Mundial",
    ("EGY","IRN"): "2 partidos; Egipto ganó en penales (Copa LG 2000). Primera vez en un Mundial",
    ("NZL","BEL"): "Nunca se habían enfrentado",

    # GRUPO H
    ("ESP","CPV"): "Nunca se habían enfrentado. Debut histórico de Cabo Verde en un Mundial",
    ("KSA","URU"): "3 partidos, incluyendo el Mundial 2018 donde Uruguay ganó 1-0",
    ("ESP","KSA"): "3 partidos; España ganó todos, incluyendo 1-0 en el Mundial 2006 y 5-0 en amistoso 2012",
    ("URU","CPV"): "Nunca se habían enfrentado",
    ("CPV","KSA"): "Nunca se habían enfrentado",
    ("URU","ESP"): "10 partidos, 2 en el Mundial: empate 2-2 en el torneo final de 1950 y 0-0 en 1990. España invicta en todos sus cruces",

    # GRUPO I
    ("FRA","SEN"): "Solo 1 partido en un Mundial: Senegal venció 1-0 a Francia en el partido inaugural del Mundial 2002 — la mayor sorpresa de ese torneo",
    ("IRQ","NOR"): "Nunca se habían enfrentado",
    ("FRA","IRQ"): "Nunca se habían enfrentado",
    ("NOR","SEN"): "1 amistoso previo (Senegal ganó 2-1 en 2006). Primera vez en un Mundial",
    ("FRA","NOR"): "16 partidos; el más reciente fue una victoria 4-0 de Francia (amistoso 2014). Primera vez en un Mundial",
    ("SEN","IRQ"): "Nunca se habían enfrentado",

    # GRUPO J
    ("ARG","ALG"): "Solo 1 amistoso (Argentina ganó 4-3 en 2007). Primera vez en un Mundial",
    ("AUT","JOR"): "Nunca se habían enfrentado. Debut histórico de Jordania en un Mundial",
    ("ARG","AUT"): "3 amistosos; el más reciente fue un empate 1-1 en 1990. Primera vez en un Mundial",
    ("JOR","ALG"): "3 partidos previos; el más reciente fue un empate 1-1 (amistoso 2004). Primera vez en un Mundial",
    ("ALG","AUT"): "1 partido en el Mundial: Austria ganó 2-0 en 1982",
    ("JOR","ARG"): "Nunca se habían enfrentado",

    # GRUPO K
    ("POR","COD"): "Nunca se habían enfrentado. Primer Mundial de R.D. del Congo desde 1974 (cuando era Zaire)",
    ("UZB","COL"): "Nunca se habían enfrentado. Debut histórico de Uzbekistán en un Mundial",
    ("POR","UZB"): "Nunca se habían enfrentado",
    ("COL","COD"): "Nunca se habían enfrentado",
    ("COL","POR"): "Nunca se habían enfrentado en un Mundial",
    ("COD","UZB"): "Nunca se habían enfrentado",

    # GRUPO L
    ("ENG","CRO"): "11 partidos, incluyendo la semifinal del Mundial 2018 donde Croacia ganó 2-1 en tiempo extra. También se enfrentaron en la Euro 2020 (ENG ganó 1-0)",
    ("GHA","PAN"): "Nunca se habían enfrentado",
    ("ENG","GHA"): "1 amistoso (empate 1-1 en 2011). Primera vez en un Mundial",
    ("PAN","CRO"): "Nunca se habían enfrentado",
    ("ENG","PAN"): "Solo 1 partido en un Mundial: Inglaterra goleó 6-1 a Panamá en el Mundial 2018",
    ("CRO","GHA"): "Nunca se habían enfrentado",
}
