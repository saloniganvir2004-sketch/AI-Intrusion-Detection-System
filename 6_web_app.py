from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import pandas as pd
import json
import os
import sys
import importlib

# Ensure we can import from 2_database_setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'scripts'))

db_setup = importlib.import_module("2_database_setup")
TrafficLog = db_setup.TrafficLog
Alert = db_setup.Alert

# Flask setup
template_dir = os.path.join(BASE_DIR, 'templates')
app = Flask(__name__, template_folder=template_dir)

# 🔐 Secret key for session
app.secret_key = "super_secret_key"

# 🔐 ADMIN LOGIN (ONLY ONE USER)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Database Connection setup
db_path = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'ids_database.db')}"
engine = create_engine(db_path)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------- HELPER FUNCTIONS ----------------------

def get_stats():
    session_db = SessionLocal()
    total_logs = session_db.query(TrafficLog).count()
    total_alerts = session_db.query(Alert).count()
    session_db.close()
    return {
        "total_logs": total_logs,
        "total_alerts": total_alerts
    }

def get_protocol_stats(session_db):
    total = session_db.query(TrafficLog).count()
    if total == 0:
        return []
    
    proto_counts = session_db.query(
        TrafficLog.protocol, func.count(TrafficLog.id)
    ).group_by(TrafficLog.protocol).all()

    colors = [
        'bg-primary-dim shadow-[0_0_8px_rgba(21,164,255,0.4)]', 
        'bg-secondary-fixed shadow-[0_0_8px_rgba(88,231,171,0.4)]', 
        'bg-primary-dim/60', 
        'bg-outline-variant'
    ]
    
    proto_counts.sort(key=lambda x: x[1], reverse=True)
    stats_list = []
    
    for i, (proto, count) in enumerate(proto_counts[:4]):
        pct = (float(count) / total) * 100
        stats_list.append({
            'name': proto,
            'count_formatted': f"{count/1000:.1f}K" if count >= 1000 else str(count),
            'percent': int(pct),
            'color': colors[i] if i < len(colors) else colors[-1]
        })
    return stats_list

# ---------------------- LOGIN ROUTES ----------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Admin Credentials"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ---------------------- MAIN ROUTES ----------------------

# 🔥 Welcome Page
@app.route('/')
def welcome():
    return render_template('welcome.html')


# 🔥 Dashboard (protected)
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    session_db = SessionLocal()
    
    logs = session_db.query(TrafficLog).order_by(TrafficLog.timestamp.desc()).limit(50).all()
    alerts = session_db.query(Alert).order_by(Alert.timestamp.desc()).limit(10).all()
    
    stats = get_stats()
    protocol_stats = get_protocol_stats(session_db)
    session_db.close()
    
    return render_template(
        'traffic_monitor.html',
        logs=logs,
        alerts=alerts,
        stats=stats,
        protocol_stats=protocol_stats
    )


# 🔥 NEW REPORT ROUTE (ADDED)
@app.route('/report')
def generate_report():
    if 'user' not in session:
        return redirect(url_for('login'))

    session_db = SessionLocal()

    total_logs = session_db.query(TrafficLog).count()
    total_alerts = session_db.query(Alert).count()

    threat_percentage = (total_alerts / total_logs * 100) if total_logs > 0 else 0

    session_db.close()

    return render_template(
        'report.html',
        total_logs=total_logs,
        total_alerts=total_alerts,
        threat_percentage=round(threat_percentage, 2)
    )


@app.route('/analysis')
def model_analysis():
    if 'user' not in session:
        return redirect(url_for('login'))

    metrics_path = os.path.join(BASE_DIR, 'data', 'metrics.json')
    try:
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
    except Exception:
        metrics = {}

    return render_template('model_analysis.html', metrics=metrics)


@app.route('/about')
def about_team():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('about_team.html')

# ---------------------- RUN APP ----------------------

if __name__ == '__main__':
    print("--- Starting IntrusionX Pro Web Dashboard ---")
    print("Go to: http://localhost:5000/")
    app.run(debug=True, port=5000)