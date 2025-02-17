import os
import logging
from datetime import datetime
from twilio.rest import Client

def send_alert(phone_number: str, message: str) -> dict:
    """Send SMS alert using Twilio"""
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_number = os.environ.get('TWILIO_PHONE_NUMBER')

        if not all([account_sid, auth_token, from_number]):
            logging.error("Twilio credentials not configured")
            return {"success": False, "error": "Twilio credentials not configured"}

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_=from_number,
            to=phone_number
        )

        return {"success": True, "message_sid": message.sid}
    except Exception as e:
        logging.error(f"Failed to send alert: {str(e)}")
        return {"success": False, "error": str(e)}

def check_alert_conditions(
    current_price: float,
    price_threshold: float,
    current_volatility: float,
    volatility_threshold: float,
    current_drawdown: float,
    drawdown_threshold: float,
    phone_number: str
) -> dict:
    """Check if alert conditions are met and send notifications"""
    alerts = []

    if current_price <= price_threshold:
        alerts.append(f"Price Alert: Bitcoin price has fallen to ${current_price:,.2f}")

    if current_volatility * 100 >= volatility_threshold:
        alerts.append(f"Volatility Alert: Current volatility is {current_volatility*100:.2f}%")

    if current_drawdown * 100 <= -drawdown_threshold:
        alerts.append(f"Drawdown Alert: Current drawdown is {current_drawdown*100:.2f}%")

    if alerts and phone_number:
        message = "\n".join(alerts)
        result = send_alert(phone_number, message)
        if result["success"]:
            logging.info("Alert sent successfully")
            return {"success": True, "alerts": alerts}
        else:
            logging.error(f"Failed to send alert: {result.get('error')}")
            return {"success": False, "error": result.get('error')}

    return {"success": True, "alerts": alerts}

def check_price_alerts(price_data: dict, phone_number: str = None) -> dict:
    """Check price alerts and send notifications if conditions are met"""
    try:
        current_price = price_data.get('price', 0)
        return check_alert_conditions(
            current_price=current_price,
            price_threshold=20000,  # Example threshold
            current_volatility=0.05,  # Example volatility
            volatility_threshold=10,  # Example threshold (10%)
            current_drawdown=-0.1,  # Example drawdown
            drawdown_threshold=20,  # Example threshold (20%)
            phone_number=phone_number
        )
    except Exception as e:
        logging.error(f"Error checking price alerts: {str(e)}")
        return {"success": False, "error": str(e)}
import json
from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.alerts = []

    def add_alert(self, metric, condition, threshold):
        alert = {
            'id': len(self.alerts) + 1,
            'metric': metric,
            'condition': condition,
            'threshold': threshold,
            'created_at': datetime.now().isoformat()
        }
        self.alerts.append(alert)
        return alert

    def check_alerts(self, current_values):
        triggered = []
        for alert in self.alerts:
            value = current_values.get(alert['metric'])
            if value is None:
                continue
            
            if alert['condition'] == 'above' and value > alert['threshold']:
                triggered.append(alert)
            elif alert['condition'] == 'below' and value < alert['threshold']:
                triggered.append(alert)
                
        return triggered
