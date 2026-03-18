import os
import pandas as pd
import math
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, "ernakulam_crime_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "crime_ai_model.pkl")

# ===============================
# Distance calculation (Haversine)
# ===============================
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# ===============================
# Load ML model
# ===============================
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return pickle.load(open(MODEL_PATH, "rb"))


# ===============================
# Core AI prediction
# ===============================
def predict_risk(user_lat, user_lon, radius_km=4):
    df = pd.read_csv(CSV_PATH)

    nearby = []

    # 🔹 Find crimes within radius
    for _, row in df.iterrows():
        dist = calculate_distance(
            user_lat,
            user_lon,
            row["latitude"],
            row["longitude"]
        )

        if dist <= radius_km:
            row_dict = row.to_dict()
            row_dict["distance"] = round(dist, 2)
            nearby.append(row_dict)

    if not nearby:
        return {
            "status": "no_data",
            "message": f"No crime data within {radius_km} KM"
        }

    # 🔹 Nearest place
    nearest = sorted(nearby, key=lambda x: x["distance"])[0]
    nearest_place = nearest["place"]

    # 🔹 Crimes ONLY for nearest place
    place_crimes = [x for x in nearby if x["place"] == nearest_place]

    crime_count = len(place_crimes)
    avg_risk = sum(x["risk_level"] for x in place_crimes) / crime_count

    # 🔹 ML prediction
    model = load_model()

    if model:
        X_pred = pd.DataFrame(
            [[crime_count, avg_risk]],
            columns=["crime_count", "avg_risk"]
        )
        pred = model.predict(X_pred)[0]

        risk_label = (
            "HIGH" if pred == 2 else
            "MEDIUM" if pred == 1 else
            "LOW"
        )
    else:
        # fallback rule-based
        if avg_risk >= 7:
            risk_label = "HIGH"
        elif avg_risk >= 4:
            risk_label = "MEDIUM"
        else:
            risk_label = "LOW"

    # 🔹 Crime types ONLY for nearest place
    crime_types = list(set(x["crime_type"] for x in place_crimes))

    return {
        "status": "success",
        "nearest_place": nearest_place,
        "distance_km": nearest["distance"],
        "crime_count": crime_count,
        "average_risk": round(avg_risk, 2),
        "predicted_risk": risk_label,
        "crime_types": crime_types
    }
