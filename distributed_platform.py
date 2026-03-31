#!/usr/bin/env python3
"""
Distributed Disaster Intelligence Platform v2.0 - Complete Auto-Managed System
Features: Auto-worker start, Real-time dashboard, Fault tolerance, Performance charts
Run: python3 distributed_platform.py
"""

from flask import Flask, request, jsonify, render_template_string
import requests
import json
import threading
import time
import subprocess
import signal
import sys
import os

app = Flask(__name__)

# Configuration
WORKER_PORTS = [5001
