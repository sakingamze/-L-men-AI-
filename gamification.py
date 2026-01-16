# gamification.py

import json
import os
from datetime import datetime
#henüz çok temel ve basit bir yapıda güncellenmesi lazım daha fazla tecrübe edinmem lazım 
# Kullanıcı puan ve rozet verilerini saklama
# --------------------
DATA_FILE = "gamification_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --------------------
# Puan ekleme
# --------------------
def add_points(username, role, points):
    data = load_data()
    if username not in data:
        data[username] = {"total_points": 0, "badges": [], "history": []}
    data[username]["total_points"] += points
    data[username]["history"].append({
        "date": str(datetime.now()),
        "points": points,
        "role": role
    })
    save_data(data)
    return data[username]["total_points"]

# --------------------
# Rozet kazanma

def award_badge(username, badge_name):
    data = load_data()
    if username not in data:
        data[username] = {"total_points": 0, "badges": [], "history": []}
    if badge_name not in data[username]["badges"]:
        data[username]["badges"].append(badge_name)
        save_data(data)
        return True
    return False

# --------------------
# Motivasyon mesajları
# --------------------
def get_motivation(username, role, points_earned):
    messages_junior = [
        f"Hey {username}! Bugün hata yapan {points_earned} Junior’dan birisin, bu çok normal devam et",
        "Her hata bir öğrenme fırsatıdır ",
        "Kod yolculuğunda adımlarını güçlendirdin! "
    ]
    messages_senior = [
        f"{username}, profesyonel bir Senior olarak {points_earned} puan kazandın. Harika iş! ",
        "Kodunu optimize etmeye devam et, uzmanlık yolunda ilerliyorsun! "
    ]
    import random
    if role.lower() == "junior":
        return random.choice(messages_junior)
    else:
        return random.choice(messages_senior)

# --------------------
# Kullanıcı bilgilerini alma
# --------------------
def get_user_stats(username):
    data = load_data()
    if username not in data:
        return {"total_points": 0, "badges": [], "history": []}
    return data[username]

# --------------------
# Örnek rozet kazanma kuralları
# --------------------
def evaluate_badges(username):
    stats = get_user_stats(username)
    badges_awarded = []
    
    # 100 puana ulaşanlara "Rising Star" rozeti
    if stats["total_points"] >= 100 and "Rising Star" not in stats["badges"]:
        award_badge(username, "Rising Star")
        badges_awarded.append("Rising Star")
    
    # 500 puana ulaşanlara "Code Master"
    if stats["total_points"] >= 500 and "Code Master" not in stats["badges"]:
        award_badge(username, "Code Master")
        badges_awarded.append("Code Master")
    
    return badges_awarded
