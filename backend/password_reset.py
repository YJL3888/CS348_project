from flask import Blueprint, request
import smtplib
from email.message import EmailMessage
import os
from db_util import create_connection, hash_password
from datetime import datetime, timezone
import random
import string

bp = Blueprint('password_reset', __name__, url_prefix='/password-reset')
_EMAIL_USER = os.environ['EMAIL_USER']
_EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


@bp.post('/get-token')
def send_password_reset_token():
    email = request.form['email']
    utc_time = datetime.now(timezone.utc)
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute('SELECT * FROM Users WHERE email=%s', (email,))
            user = cursor.fetchone()
            if not user:
                return {'error': 'Invalid email'}, 400
            cursor.execute('SELECT * FROM PasswordReset WHERE email=%s AND active=true', (email,))
            if prev_reset := cursor.fetchone():
                cursor.execute('UPDATE PasswordReset SET active=false WHERE id=%s', (prev_reset['id'],))
            token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            cursor.execute('INSERT INTO PasswordReset(token, email, active) VALUES(%s, %s, %s)',
                           (token, email, True))
            msg = EmailMessage()
            msg['Subject'] = 'GooseGooseGo Password Reset'
            msg['From'] = _EMAIL_USER
            msg['To'] = email
            msg.set_content(f'''
            <p>Hi {user['username']},</p>

            <p>You requested a password reset for your GooseGooseGo account at {utc_time}.</p>
            <p>Use this token to complete the process:</p>
            <pre>{token}</pre>
            <p>If this was not you, you can disregard this email.</p>
            ''', subtype='html')
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(_EMAIL_USER, _EMAIL_PASSWORD)
            smtp.send_message(msg)
            smtp.quit()
            connection.commit()
            return {'message': 'The token was sent to your email.'}


@bp.post('')
def reset_password():
    email = request.form['email']
    token = request.form['token']
    new_password = request.form['password']
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute('SELECT * FROM PasswordReset WHERE email=%s AND active = true', (email,))
            reset_info = cursor.fetchone()
            if not reset_info or reset_info['token'] != token:  # TODO: check time (expired?)
                return {'error': 'Invalid token.'}, 400
            cursor.execute('UPDATE Users SET password=%s WHERE email=%s',
                           (hash_password(new_password), email))
            cursor.execute('UPDATE PasswordReset SET active=false WHERE id=%s', (reset_info['id'],))
            connection.commit()
            return {'message': 'Password successfully reset. You may now login.'}
