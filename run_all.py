# run_all.py
import subprocess
import sys
import time

def start_process(script, args=[]):
    return subprocess.Popen(
        [sys.executable, script] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

if __name__ == "__main__":
    print("=" * 55)
    print("  Distributed Disaster Intelligence Platform")
    print("=" * 55)

    procs = []
    print("[LAUNCHER] Starting Worker-1 on port 5001...")
    procs.append(start_process("worker.py", ["5001"]))
    time.sleep(0.5)

    print("[LAUNCHER] Starting Worker-2 on port 5002...")
    procs.append(start_process("worker.py", ["5002"]))
    time.sleep(0.5)

    print("[LAUNCHER] Starting Worker-3 on port 5003...")
    procs.append(start_process("worker.py", ["5003"]))
    time.sleep(1)

    print("[LAUNCHER] Starting Master Node on port 5000...")
    procs.append(start_process("master.py"))
    time.sleep(1.5)

    print()
    print("[OK] All nodes started!")
    print("[OK] Open in browser: http://127.0.0.1:5000")
    print()
    print("Press Ctrl+C to stop all nodes.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[LAUNCHER] Stopping all nodes...")
        for p in procs:
            p.terminate()
        print("[LAUNCHER] All nodes stopped.")
