import flask
from flask_cors import CORS
import llmservice
import base64
import json
import os

app = flask.Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")

def read_db():
    if not os.path.exists(DB_PATH):
        return {"jadwal": [], "history": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def write_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_schedules(start_time, interval_h, count=5):
    """Generate repeated schedule time slots from a start time and interval."""
    h, m = map(int, start_time.split(":"))
    schedules = []
    for i in range(count):
        new_h = (h + i * interval_h) % 24
        time_str = f"{new_h:02d}:{m:02d}"
        period = "Pagi" if new_h < 12 else "Siang" if new_h < 18 else "Malam"
        icon = "sun" if period == "Pagi" else "cloud"
        schedules.append({
            "id": i + 1,
            "time": time_str,
            "period": period,
            "instruction": "Sesudah Makan",
            "icon": icon,
            "isActive": True
        })
    return schedules

# ─── Image Recognition ───────────────────────────────────────────────

@app.route("/recognize", methods=["POST"])
def recognize():
    req_json = flask.request.json
    a = base64.b64decode(req_json["image"].split(",")[1])
    print(a)
    res = json.loads(str(llmservice.dollm(a)))

    if "error" in res:
        return {"status": "error"}
    return {
        "status" : "ok",
        "data" : res
    }

# ─── Jadwal (Schedule) Endpoints ─────────────────────────────────────

@app.route("/api/schedules", methods=["GET"])
def get_schedules():
    """Return list of all jadwal entries.
    'time' is the next closest consumption time relative to now."""
    from datetime import datetime
    now = datetime.now()
    now_minutes = now.hour * 60 + now.minute  # current time in minutes since midnight

    db = read_db()
    jadwal_list = db.get("jadwal", [])
    result = []
    for j in jadwal_list:
        sub = j.get("jadwal", [])
        next_time = sub[0]["time"] if sub else "00:00"

        if sub:
            # Find the next closest time that is >= now (today), or wrap to tomorrow
            best_diff = None
            for s in sub:
                h, m = map(int, s["time"].split(":"))
                t_minutes = h * 60 + m
                diff = t_minutes - now_minutes
                if diff < 0:
                    diff += 24 * 60  # wrap to next day
                if best_diff is None or diff < best_diff:
                    best_diff = diff
                    next_time = s["time"]

        result.append({
            "id": j["id"],
            "name": j["name"],
            "dose": j.get("dose", ""),
            "qty": j.get("qty", ""),
            "time": next_time
        })
    return flask.jsonify(result)

@app.route("/api/schedules/<int:sched_id>", methods=["GET"])
def get_schedule_detail(sched_id):
    """Return full detail for a single jadwal entry (image, nextDose, sub-jadwal list)."""
    db = read_db()
    jadwal_list = db.get("jadwal", [])
    jadwal = next((j for j in jadwal_list if j["id"] == sched_id), None)
    if not jadwal:
        return flask.jsonify({"error": "Not found"}), 404

    sub = jadwal.get("jadwal", [])
    first_time = sub[0]["time"] if sub else "00:00"
    h = int(first_time.split(":")[0])
    period = "Pagi" if h < 12 else "Siang" if h < 18 else "Malam"

    return flask.jsonify({
        "image": jadwal.get("image", f"https://placehold.co/600x400/pink/white?text={jadwal['name']}"),
        "nextDose": {
            "countdown": f"{jadwal.get('interval_h', 4)}:00:00",
            "time": first_time,
            "period": period,
            "instruction": "Sesudah Makan",
            "interval_h": jadwal.get("interval_h", 0)
        },
        "schedules": sub,
        "all_desc": jadwal.get("all_desc", "")
    })

@app.route("/api/schedules", methods=["POST"])
def add_schedule():
    """Create a new jadwal entry from a detection.
    Also appends a history record with the full POST body."""
    req = flask.request.json
    db = read_db()
    jadwal_list = db.get("jadwal", [])

    new_id = max([j["id"] for j in jadwal_list], default=0) + 1

    name = req.get("name", "Obat Baru")
    time = req.get("time", "08:00")
    dose = req.get("dose", "1 Tablet")
    qty = req.get("qty", "1 Tablet")
    interval_h = req.get("interval_h", 0)
    all_desc = req.get("all_desc", "")
    image_url = req.get("image", f"https://placehold.co/600x400/pink/white?text={name}")

    # Generate sub-jadwal time slots
    sub_jadwal = generate_schedules(time, interval_h, 5)

    jadwal_list.append({
        "id": new_id,
        "name": name,
        "dose": dose,
        "qty": qty,
        "image": image_url,
        "interval_h": interval_h,
        "all_desc": all_desc,
        "jadwal": sub_jadwal
    })
    db["jadwal"] = jadwal_list

    # Append to history (store the full POST body)
    history = db.get("history", [])
    new_hist_id = max([h["id"] for h in history], default=0) + 1
    history.append({
        "id": new_hist_id,
        "name": name,
        "image": None,
        "bahanAktif": req.get("bahanAktif", ""),
        "manfaat": req.get("manfaat", []),
        "dosis": dose,
        "peringatan": req.get("peringatan", ""),
        "penyimpanan": req.get("penyimpanan", ""),
        "all_desc": all_desc,
        "detected_at": time
    })
    db["history"] = history

    write_db(db)
    return flask.jsonify({"status": "ok", "id": new_id})

@app.route("/api/schedules/<int:sched_id>/toggle", methods=["POST"])
def toggle_schedule(sched_id):
    """Toggle isActive on a sub-jadwal entry."""
    req = flask.request.json
    sub_sched_id = req.get("sub_schedule_id")

    db = read_db()
    jadwal_list = db.get("jadwal", [])
    jadwal = next((j for j in jadwal_list if j["id"] == sched_id), None)

    if jadwal and "jadwal" in jadwal:
        for s in jadwal["jadwal"]:
            if s["id"] == sub_sched_id:
                s["isActive"] = not s["isActive"]
                break
        write_db(db)
        return flask.jsonify({"status": "ok", "jadwal": jadwal})

    return flask.jsonify({"error": "Schedule not found"}), 404

# ─── History Endpoints ────────────────────────────────────────────────

@app.route("/api/history", methods=["GET"])
def get_history():
    db = read_db()
    return flask.jsonify(db.get("history", []))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
