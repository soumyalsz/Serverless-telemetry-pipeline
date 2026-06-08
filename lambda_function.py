import json
import urllib.request
from datetime import datetime

def lambda_handler(event, context):
    latitude = 22.5726
    longitude = 88.3639
    y
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,surface_pressure"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            raw_data = json.loads(response.read().decode())
        
        current_telemetry = raw_data.get("current", {})

        timestamp = current_telemetry.get("time")
        temp = current_telemetry.get("temperature_2m")
        humidity = current_telemetry.get("relative_humidity_2m")
        pressure = current_telemetry.get("surface_pressure")

        telemetry_record = {
            "processed_at": str(datetime.utcnow()),
            "telemetry_timestamp": timestamp,
            "coordinates": {"lat": latitude, "lon": longitude},
            "metrics": {
                "temperature_celsius": temp,
                "humidity_percentage": humidity,
                "surface_pressure_hpa": pressure
            },
            "status": "NORMAL"
        }
        
        if temp > 42.0 or temp < 5.0:
            telemetry_record["status"] = "ALERT_TEMPERATURE_ANOMALY"
        elif humidity > 95.0:
            telemetry_record["status"] = "ALERT_EXCESSIVE_MOISTURE"
            
        print(f"Ingested telemetry payload: {json.dumps(telemetry_record)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(telemetry_record)
        }
        
    except Exception as e:
        error_msg = f"Telemetry ingestion failed: {str(e)}"
        print(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": error_msg})
        }
feat : initial serverless telemetry script
