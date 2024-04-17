import pandas as pd
import numpy as np
import json


def adjust_fields(scores):
    scores["pos_local"] = scores["pos_local"].fillna(0).astype(int)
    scores["pos_visitante"] = scores["pos_visitante"].fillna(0).astype(int)
    scores["fecha"] = pd.to_datetime(scores["fecha"])
    scores["dia"] = scores["fecha"].dt.dayofweek
    scores["result"] = ""
    for i in range(0, scores.shape[0]):
        if scores["gana_local"][i] == True:
            scores["result"][i] = "Local"
        elif scores["empate"][i] == True:
            scores["result"][i] = "Empate"
        elif scores["gana_visitante"][i] == True:
            scores["result"][i] = "Visitante"
        else:
            scores["result"][i] = np.nan
    scores = scores.sort_values("fecha")
    scores = scores.reset_index(drop=True)
    scores["gol_favor_local_local_6_matches"] = np.nan
    scores["gol_favor_local_visit_6_matches"] = np.nan
    scores["gol_favor_visit_local_6_matches"] = np.nan
    scores["gol_favor_visit_visit_6_matches"] = np.nan

    scores["gol_contra_local_local_6_matches"] = np.nan
    scores["gol_contra_local_visit_6_matches"] = np.nan
    scores["gol_contra_visit_local_6_matches"] = np.nan
    scores["gol_contra_visit_visit_6_matches"] = np.nan

    scores["vict_local_local_6_matches"] = np.nan
    scores["vict_local_visit_6_matches"] = np.nan
    scores["vict_visit_local_6_matches"] = np.nan
    scores["vict_visit_visit_6_matches"] = np.nan

    scores["emp_local_local_6_matches"] = np.nan
    scores["emp_local_visit_6_matches"] = np.nan
    scores["emp_visit_local_6_matches"] = np.nan
    scores["emp_visit_visit_6_matches"] = np.nan

    scores["los_local_local_6_matches"] = np.nan
    scores["los_local_visit_6_matches"] = np.nan
    scores["los_visit_local_6_matches"] = np.nan
    scores["los_visit_visit_6_matches"] = np.nan

    scores["vict_local_igual_6_dire_matches"] = np.nan
    scores["emp_local_igual_6_dire_matches"] = np.nan
    scores["los_local_igual_6_dire_matches"] = np.nan
    scores["vict_local_dif_6_dire_matches"] = np.nan
    scores["emp_local_dif_6_dire_matches"] = np.nan
    scores["los_local_dif_6_dire_matches"] = np.nan

    scores["gol_favor_local_local_3_matches"] = np.nan
    scores["gol_favor_local_visit_3_matches"] = np.nan
    scores["gol_favor_visit_local_3_matches"] = np.nan
    scores["gol_favor_visit_visit_3_matches"] = np.nan

    scores["gol_contra_local_local_3_matches"] = np.nan
    scores["gol_contra_local_visit_3_matches"] = np.nan
    scores["gol_contra_visit_local_3_matches"] = np.nan
    scores["gol_contra_visit_visit_3_matches"] = np.nan

    scores["vict_local_local_3_matches"] = np.nan
    scores["vict_local_visit_3_matches"] = np.nan
    scores["vict_visit_local_3_matches"] = np.nan
    scores["vict_visit_visit_3_matches"] = np.nan

    scores["emp_local_local_3_matches"] = np.nan
    scores["emp_local_visit_3_matches"] = np.nan
    scores["emp_visit_local_3_matches"] = np.nan
    scores["emp_visit_visit_3_matches"] = np.nan

    scores["los_local_local_3_matches"] = np.nan
    scores["los_local_visit_3_matches"] = np.nan
    scores["los_visit_local_3_matches"] = np.nan
    scores["los_visit_visit_3_matches"] = np.nan

    scores["vict_local_igual_3_dire_matches"] = np.nan
    scores["emp_local_igual_3_dire_matches"] = np.nan
    scores["los_local_igual_3_dire_matches"] = np.nan
    scores["vict_local_dif_3_dire_matches"] = np.nan
    scores["emp_local_dif_3_dire_matches"] = np.nan
    scores["los_local_dif_3_dire_matches"] = np.nan

    scores["cuota_local"] = ""
    scores["cuota_empate"] = ""
    scores["cuota_visitante"] = ""

    return scores

def sliding_filling_for_pred(scores, historical):
    for i in range(1, scores.shape[0]):
        scores["gol_favor_local_local_6_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(6)["goles_local"].mean()
        scores["gol_favor_local_visit_6_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(6)["goles_visitante"].mean()
        scores["gol_favor_visit_local_6_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(6)["goles_local"].mean()
        scores["gol_favor_visit_visit_6_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(6)["goles_visitante"].mean()

        scores["gol_contra_local_local_6_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(6)["goles_visitante"].mean()
        scores["gol_contra_local_visit_6_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(6)["goles_local"].mean()
        scores["gol_contra_visit_local_6_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(6)["goles_visitante"].mean()
        scores["gol_contra_visit_visit_6_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(6)["goles_local"].mean()

        scores["vict_local_local_6_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(6)["gana_local"].mean()
        scores["vict_local_visit_6_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(6)["gana_visitante"].mean()
        scores["vict_visit_local_6_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(6)["gana_local"].mean()
        scores["vict_visit_visit_6_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(6)["gana_visitante"].mean()

        scores["emp_local_local_6_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(6)["empate"].mean()
        scores["emp_local_visit_6_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(6)["empate"].mean()
        scores["emp_visit_local_6_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(6)["empate"].mean()
        scores["emp_visit_visit_6_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(6)["empate"].mean()

        scores["los_local_local_6_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(6)["gana_visitante"].mean()
        scores["los_local_visit_6_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(6)["gana_local"].mean()
        scores["los_visit_local_6_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(6)["gana_visitante"].mean()
        scores["los_visit_visit_6_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(6)["gana_local"].mean()

        scores["vict_local_igual_6_dire_matches"][i] = historical[(historical["local"]==scores["local"][i])][(historical["visitante"]==scores["visitante"][i])].tail(6)["gana_local"].mean()
        scores["emp_local_igual_6_dire_matches"][i] = historical[(historical["local"]==scores["local"][i])][(historical["visitante"]==scores["visitante"][i])].tail(6)["empate"].mean()
        scores["los_local_igual_6_dire_matches"][i] = historical[(historical["local"]==scores["local"][i])][(historical["visitante"]==scores["visitante"][i])].tail(6)["gana_local"].mean()
        scores["vict_local_dif_6_dire_matches"][i] = historical[(historical["visitante"]==scores["local"][i])][(historical["local"]==scores["visitante"][i])].tail(6)["gana_visitante"].mean()
        scores["emp_local_dif_6_dire_matches"][i] = historical[(historical["visitante"]==scores["local"][i])][(historical["local"]==scores["visitante"][i])].tail(6)["empate"].mean()
        scores["los_local_dif_6_dire_matches"][i] = historical[(historical["visitante"]==scores["local"][i])][(historical["local"]==scores["visitante"][i])].tail(6)["gana_visitante"].mean()

        scores["gol_favor_local_local_3_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(3)["goles_local"].mean()
        scores["gol_favor_local_visit_3_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(3)["goles_visitante"].mean()
        scores["gol_favor_visit_local_3_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(3)["goles_local"].mean()
        scores["gol_favor_visit_visit_3_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(3)["goles_visitante"].mean()

        scores["gol_contra_local_local_3_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(3)["goles_visitante"].mean()
        scores["gol_contra_local_visit_3_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(3)["goles_local"].mean()
        scores["gol_contra_visit_local_3_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(3)["goles_visitante"].mean()
        scores["gol_contra_visit_visit_3_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(3)["goles_local"].mean()

        scores["vict_local_local_3_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(3)["gana_local"].mean()
        scores["vict_local_visit_3_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(3)["gana_visitante"].mean()
        scores["vict_visit_local_3_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(3)["gana_local"].mean()
        scores["vict_visit_visit_3_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(3)["gana_visitante"].mean()

        scores["emp_local_local_3_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(3)["empate"].mean()
        scores["emp_local_visit_3_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(3)["empate"].mean()
        scores["emp_visit_local_3_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(3)["empate"].mean()
        scores["emp_visit_visit_3_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(3)["empate"].mean()

        scores["los_local_local_3_matches"][i] = historical[historical["local"]==scores["local"][i]].tail(3)["gana_visitante"].mean()
        scores["los_local_visit_3_matches"][i] = historical[historical["visitante"]==scores["local"][i]].tail(3)["gana_local"].mean()
        scores["los_visit_local_3_matches"][i] = historical[historical["local"]==scores["visitante"][i]].tail(3)["gana_visitante"].mean()
        scores["los_visit_visit_3_matches"][i] = historical[historical["visitante"]==scores["visitante"][i]].tail(3)["gana_local"].mean()

        scores["vict_local_igual_3_dire_matches"][i] = historical[(historical["local"]==scores["local"][i])][(historical["visitante"]==scores["visitante"][i])].tail(3)["gana_local"].mean()
        scores["emp_local_igual_3_dire_matches"][i] = historical[(historical["local"]==scores["local"][i])][(historical["visitante"]==scores["visitante"][i])].tail(3)["empate"].mean()
        scores["los_local_igual_3_dire_matches"][i] = historical[(historical["local"]==scores["local"][i])][(historical["visitante"]==scores["visitante"][i])].tail(3)["gana_local"].mean()
        scores["vict_local_dif_3_dire_matches"][i] = historical[(historical["visitante"]==scores["local"][i])][(historical["local"]==scores["visitante"][i])].tail(3)["gana_visitante"].mean()
        scores["emp_local_dif_3_dire_matches"][i] = historical[(historical["visitante"]==scores["local"][i])][(historical["local"]==scores["visitante"][i])].tail(3)["empate"].mean()
        scores["los_local_dif_3_dire_matches"][i] = historical[(historical["visitante"]==scores["local"][i])][(historical["local"]==scores["visitante"][i])].tail(3)["gana_visitante"].mean()

    return scores

def fill_cuotas(cuotas, scores):
    try:
        with open("equipos.conf") as config:
            equipos = json.load(config)
    except FileNotFoundError as e:
        print("Error: The file 'equipos.conf' was not found.")
        raise e

    for i in range(scores.shape[0]):
        scores["local"][i] = equipos.get(scores["local"][i])
        scores["visitante"][i] = equipos.get(scores["visitante"][i])
    cuotas['datetime'] = pd.to_datetime(cuotas['datetime'])
    cuotas = cuotas.sort_values("datetime")
    cuotas["date_lecture"] = ""
    scores['fecha'] = pd.to_datetime(scores['fecha'])
    for i in range(cuotas.shape[0]):
        cuotas["date_lecture"][i] = cuotas['datetime'][i].date()
    for i in range(scores.shape[0]):
        if cuotas[(cuotas["date_lecture"] <= scores["fecha"][i]) & (cuotas["local"] == scores["local"][i]) & (cuotas["visitante"] == scores["visitante"][i])].shape[0] >= 1:
            scores.loc[i,"cuota_local"] = cuotas[(cuotas["date_lecture"] <= scores["fecha"][i]) & (cuotas["local"] == scores["local"][i]) & (cuotas["visitante"] == scores["visitante"][i])].iloc[-1]["cuota_local"]
            scores.loc[i,"cuota_visitante"] = cuotas[(cuotas["date_lecture"] <= scores["fecha"][i]) & (cuotas["local"] == scores["local"][i]) & (cuotas["visitante"] == scores["visitante"][i])].iloc[-1]["cuota_visitante"]
            scores.loc[i,"cuota_empate"] = cuotas[(cuotas["date_lecture"] <= scores["fecha"][i]) & (cuotas["local"] == scores["local"][i]) & (cuotas["visitante"] == scores["visitante"][i])].iloc[-1]["cuota_empate"]
    return scores

def main():
    # load properties from configuration file
    try:
        with open("config_file.conf") as config:
            conf = json.load(config)
    except FileNotFoundError as e:
        print("Error: The file 'config_file.conf' was not found.")
        raise e
    cuotas = pd.read_csv(conf["cuotas_file"])
    scores = pd.read_csv(conf["scores_file"])
    historical = pd.read_csv(conf["historical_scores_file"])
    adjusted_scores = adjust_fields(scores)
    scores_sliding = sliding_filling_for_pred(adjusted_scores, historical)
    complete_scores = fill_cuotas(cuotas, scores_sliding)        
    complete_scores.to_csv(conf["ready_to_predict_file"],index=False)    

if __name__ == "__main__":
    # the program execution starts here with the main method
    main()
