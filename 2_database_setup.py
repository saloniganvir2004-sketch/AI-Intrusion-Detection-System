from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class TrafficLog(Base):
    __tablename__ = 'traffic_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String(50), nullable=False)
    destination_ip = Column(String(50), nullable=False)
    protocol = Column(String(20))
    packet_size = Column(Float)
    duration = Column(Float)
    
class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    threat_type = Column(String(100), nullable=False)
    source_ip = Column(String(50))
    severity_level = Column(String(20))
    mitigation_status = Column(String(20), default="Pending")

class AdminUser(Base):
    __tablename__ = 'admin_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # Should use hashing like bcrypt
    role = Column(String(20), default="Admin")

def init_db(db_path=None):
    """
    Initializes the DBMS. Creating the SQLite database and all tables.
    """
    if db_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_dir = os.path.join(base_dir, 'db')
        os.makedirs(db_dir, exist_ok=True)  # <--- This fixes the error!
        db_path = f"sqlite:///{os.path.join(db_dir, 'ids_database.db')}"
        
    print(f"Connecting to DBMS at {db_path}...")
    engine = create_engine(db_path, echo=False)
    
    # Create the tables
    Base.metadata.create_all(engine)
    print("Tables created successfully: traffic_logs, alerts, admin_users.")
    
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    print("Starting Phase 2: Database Management (DBMS) Setup")
    session = init_db()
    
    # Seed a dummy admin user
    try:
        if session.query(AdminUser).count() == 0:
            dummy_admin = AdminUser(username="admin", password_hash="hashed_password_123")
            session.add(dummy_admin)
            session.commit()
            print("Default admin account created (username: admin).")
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()
    
    print("DBMS Phase 2 complete. Database securely formatted.")
