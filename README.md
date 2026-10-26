# AI-Based Smart City Governance and Cybersecurity

## Stack
Python 3.8+, Flask, HTML/CSS/JavaScript-ready frontend, MySQL, NumPy, scikit-learn.
Apache/Nginx can be placed in front of Flask for deployment.

## Run
1. Install Python and MySQL.
2. Run `database.sql` in MySQL Workbench.
3. In this folder run:
   `pip install -r requirements.txt`
4. Set your MySQL password in `app.py` or environment variable `DB_PASSWORD`.
5. Run:
   `python app.py`
6. Open http://127.0.0.1:5000

## AI feature
The Security page uses Isolation Forest to detect anomalous network behavior.
Normal test: 1500 bytes, 1 failed login, 90 requests, 40% CPU.
Suspicious test: 50000 bytes, 35 failed logins, 1200 requests, 98% CPU.

This is an academic prototype using synthetic training data, not a production cybersecurity system.
