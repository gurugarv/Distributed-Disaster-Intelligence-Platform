# Distributed Disaster Intelligence Platform 🚨

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask)
![Distributed Systems](https://img.shields.io/badge/Distributed-Computing-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Working-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> A premium mini-project README for a **fault-tolerant distributed disaster report analysis system** built with Python, Flask, and multiple worker nodes.

---

## 📌 Overview

The **Distributed Disaster Intelligence Platform** is a mini project based on distributed computing concepts. It simulates a real-world emergency response system where multiple worker nodes process disaster reports in parallel, while a master node manages task distribution, health monitoring, aggregation, and fault tolerance.

This project demonstrates:
- Distributed architecture
- Parallel processing
- Worker health monitoring
- Fault tolerance and reassignment
- Real-time dashboard reporting
- Severity-based emergency prioritization

---

## ✨ Features

- **Master-Worker Architecture** for distributed processing
- **3 Independent Worker Nodes** running on separate ports
- **Parallel Report Processing** for faster execution
- **Automatic Health Checks** before assigning tasks
- **Fault Tolerance** through worker failure detection and reassignment
- **Severity Scoring Engine** using emergency keywords
- **Interactive Web Dashboard** with modern UI
- **Live Worker Status Monitoring**
- **Sorted Results Table** based on severity
- **One-Click Launcher** using `run_all.py`

---

## 🏗️ System Architecture

```text
                    +---------------------------+
                    |       Master Node         |
                    |       Port: 8080          |
                    |---------------------------|
                    | - Health Check            |
                    | - Data Partitioning       |
                    | - Result Aggregation      |
                    | - Fault Tolerance         |
                    | - Web Dashboard           |
                    +------------+--------------+
                                 |
        ---------------------------------------------------------
        |                         |                            |
        v                         v                            v
+---------------+        +---------------+            +---------------+
|   Worker-1    |        |   Worker-2    |            |   Worker-3    |
|   Port: 5001  |        |   Port: 5002  |            |   Port: 5003  |
|---------------|        |---------------|            |---------------|
| Analyze chunk |        | Analyze chunk |            | Analyze chunk |
| Score reports |        | Score reports |            | Score reports |
+---------------+        +---------------+            +---------------+

                    +---------------------------+
                    |       reports.json        |
                    |   Emergency report data   |
                    +---------------------------+
🧠 How It Works
	1.	The master node loads all reports from  reports.json .
	2.	It checks which worker nodes are alive using  /health .
	3.	The report dataset is split into chunks.
	4.	Chunks are sent to alive workers in parallel.
	5.	Each worker analyzes reports using disaster-related keywords.
	6.	Severity levels are assigned:
	•	 CRITICAL 
	•	 HIGH 
	•	 MEDIUM 
	•	 LOW 
	•	 NONE 
	7.	The master aggregates results and sorts them by severity score.
	8.	If any worker fails, its chunk is reassigned to another active worker.
	9.	Final results are displayed in the dashboard.
🚀 Tech Stack
	•	Python 3
	•	Flask
	•	Requests
	•	HTML / CSS / JavaScript
	•	JSON
	•	Threading
<img width="651" height="154" alt="Screenshot 2026-04-02 at 10 09 17 PM" src="https://github.com/user-attachments/assets/476601de-0686-4afa-92dd-0824312cf01c" />
⚙️ Installation
1. Clone the repository
git clone https://github.com/your-username/distributed-disaster-platform.git
cd distributed-disaster-platform
2. Install dependencies
pip3 install -r requirements.txt

▶️ Run the Project
Option 1: Run everything together
python3 run_all.py
🌐 Open in Browser
Once the master starts, open:
http://127.0.0.1:8080/

📊 Dashboard Highlights
The dashboard provides:
	•	Total reports processed
	•	Total critical incidents found
	•	Active worker count
	•	Processing time
	•	Individual worker statistics
	•	Real-time logs
	•	Complete severity-sorted emergency report table

Detected keywords:
	•	injured
	•	rescue
	•	immediate
	•	collapsed
Assigned severity:
	•	CRITICAL
🛡️ Fault Tolerance
This project includes a simple but effective fault-tolerance mechanism.
If one worker node fails:
	•	the master detects it during health checks
	•	failed chunks are identified
	•	the task is reassigned to another alive worker
	•	processing continues without complete system failure
This demonstrates one of the core principles of distributed systems.
📈 Learning Outcomes
This project helps understand:
	•	Distributed system design
	•	Task partitioning
	•	Fault tolerance
	•	Service health monitoring
	•	Parallel execution
	•	Result aggregation
	•	Client-server communication using REST APIs
	•	Dashboard-based monitoring
🎓 Use Cases
Although this is a mini project, the idea can be extended to:
	•	Emergency response systems
	•	Disaster management dashboards
	•	Smart city alert platforms
	•	Hospital emergency triage systems
	•	Real-time distributed analytics systems
🔮 Future Improvements
	•	Auto-start worker nodes from the master
	•	Database integration instead of JSON
	•	Real-time updates with WebSockets
	•	Docker-based deployment
	•	Cloud deployment with multiple machines
	•	Authentication for admin dashboard
	•	Advanced analytics and graphs
	•	AI/NLP-based report classification
🤝 Contributing
Contributions are welcome.
	1.	Fork the repository
	2.	Create a new branch
	3.	Make your changes
	4.	Commit and push
	5.	Open a pull request
📜 License
This project is licensed under the MIT License.
👨‍💻 Author
Garv Singh
Distributed Computing Mini Project
NNIMS - Year 3, Semester 6
⭐ Support
If you found this project useful, consider:
	•	Starring the repository
	•	Forking the project
	•	Sharing feedback
	•	Improving the system with new features
