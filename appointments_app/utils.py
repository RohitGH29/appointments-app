import frappe
from twilio.rest import Client  
from frappe.utils.password import get_decrypted_password

print("Loading utils.py")

def get_twilio_client():
    account_sid = frappe.db.get_single_value("Appointments Twilio Settings","account_sid")
    auth_token = get_decrypted_password("Appointments Twilio Settings", "Appointments Twilio Settings", "auth_token")

    if not account_sid or not auth_token:
        frappe.throw("Please set Account SID and Auth Token in Appointments Twilio Settings")

    return Client(account_sid, auth_token)

# number = "+16204558661"
# function to send a message
def send_message(body, from_, to):
    client = get_twilio_client()
    message = client.messages.create(
        body=body,
        from_=from_,
        to=to
    ) 

    try:
        frappe.get_doc({
            "doctype": "Appointments Sms Log",
            "twilio_sid": message.sid,
            "body": body,
            "from_": from_,
            "to": to
        }
        ).insert(ignore_permissions=True)

    except Exception as e:
        frappe.log_error("Appointments SMS Log Creation Failed")

    return message.sid 