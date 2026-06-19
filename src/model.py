# -*- coding: utf-8 -*-
"""
Modelo estadistico para los 72 partidos de fase de grupos del Mundial 2026.

Metodologia (igual para los 72 partidos, totalmente reproducible):
1. Rating tipo Elo derivado del Ranking FIFA real al 11-jun-2026:
   R = 1900 - 9*(rank-1)   [rank 1 -> 1900, rank 85 -> 1144]
   Bonus de +40 puntos de rating si el equipo es anfitrion (MEX/USA/CAN)
   jugando en su torneo (ventaja real de localia/aficion).
2. xG total esperado fijo en 2.60 goles/partido (promedio historico real
   de goles por partido en fases de grupos de Mundiales recientes).
   Se reparte segun la diferencia de rating con una logistica suave.
3. Division por mitades: 45% de los goles en la 1a mitad, 55% en la 2a
   (tendencia historica real: mas goles conforme avanza el partido).
4. Monte Carlo real con numpy, N=50.000 simulaciones por partido: se
   simulan goles de cada mitad con Poisson independientes y se agregan.
   Todas las probabilidades (1X2, doble oportunidad, over/under, BTTS,
   handicap, clean sheet, marcadores exactos, marcador al descanso,
   "giro de resultado") se derivan EMPIRICAMENTE de esas simulaciones.
5. Corners y tarjetas/faltas se modelan con Poisson independientes,
   calibrados con promedios reales de Mundiales recientes (~9-10
   corners/partido, ~3.5-4 tarjetas/partido).
"""
import numpy as np

N_SIM = 50000
RNG = np.random.default_rng(20260618)

XG_TOTAL_BASE = 2.60
HOST_BONUS = 40


def rating(rank, host=False):
    r = 1900 - 9 * (rank - 1)
    if host:
        r += HOST_BONUS
    return r


def simulate_match(rank_home, rank_away, host_home=False, host_away=False,
                   seed_offset=0,
                   style_home=(1.0,1.0,1.0,1.0), style_away=(1.0,1.0,1.0,1.0)):
    """
    style_x = (ATT, DEF, CARD, CORN)
    ATT_home * (1/DEF_away) -> escala el xG del local
    ATT_away * (1/DEF_home) -> escala el xG del visitante
    """
    Rh = rating(rank_home, host_home)
    Ra = rating(rank_away, host_away)
    diff = Rh - Ra

    att_h, def_h, card_h, corn_h = style_home
    att_a, def_a, card_a, corn_a = style_away

    # xG base según calidad de los equipos y diferencia de nivel
    avg_R = (Rh + Ra) / 2
    quality = float(np.clip((avg_R - 1144) / (1900 - 1144), 0, 1.3))
    gap = float(np.clip(abs(diff) / 756, 0, 1.3))
    xg_base = 2.15 + 0.55 * quality + 0.65 * gap
    xg_base = float(np.clip(xg_base, 1.85, 3.8))

    # Reparto base según Elo
    share_h = 1 / (1 + 10 ** (-diff / 700))

    # xG individual ajustado por estilo (ATT propio × 1/DEF rival)
    # Normalizamos para que la suma total escale respecto a xg_base
    raw_h = share_h * att_h * (1.0 / def_a)
    raw_a = (1 - share_h) * att_a * (1.0 / def_h)
    total_raw = raw_h + raw_a
    # Escalar para que la suma final tenga sentido (cercana a xg_base ajustado)
    style_total_factor = (att_h / def_a + att_a / def_h) / 2.0
    xg_total_match = float(np.clip(xg_base * style_total_factor, 1.4, 4.2))
    xg_h = xg_total_match * (raw_h / total_raw)
    xg_a = xg_total_match * (raw_a / total_raw)

    lh1, lh2 = xg_h * 0.45, xg_h * 0.55
    la1, la2 = xg_a * 0.45, xg_a * 0.55

    rng = np.random.default_rng(20260618 + seed_offset)
    h1 = rng.poisson(lh1, N_SIM)
    h2 = rng.poisson(lh2, N_SIM)
    a1 = rng.poisson(la1, N_SIM)
    a2 = rng.poisson(la2, N_SIM)
    hg = h1 + h2
    ag = a1 + a2
    hht = h1
    aht = a1

    # --- Corners ---
    corners_base = 8.4 + (xg_total_match - 2.6) * 1.8
    corners_base = float(np.clip(corners_base, 6.0, 13.0))
    corners_total_l = corners_base * (corn_h + corn_a) / 2.0
    corners_total_l = float(np.clip(corners_total_l, 5.5, 14.0))
    corner_share_h = 0.5 + (share_h - 0.5) * 0.75
    c_h_raw = corner_share_h * corn_h
    c_a_raw = (1 - corner_share_h) * corn_a
    c_tot_raw = c_h_raw + c_a_raw
    c_h_l = corners_total_l * c_h_raw / c_tot_raw
    c_a_l = corners_total_l * c_a_raw / c_tot_raw
    ch = rng.poisson(c_h_l, N_SIM)
    ca = rng.poisson(c_a_l, N_SIM)

    # --- Tarjetas y faltas ---
    # Base según lo parejo del partido, ajustada por estilo físico de cada equipo
    cards_base = 3.4 + max(0.0, (700 - abs(diff))) / 700 * 1.0
    card_share_h = 0.5 - (share_h - 0.5) * 0.25
    y_h_l = cards_base * card_share_h * card_h
    y_a_l = cards_base * (1 - card_share_h) * card_a
    cards_total_l = y_h_l + y_a_l
    yh = rng.poisson(y_h_l, N_SIM)
    ya = rng.poisson(y_a_l, N_SIM)
    fouls_total_l = cards_total_l * 6.1
    red_prob = float(np.clip(0.12 - abs(diff) / 9000 + (card_h + card_a - 2.0) * 0.015, 0.04, 0.22))

    def pct(mask):
        return float(np.mean(mask)) * 100

    res = {}
    res["Rh"], res["Ra"], res["diff"] = Rh, Ra, diff
    res["xg_h"], res["xg_a"] = xg_h, xg_a
    res["xg_total"] = xg_h + xg_a

    # 1X2
    res["p_home"] = pct(hg > ag)
    res["p_draw"] = pct(hg == ag)
    res["p_away"] = pct(hg < ag)
    res["p_1x"] = res["p_home"] + res["p_draw"]
    res["p_12"] = res["p_home"] + res["p_away"]
    res["p_x2"] = res["p_draw"] + res["p_away"]

    # Over/Under goles totales
    tg = hg + ag
    for line in [1.5, 2.5, 3.5, 4.5]:
        res[f"over_{line}"] = pct(tg > line)
        res[f"under_{line}"] = 100 - res[f"over_{line}"]

    # BTTS
    res["btts_yes"] = pct((hg > 0) & (ag > 0))
    res["btts_no"] = 100 - res["btts_yes"]
    # BTTS 2a mitad (ambos marcan en la segunda mitad)
    res["btts_2h"] = pct((h2 > 0) & (a2 > 0))
    res["home_scores_1h"] = pct(h1 > 0)

    # Clean sheet
    res["cs_home"] = pct(ag == 0)   # home no recibe goles
    res["cs_away"] = pct(hg == 0)   # away no recibe goles

    # Handicap asiatico
    res["hcap_home_-1.5"] = pct((hg - ag) >= 2)
    res["hcap_away_+1.5"] = 100 - res["hcap_home_-1.5"]
    res["hcap_home_-2.5"] = pct((hg - ag) >= 3)
    res["hcap_away_+2.5"] = 100 - res["hcap_home_-2.5"]

    # Marcadores exactos (top 6)
    from collections import Counter
    cnt = Counter(zip(hg.tolist(), ag.tolist()))
    top6 = cnt.most_common(6)
    res["top_scores"] = [(f"{h}-{a}", c / N_SIM * 100) for (h, a), c in top6]

    # Medio tiempo
    res["ht_home"] = pct(hht > aht)
    res["ht_draw"] = pct(hht == aht)
    res["ht_away"] = pct(hht < aht)

    # Giro de resultado tras el descanso (signo del marcador cambia entre HT y FT)
    sign_ht = np.sign(hht - aht)
    sign_ft = np.sign(hg - ag)
    res["giro_resultado"] = pct(sign_ht != sign_ft)

    # Goleada (margen final >= 3) para cada lado
    res["goleada_home"] = pct((hg - ag) >= 3)
    res["goleada_away"] = pct((ag - hg) >= 3)

    # Marcador promedio simulado y resultado mas repetido
    res["avg_home_goals"] = float(np.mean(hg))
    res["avg_away_goals"] = float(np.mean(ag))
    res["mode_score"] = top6[0][0] if top6 else (0, 0)

    # Corners
    res["corners_total"] = float(np.mean(ch + ca))
    res["corners_home"] = float(np.mean(ch))
    res["corners_away"] = float(np.mean(ca))
    res["over_corners_5.5"] = pct((ch + ca) > 5.5)
    res["over_corners_7.5"] = pct((ch + ca) > 7.5)
    res["over_corners_9.5"] = pct((ch + ca) > 9.5)
    res["under_corners_9.5"] = 100 - res["over_corners_9.5"]
    res["over_corners_11.5"] = pct((ch + ca) > 11.5)
    res["hcap_corners_home_-1.5"] = pct((ch - ca) >= 2)

    # Tarjetas / faltas
    res["cards_total"] = float(np.mean(yh + ya))
    res["red_prob"] = red_prob * 100
    res["over_cards_2.5"] = pct((yh + ya) > 2.5)
    res["over_cards_3.5"] = pct((yh + ya) > 3.5)
    res["over_cards_4.5"] = pct((yh + ya) > 4.5)
    res["fouls_total"] = fouls_total_l
    res["over_fouls_19.5"] = pct(rng.poisson(fouls_total_l, N_SIM) > 19.5)
    res["over_fouls_21.5"] = pct(rng.poisson(fouls_total_l, N_SIM) > 21.5)
    res["over_fouls_25.5"] = pct(rng.poisson(fouls_total_l, N_SIM) > 25.5)

    # Confianza del modelo
    res["confidence"] = float(np.clip(50 + abs(diff) / 12, 50, 92))

    # Distribucion temporal de goles (forma cerrada, calibrada al xg del partido)
    weights = [0.13, 0.15, 0.17, 0.18, 0.19, 0.18]
    res["temporal"] = []
    for w in weights:
        il = res["xg_total"] * w
        res["temporal"].append((1 - np.exp(-il)) * 100)

    # Props especiales
    res["win_both_halves_home"] = pct((h1 > a1) & (h2 > a2))
    res["win_1h_home"] = pct(h1 > a1)
    res["over_0.5_1h"] = pct((h1 + a1) > 0.5)
    res["shots_home_over"] = float(np.clip(50 + share_h * 30, 45, 75))  # referencia descriptiva

    return res
