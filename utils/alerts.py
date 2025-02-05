import os
from datetime import datetime
from twilio.rest import Client
import streamlit as st

def send_alert(phone_number: str, message: str) -> bool:
    """Send SMS alert using Twilio"""
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_number = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            st.error("Twilio credentials not configured")
            return False
            
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=phone_number
        )
        
        return True
    except Exception as e:
        st.error(f"Failed to send alert: {str(e)}")
        return False

def check_alert_conditions(
    current_price: float,
    price_threshold: float,
    current_volatility: float,
    volatility_threshold: float,
    current_drawdown: float,
    drawdown_threshold: float,
    phone_number: str
) -> None:
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
        if send_alert(phone_number, message):
            st.success("Alert sent successfully!")
        else:
            st.error("Failed to send alert")
