# master.py
# Distributed Disaster Intelligence Platform - Master Node
# Run: python master.py

from flask import Flask, request, jsonify, render_template_string
import requests
import json
import threading
import time

app = Flask(__name__)

WORKERS = [
    {"id": "Worker-1", "url": "http://127.0.0.1:5001"},
    {"id": "Worker-2", "url": "http://127.0.0.1:5002"},
    {"id": "Worker-3", "url": "http://127.0.0.1:5003"}
]

DATA_FILE = "reports.json"
results_lock = threading.Lock()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Distributed Disaster Intelligence Platform</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
  header { background: #1e293b; padding: 20px 40px; border-bottom: 2px solid #f43f5e; }
  header h1 { font-size: 1.5rem; color: #f43f5e; }
  header p  { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; }
  .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 30px; }
  .card { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
  .card .label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
  .card .value { font-size: 2rem; font-weight: 700; margin-top: 6px; }
  .red   { color: #f43f5e; }
  .yellow{ color: #facc15; }
  .green { color: #4ade80; }
  .blue  { color: #60a5fa; }
  .btn { background: #f43f5e; color: white; border: none; padding: 14px 32px;
         border-radius: 8px; font-size: 1rem; cursor: pointer; margin-bottom: 24px; transition: 0.2s; }
  .btn:hover { background: #e11d48; }
  .btn:disabled { background: #475569; cursor: not-allowed; }
  .section-title { font-size: 1rem; font-weight: 600; color: #cbd5e1; margin-bottom: 12px; margin-top: 24px; }
  table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; }
  th { background: #334155; padding: 12px 16px; text-align: left; font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; }
  td { padding: 12px 16px; border-bottom: 1px solid #334155; font-size: 0.85rem; }
  tr:last-child td { border-bottom: none; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
  .badge-critical { background: #7f1d1d; color: #fca5a5; }
  .badge-high     { background: #78350f; color: #fcd34d; }
  .badge-medium   { background: #1e3a5f; color: #93c5fd; }
  .badge-low      { background: #1a2e1a; color: #86efac; }
  .badge-none     { background: #1e293b; color: #64748b; }
  .worker-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .worker-card { background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 16px; }
  .worker-card h3 { font-size: 0.9rem; margin-bottom: 10px; color: #60a5fa; }
  .worker-stat { display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-top: 4px; }
  #status { font-size: 0.85rem; color: #94a3b8; margin-bottom: 16px; display:block; }
  #log { background: #0f172a; border: 1px solid #334155; border-radius: 8px;
         padding: 14px; font-size: 0.78rem; color: #94a3b8; max-height: 150px; overflow-y: auto;
         font-family: monospace; margin-top: 12px; white-space: pre-wrap; }
</style>
</head>
<body>
<header>
  <h1>Distributed Disaster Intelligence Platform</h1>
  <p>Master Node -- Fault-Tolerant Distributed Emergency Report Processing</p>
</header>
<div class="container">
  <button class="btn" id="runBtn" onclick="runProcessing()">Start Distributed Processing</button>
  <span id="status">Waiting to start...</span>

  <div class="grid">
    <div class="card"><div class="label">Total Reports</div><div class="value blue" id="total">--</div></div>
    <div class="card"><div class="label">Critical Incidents</div><div class="value red" id="critical">--</div></div>
    <div class="card"><div class="label">Active Workers</div><div class="value green" id="workers">--</div></div>
    <div class="card"><div class="label">Processing Time</div><div class="value yellow" id="ptime">--</div></div>
  </div>

  <div class="section-title">Worker Node Performance</div>
  <div class="worker-grid">
    <div class="worker-card"><h3>Worker-1</h3>
      <div class="worker-stat"><span>Assigned</span><span id="w1a">--</span></div>
      <div class="worker-stat"><span>Critical</span><span id="w1c">--</span></div>
    </div>
    <div class="worker-card"><h3>Worker-2</h3>
      <div class="worker-stat"><span>Assigned</span><span id="w2a">--</span></div>
      <div class="worker-stat"><span>Critical</span><span id="w2c">--</span></div>
    </div>
    <div class="worker-card"><h3>Worker-3</h3>
      <div class="worker-stat"><span>Assigned</span><span id="w3a">--</span></div>
      <div class="worker-stat"><span>Critical</span><span id="w3c">--</span></div>
    </div>
  </div>

  <div class="section-title">Emergency Report Analysis</div>
  <table>
    <thead>
      <tr>
        <th>#</th><th>Location</th><th>Description</th>
        <th>Severity</th><th>Keywords</th><th>Assigned To</th>
      </tr>
    </thead>
    <tbody id="reportTable">
      <tr><td colspan="6" style="text-align:center;color:#64748b;">Run processing to see results</td></tr>
    </tbody>
  </table>

  <div id="log">[LOG] System ready. Press Start to begin distributed processing.</div>
</div>

<script>
function log(msg) {
  const el = document.getElementById("log");
  const ts = new Date().toLocaleTimeString();
  el.textContent += "\\n[" + ts + "] " + msg;
  el.scrollTop = el.scrollHeight;
}

function badgeClass(level) {
  const map = {CRITICAL:"badge-critical",HIGH:"badge-high",MEDIUM:"badge-medium",LOW:"badge-low",NONE:"badge-none"};
  return map[level] || "badge-none";
}

async function runProcessing() {
  const btn = document.getElementById("runBtn");
  btn.disabled = true;
  document.getElementById("status").textContent = "Processing... please wait";
  log("Sending request to master node...");

  try {
    const res = await fetch("/process_all", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({})
    });

    if (!res.ok) {
      const err = await res.text();
      log("ERROR from server: " + err);
      document.getElementById("status").textContent = "Error. Check log.";
      return;
    }

    const data = await res.json();
    if (data.error) { log("ERROR: " + data.error); return; }

    const s = data.summary;
    document.getElementById("total").textContent    = s.total_reports;
    document.getElementById("critical").textContent = s.total_critical;
    document.getElementById("workers").textContent  = data.active_workers + "/" + data.num_workers;
    document.getElementById("ptime").textContent    = data.processing_time_s + "s";

    s.per_worker.forEach(function(w, i) {
      const n = i + 1;
      const wa = document.getElementById("w"+n+"a");
      const wc = document.getElementById("w"+n+"c");
      if (wa) wa.textContent = w.total_assigned;
      if (wc) wc.textContent = w.critical_count;
    });

    const tbody = document.getElementById("reportTable");
    tbody.innerHTML = "";
    data.all_results.forEach(function(r) {
      const kws = (r.keywords_found && r.keywords_found.length) ? r.keywords_found.join(", ") : "none";
      const shortText = r.text.length > 55 ? r.text.substring(0, 55) + "..." : r.text;
      tbody.innerHTML += "<tr>" +
        "<td>" + r.id + "</td>" +
        "<td>" + r.location + "</td>" +
        "<td>" + shortText + "</td>" +
        "<td><span class='badge " + badgeClass(r.severity_level) + "'>" + r.severity_level + "</span></td>" +
        "<td style='color:#94a3b8;font-size:0.75rem'>" + kws + "</td>" +
        "<td style='color:#60a5fa'>" + (r.assigned_worker || "--") + "</td>" +
        "</tr>";
    });

    log("Done! " + s.total_critical + " critical out of " + s.total_reports + " reports.");
    log("Active workers: " + data.active_workers + " | Time: " + data.processing_time_s + "s");
    document.getElementById("status").textContent = "Done. " + s.total_critical + " critical incidents found.";

  } catch(err) {
    log("FETCH ERROR: " + err.message);
    document.getElementById("status").textContent = "Request failed. See log.";
  } finally {
    btn.disabled = false;
  }
}
</script>
</body>
</html>
"""

def load_reports():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def partition_data(data, num_chunks):
    size = max(1, len(data) // num_chunks)
    chunks = []
    for i in range(0, len(data), size):
        chunks.append(data[i:i + size])
    return chunks

def check_worker_health(worker):
    try:
        r = requests.get(worker["url"] + "/health", timeout=2)
        return r.status_code == 200
    except:
        return False

def send_to_worker(worker, chunk, results_store, failed_chunks):
    try:
        resp = requests.post(
            worker["url"] + "/process_reports",
            json={"reports": chunk},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        for report in data.get("analyzed_reports", []):
            report["assigned_worker"] = worker["id"]
        with results_lock:
            results_store.append(data)
        print("[MASTER] " + worker["id"] + " processed " + str(data["total_assigned"]) + " reports. Critical: " + str(data["critical_count"]))
    except Exception as e:
        print("[MASTER] FAILED " + worker["id"] + ": " + str(e))
        with results_lock:
            failed_chunks.append((worker["id"], chunk))

@app.route("/")
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "master running"})

@app.route("/process_all", methods=["POST"])
def process_all():
    start_time = time.time()

    try:
        reports = load_reports()
    except Exception as e:
        return jsonify({"error": "Could not load reports.json: " + str(e)}), 500

    alive_workers = [w for w in WORKERS if check_worker_health(w)]
    dead_workers  = [w for w in WORKERS if not check_worker_health(w)]

    print("[MASTER] Alive: " + str([w["id"] for w in alive_workers]))
    if dead_workers:
        print("[MASTER] Dead: " + str([w["id"] for w in dead_workers]))

    if not alive_workers:
        return jsonify({"error": "No worker nodes available. Start workers first."}), 503

    partitions    = partition_data(reports, len(alive_workers))
    results_store = []
    failed_chunks = []

    threads = []
    for worker, chunk in zip(alive_workers, partitions):
        t = threading.Thread(target=send_to_worker, args=(worker, chunk, results_store, failed_chunks))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    for original_id, chunk in failed_chunks:
        for fallback in alive_workers:
            if fallback["id"] != original_id:
                print("[MASTER] Reassigning chunk from " + original_id + " to " + fallback["id"])
                send_to_worker(fallback, chunk, results_store, [])
                break

    total_reports  = sum(r["total_assigned"]  for r in results_store)
    total_critical = sum(r["critical_count"]  for r in results_store)
    all_results    = [rep for r in results_store for rep in r.get("analyzed_reports", [])]
    all_results.sort(key=lambda x: x.get("severity_score", 0), reverse=True)

    per_worker = [{
        "worker_id":      r["worker_id"],
        "total_assigned": r["total_assigned"],
        "critical_count": r["critical_count"]
    } for r in results_store]

    return jsonify({
        "summary": {
            "total_reports":  total_reports,
            "total_critical": total_critical,
            "per_worker":     per_worker
        },
        "all_results":       all_results,
        "processing_time_s": round(time.time() - start_time, 3),
        "num_workers":       len(WORKERS),
        "active_workers":    len(alive_workers),
        "failed_workers":    [w["id"] for w in dead_workers]
    })
@app.route("/process_all_get", methods=["GET"])
def process_all_get():
    return process_all()


if __name__ == "__main__":
    print("[MASTER] Starting Distributed Disaster Intelligence Platform...")
    print("[MASTER] Dashboard: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=8080, debug=False)
