import requests
import sys

def send_message(user, password, sender, phone, text, priority, params):
    api_url = "https://bhashsms.com/api/sendmsg.php"
    payload = {
        'user': user,
        'pass': password,
        'sender': sender,
        'phone': phone,
        'text': text,
        'priority': priority,
        'stype': 'normal',
        'Params': params
    }
    response = requests.get(api_url, params=payload)
    return response.text

def main():
    # Placeholder values for message parameters
    user = "PastelFrames"
    password = "123456"
    sender = "BUZWAP"
    phone_number = "7708196973"  # Replace with the actual phone number
    text = "cloud_deletion"
    priority = "wa"
    dynamic_params = "PastelFrames Ai."  # Replace with actual dynamic parameters

    # Sending message
    response = send_message(user, password, sender, phone_number, text, priority, dynamic_params)
    print(f"Message sent to {phone_number} with response: {response}")

if __name__ == "__main__":
    main()
