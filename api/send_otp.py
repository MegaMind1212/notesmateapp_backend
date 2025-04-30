import smtplib
from email.mime.text import MIMEText
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Email configuration (store in environment variables for security)
EMAIL_USER = os.getenv('EMAIL_USER', 'yashkb2002@gmail.com')  # Default to your Gmail
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'rnrubxmhfvhhcvrd')  # Default to your App Password

# SMTP server settings for Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

@app.route('/', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        to_email = data.get('toEmail')
        otp = data.get('otp')

        if not to_email or not otp:
            return jsonify({'error': 'toEmail and otp are required'}), 400

        # Create the email message
        msg = MIMEText(f'Your Notesmate OTP is: {otp}')
        msg['Subject'] = 'Notesmate OTP Verification'
        msg['From'] = EMAIL_USER
        msg['To'] = to_email

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f'OTP email sent successfully to: {to_email}')
        return jsonify({'message': 'OTP sent successfully'}), 200

    except Exception as e:
        print(f'Failed to send OTP email: {e}')
        return jsonify({'error': f'Failed to send OTP: {str(e)}'}), 500

def handler(request):
    return app