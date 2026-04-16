import time
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
import os
import importlib

# Ensure we can import from 2_database_setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
db_setup = importlib.import_module("2_database_setup")
TrafficLog = db_setup.TrafficLog
Alert = db_setup.Alert
init_db = db_setup.init_db

class SecurityAgent:
    """
    Intelligent Agent (Subject: AI and Robotics/RPA).
    Monitors traffic, queries the Deep Learning model (simulated here), 
    and takes automated actions.
    """
    def __init__(self, db_session):
        self.db = db_session
        print("Security Agent Initialized and connected to Database.")

    def analyze_traffic(self, log_entry):
        """
        In a real scenario, this method would pass the log_entry to the 
        Deep Learning model. Here we mock the DL inference.
        """
        # Mock probability of intrusion (e.g., if packet size is suspiciously large)
        is_intrusion = random.random() > 0.85 
        
        if is_intrusion:
            self.trigger_alert(log_entry)
            self.mitigate_threat(log_entry.source_ip)
            
    def trigger_alert(self, log_entry):
        """Registers an alert in the database and notifies admin."""
        new_alert = Alert(
            threat_type="Anomaly Detected by Deep Learning Model",
            source_ip=log_entry.source_ip,
            severity_level="High"
        )
        self.db.add(new_alert)
        self.db.commit()
        
        print(f"\n[CRITICAL ALERT] Intrusion detected from IP: {log_entry.source_ip}")
        print(f"Details: Protocol={log_entry.protocol}, Size={log_entry.packet_size}")

    def mitigate_threat(self, source_ip):
        """
        Robotic Process Automation: Automatically performing mitigation steps.
        """
        print(f"[MITIGATION AGENT] Executing firewall rule to block IP: {source_ip}")
        # Mock command: e.g., os.system(f"iptables -A INPUT -s {source_ip} -j DROP")
        time.sleep(1) # Simulating execution time
        
        # Update the database
        alert = self.db.query(Alert).filter_by(source_ip=source_ip).order_by(Alert.id.desc()).first()
        if alert:
            alert.mitigation_status = "Blocked IP"
            self.db.commit()
        print("[MITIGATION AGENT] Threat neutralized successfully.\n")

def simulate_realtime_traffic(agent):
    """Generates continuous fake network logs to simulate streaming data."""
    protocols = ['TCP', 'UDP', 'ICMP']
    
    print("\nStarting Real-time Traffic Simulation...")
    try:
        while True:
            # Generate fake traffic log
            src_ip = f"192.168.1.{random.randint(1, 20)}"
            dst_ip = f"10.0.0.{random.randint(1, 20)}"
            proto = random.choice(protocols)
            size = random.uniform(50.0, 1500.0)
            
            new_log = TrafficLog(
                source_ip=src_ip,
                destination_ip=dst_ip,
                protocol=proto,
                packet_size=size,
                duration=random.uniform(0.1, 5.0)
            )
            
            # Save to Database
            agent.db.add(new_log)
            agent.db.commit()
            
            # Agent analyzes the log snippet
            agent.analyze_traffic(new_log)
            
            time.sleep(2) # Wait 2 seconds before next packet
            
    except KeyboardInterrupt:
        print("\nTraffic Simulation Stopped.")

if __name__ == "__main__":
    print("Starting Phase 4: AI Software Agent")
    session = init_db()
    
    agent = SecurityAgent(session)
    simulate_realtime_traffic(agent)
    
    session.close()
