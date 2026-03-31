# worker.py
# Distributed Disaster Intelligence Platform - Worker Node
# Run multiple instances on different ports:
#   python worker.py 5001
#   python worker.py 5002
#   python worker.py 5003

from flask import Flask, request, jsonify
import time
import sys

app = Flask(__name__)

# Critical keywords for emergency detection
CRITICAL_KEYWORDS = [
    "fire", "help", "injured", "urgent", "flood",
    "rescue", "casualties", "trapped", "immediate",
    "emergency", "evacuate", "danger", "collapsed"
]

# Severity scoring based on keywords
SEVERITY_WEIGHTS = {
    "casualties":  5,
    "collapsed":   5,
    "evacuate":    4,
    "trapped":     4,
    "immediate":   4,
    "urgent":      3,
    "fire":        3,
    "flood":       3,
    "injured":     3,
    "emergency":   3,
    "rescue":      2,
    "danger":      2,
    "help":        1
}

def analyze_report(report):
    """Analyze a single emergency report and return structured result."""
    text = report.get("text", "").lower()
    report_id = report.get("id")
    location = report.get("location", "Unknown")

    matched_keywords = [kw for kw in CRITICAL_KEYWORDS if kw in text]
    severity_score = sum(SEVERITY_WEIGHTS.get(kw, 1) for kw in matched_keywords)
    is_critical = len(matched_keywords) > 0

    if severity_score >= 10:
        severity_level = "CRITICAL"
    elif severity_score >= 5:
        severity_level = "HIGH"
    elif severity_score >= 2:
        severity_level = "MEDIUM"
    elif severity_score == 1:
        severity_level = "LOW"
    else:
        severity_level = "NONE"

    return {
        "id":             report_id,
        "location":       location,
        "text":           report.get("text", ""),
        "is_critical":    is_critical,
        "severity_score": severity_score,
        "severity_level": severity_level,
        "keywords_found": matched_keywords
    }

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint so master can verify worker is alive."""
    return jsonify({"status": "alive", "worker_id": worker_id})

@app.route("/process_reports", methods=["POST"])
def process_reports():
    """Receive a chunk of reports, analyze them, return structured results."""
    data = request.get_json()
    if not data or "reports" not in data:
        return jsonify({"error": "No reports provided"}), 400

    reports = data["reports"]
    start = time.time()

    results = [analyze_report(r) for r in reports]

    critical_count  = sum(1 for r in results if r["is_critical"])
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "NONE": 0}
    for r in results:
        severity_counts[r["severity_level"]] += 1

    processing_time = round(time.time() - start, 4)

    return jsonify({
        "worker_id":          worker_id,
        "total_assigned":     len(reports),
        "critical_count":     critical_count,
        "severity_breakdown": severity_counts,
        "processing_time_s":  processing_time,
        "analyzed_reports":   results
    })

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    worker_id = f"Worker-{port}"
    print(f"[{worker_id}] Starting on port {port}...")
    app.run(host="0.0.0.0", port=port)
