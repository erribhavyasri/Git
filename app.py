from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "smart-city-demo")

DB = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "smart_city_db")
}

def db():
    return mysql.connector.connect(**DB)

def rows(sql, params=()):
    con=db(); cur=con.cursor(dictionary=True)
    try:
        cur.execute(sql, params); return cur.fetchall()
    finally:
        cur.close(); con.close()

def run(sql, params=()):
    con=db(); cur=con.cursor()
    try:
        cur.execute(sql, params); con.commit()
    finally:
        cur.close(); con.close()

# Lightweight ML model: Isolation Forest for anomaly detection.
X=np.array([
 [1200,1,80,35],[1500,0,95,40],[1300,1,100,42],
 [1800,2,110,45],[2100,1,120,48],[1600,0,90,38],
 [1400,1,85,36],[1900,2,115,44],[1550,0,92,39],
 [1750,1,105,43],[50000,35,1200,98],[65000,50,1500,99]
])
model=IsolationForest(contamination=0.15, random_state=42).fit(X)

@app.route("/")
def home():
    stats={
      "citizens": rows("SELECT COUNT(*) c FROM citizens")[0]["c"],
      "services": rows("SELECT COUNT(*) c FROM services")[0]["c"],
      "alerts": rows("SELECT COUNT(*) c FROM security_alerts WHERE status='Open'")[0]["c"],
      "complaints": rows("SELECT COUNT(*) c FROM complaints WHERE status='Open'")[0]["c"]
    }
    return render_template("dashboard.html", stats=stats,
      alerts=rows("SELECT * FROM security_alerts ORDER BY id DESC LIMIT 8"),
      complaints=rows("""SELECT c.*,ci.name citizen_name FROM complaints c
                         LEFT JOIN citizens ci ON c.citizen_id=ci.id
                         ORDER BY c.id DESC LIMIT 8"""))

@app.route("/citizens", methods=["GET","POST"])
def citizens():
    if request.method=="POST":
        run("INSERT INTO citizens(name,email,phone) VALUES(%s,%s,%s)",
            (request.form["name"],request.form["email"],request.form["phone"]))
        flash("Citizen added.")
        return redirect(url_for("citizens"))
    return render_template("citizens.html", citizens=rows("SELECT * FROM citizens ORDER BY id DESC"))

@app.route("/services", methods=["GET","POST"])
def services():
    if request.method=="POST":
        run("INSERT INTO services(name,department,status) VALUES(%s,%s,%s)",
            (request.form["name"],request.form["department"],request.form["status"]))
        flash("Service added.")
        return redirect(url_for("services"))
    return render_template("services.html", services=rows("SELECT * FROM services ORDER BY id DESC"))

@app.route("/complaints", methods=["GET","POST"])
def complaints():
    if request.method=="POST":
        run("""INSERT INTO complaints(citizen_id,title,category,description)
               VALUES(%s,%s,%s,%s)""",
            (request.form["citizen_id"],request.form["title"],
             request.form["category"],request.form["description"]))
        flash("Complaint submitted.")
        return redirect(url_for("complaints"))
    return render_template("complaints.html",
        citizens=rows("SELECT * FROM citizens ORDER BY name"),
        complaints=rows("""SELECT c.*,ci.name citizen_name FROM complaints c
                           LEFT JOIN citizens ci ON c.citizen_id=ci.id
                           ORDER BY c.id DESC"""))

@app.route("/security", methods=["GET","POST"])
def security():
    if request.method=="POST":
        ip=request.form["source_ip"]
        values=[float(request.form[x]) for x in
                ["network_bytes","failed_logins","request_count","cpu_usage"]]
        prediction=model.predict([values])[0]
        score=float(model.decision_function([values])[0])
        anomaly=prediction==-1
        severity="High" if anomaly else "Low"
        title="AI detected anomalous network activity" if anomaly else "Normal network activity"
        status="Open" if anomaly else "Closed"
        run("""INSERT INTO security_alerts
               (source_ip,title,severity,network_bytes,failed_logins,
                request_count,cpu_usage,status,created_at)
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (ip,title,severity,*values,status,datetime.now()))
        return render_template("security_result.html",
            prediction="Anomaly Detected" if anomaly else "Normal",
            severity=severity, score=round(score,4), ip=ip)
    return render_template("security.html",
                           alerts=rows("SELECT * FROM security_alerts ORDER BY id DESC"))

if __name__=="__main__":
    app.run(debug=True)
