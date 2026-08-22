from flask import Flask, request, jsonify
import requests

app=Flask(__name__)

#Thresholds

RAINFALL_THRESHOLD=100
RIVER_LEVEL_THRESHOLD=4.0
AQI_THRESHOLD=200
WIND_SPEED_THRESHOLD=60

def analyze_sensor_data(data):
    alerts=[]
    rainfall=data["rainfall"]
    river_level=data["river_level"]
    aqi=data["aqi"]
    wind_speed=data["wind_speed"]

    if (rainfall > RAINFALL_THRESHOLD):
        alerts.append("Heavy rainfall detected")
    if (river_level > RIVER_LEVEL_THRESHOLD):
        alerts.append("High river level detected")
    if (aqi > AQI_THRESHOLD):
        alerts.append("Hazardous air quality detected")
    if (wind_speed > WIND_SPEED_THRESHOLD):
        alerts.append("Severe wind detected")

    if (len(alerts)>=2):
        severity="CRITICAL"
    elif (len(alerts)==1):
        severity="WARNING"
    else:
        severity="NORMAL"
    return {
        "severity" : severity,
        "alerts":alerts
    }

@app.route("/sensor-data",methods=["POST"])
def receive_sensor_data():
    data=request.get_json()
    if not data:
        return jsonify({
            "error":"No sensor data received"
        }),400
    result=analyze_sensor_data(data)
    alert_payload={
        "severity":result["severity"],
        "alerts":result["alerts"],
        "timestamp":data["timestamp"]
    }
    print(alert_payload)
    response=requests.post(
        "http://localhost:6000/alerts",
        json=alert_payload
    )

    return jsonify(alert_payload)

if (__name__=="__main__"):
    app.run(host="0.0.0.0",port=5000)
