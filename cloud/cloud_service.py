from flask import Flask, request,jsonify

app=Flask(__name__)

def send_email(alert):
    print("\nEMAIL!!!!")
    print("To: <insert email id>")
    print(f"Subject: {alert["severity"]} Environmental alert")
    print()
    if (alert["alerts"]):
        for msg in alert["alerts"]:
            print(f" - {msg}")
    else:
        print("No environmental issues")
    print()



def process_alert(alert):
    severity=alert["severity"] 
    if (severity.lower()=="normal"):
        send_email(alert)
        return "Normal email sent"
    elif (severity.lower()=="warning"):
        send_email(alert)
        return "Warning email sent"
    elif (severity.lower()=="critical"):
        send_email(alert)
        return "Critical email sent"

    return "Unknown severity"

    

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
