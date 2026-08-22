from flask import Flask, request,jsonify
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

app=Flask(__name__)

load_dotenv()
SMTP_EMAIL=os.getenv("SMTP_EMAIL")
SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
ALERT_EMAIL=os.getenv("ALERT_EMAIL")

prev_severity=None


def send_email(alert):
    message=EmailMessage()
    message["From"]=SMTP_EMAIL
    message["To"]=ALERT_EMAIL
    message["Subject"]=f"{alert["severity"]} Environmental Alert"
    body=f"""
Environmental Monitoring Alert
Severity: {alert["severity"]}
Time: {alert["timestamp"]}
Detected conditions: 
"""
    if (alert["alerts"]):
        for item in alert["alerts"]:
            body+=f" - {item}\n"
    else:
        body+="None\n"
    message.set_content(body)
    with smtplib.SMTP("smtp.gmail.com",587)as smtp:
        smtp.starttls()
        smtp.login(SMTP_EMAIL,SMTP_PASSWORD)
        smtp.send_message(message)

    print("Email successfully sent")
    



def process_alert(alert):
    global prev_severity
    severity=alert["severity"] 
    if (prev_severity!=severity):
        send_email(alert)
        prev_severity=severity
        return f"{severity} email sent"
    return f"{severity} unchanged. No email sent."


    

@app.route("/alerts",methods=["POST"])
def receive_alert():
    alert=request.get_json()

    if not alert:
        return jsonify({
            "error":"No alert received"
        }),400

    print("\nAlert received from Gateway: ")
    print(alert)
    result=process_alert(alert)
      
    return jsonify({
        "status":"received",
        "result":result
    })

if (__name__=="__main__"):
    app.run(host="0.0.0.0",port=6000)
