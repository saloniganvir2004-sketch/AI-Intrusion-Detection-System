# AI-Based Cybersecurity Intrusion Detection System

An advanced Cybersecurity Intrusion Detection System (IDS) developed to meet M.Sc (AI & DA) 2nd-semester requirements. This system demonstrates the practical integration of core academic subjects into a unified, real-world application.

## Subject Integration Overview
- **Deep Learning**: Implementation of Autoencoders/LSTMs to act as the primary Anomaly Detection Engine.
- **Statistical Learning & Inferential Statistics**: Exploratory Data Analysis, fundamental feature engineering, and baseline generation using algorithms like Random Forest.
- **DBMS**: Leveraging SQLite/SQLAlchemy for dynamic table creation, data ingestion, and rapid querying of network logs & security alerts.
- **AI & Robotics (Agents)**: A programmable Software Robot (Agent) that continuously monitors traffic flow and automatically executes mitigation protocols (RPA) upon anomaly detection.

---

## Project Structure
```
IDS_Project/
│
├── db/                       # Database files (.db) will be stored here
├── data/                     # Store your datasets (e.g., NSL-KDD CSV files) here
├── models/                   # Saved Deep Learning models (.h5) 
├── scripts/                  
│   ├── 1_eda_and_preprocessing.py   # Statistical Analysis & Feature Scaling
│   ├── 2_database_setup.py          # DBMS Schema Initialization
│   ├── 3_model_training.py          # Machine Learning & Deep Learning Training
│   ├── 4_intelligent_agent.py       # Simulated AI Agent (Real-time monitoring & RPA)
│   └── 5_app.py                     # Streamlit Admin UI Dashboard
│
├── requirements.txt          # Python library dependencies
└── README.md                 # Project documentation
```

---

## Setup & Execution Guide 🚀

### Step 1: Environment Setup
1. Ensure Python 3.10+ is installed.
2. Activate your Virtual Environment:
   ```bash
   venv\Scripts\activate      # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Running the Project
Follow the numerical order of the scripts located in the `scripts/` folder.

**1. Data Preparation**
Place your dataset (e.g., NSL-KDD `KDDTrain+.txt`) inside the `data/` folder, then run:
```bash
python scripts/1_eda_and_preprocessing.py
```
*This handles statistical learning concepts.*

**2. Initialize Database**
```bash
python scripts/2_database_setup.py
```
*This creates the `ids_database.db` backend (DBMS).*

**3. Train Models**
```bash
python scripts/3_model_training.py
```
*This trains both the Statistical Baseline (Random Forest) and the Deep Neural Network.*

**4. Start the Intelligent Agent**
```bash
python scripts/4_intelligent_agent.py
```
*This will start simulating incoming traffic, detecting threats, and executing mock mitigations.*

**5. Launch Dashboard**
In a new terminal (while Step 4 is running), launch the visual dashboard:
```bash
python scripts\6_web_app.py
```
*This is the front-end for the admin to monitor alerts and logs.*

---

## Interview Talking Points
1. Emphasize that you didn't just build a model; you built an **end-to-end pipeline**.
2. Explain how Data Preprocessing handles high variance in incoming packet sizes (refer to Statistical Learning concepts).
3. Be ready to explain the choice of Deep Learning. Why an Autoencoder? "Because intrusions are often zero-day attacks; learning 'normal' traffic and flagging high reconstruction errors is safer than trying to classify unknown attack signatures."
4. Showcase the AI Agent acting as an autonomous incident response bot.
