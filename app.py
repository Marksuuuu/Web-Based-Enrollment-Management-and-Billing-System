import bcrypt
from flask import Flask, render_template, jsonify, request
import os
from flask import Flask, render_template, jsonify, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import psycopg2
import json
import psycopg2.extras
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


db_config = {
    'host': '127.0.0.1',
    'port': '5432',
    'dbname': 'web_based_enrollment_management',
    'user': 'flask_user',
    'password': '-clear1125'
}

app = Flask(__name__)
app.secret_key = 'marksuuuu'

app.config['MAIL_DEFAULT_SENDER'] = 'WEB BASED ENROLLMENT MANAGEMENT SYSTEM MAILER'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'johnraymark3@gmail.com'
app.config['MAIL_PASSWORD'] = 'qqrlvfznwvjnnjol'
mail = Mail(app)

app.config['SECRET_KEY'] = 'marksuuuu'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User:
    def __init__(self, username, password, id, activate, profile, email, role, firstname, lastname, middlename):
        self.id = id
        self.username = username
        self.password = password
        self.activate = activate
        self.profile = profile
        self.email = email
        self.role = role
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self.is_active = activate

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return True  # Modify this based on your authentication logic

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False



@login_manager.user_loader
def load_user(user_id):
    # Load user from the database based on the user_id
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username, password, id, activate,  profile, email, role , firstname , lastname , middlename  FROM public.user_details_tbl WHERE username = %s", (user_id,))
            result = cur.fetchone()
            if result:
                username, password, id, activate,  profile, email, role , firstname , lastname , middlename  = result
                return User(username, password, id, activate, profile, email, role , firstname , lastname , middlename)
    return None



def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def send_verification_email(email):
    token = generate_verification_token(email)
    domain = request.host_url.rstrip('/') 
    verification_link = f'{domain}/verify/{token}'

    sender = ('SYSTEM MAILER', 'WEB BASED ENROLLMENT MANAGEMENT SYSTEM')
    recipients = [email]
    subject = 'Account Activation'
    def send_verification_email(email):
        token = generate_verification_token(email)
    domain = request.host_url.rstrip('/')
    verification_link = f'{domain}/verify/{token}'

    sender = ('SYSTEM MAILER', 'WEB BASED ENROLLMENT MANAGEMENT SYSTEM')
    recipients = [email]
    subject = 'Account Activation'

    # Create a multipart message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender[0]
    msg['To'] = email

    # Create the HTML body
    html_body = f'''
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 500px;
                margin: 0 auto;
                padding: 20px;
            }}
            h2 {{
                color: #333;
            }}
            p {{
                margin-bottom: 10px;
            }}
            .cta-button {{
                display: inline-block;
                background-color: #007bff;
                color: #fff;
                padding: 10px 20px;
                border-radius: 4px;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Dear User,</h2>

            <p>Thank you for registering with our enrollment management system.</p>
            <p>To activate your account, please click on the following link:</p>

            <p>
                <a href="{verification_link}" class="cta-button">Activate Account</a>
            </p>

            <p>If you did not register for an account or have any questions, please contact our support team.</p>

            <p>Best regards,</p>
            <p>The Enrollment Management Team</p>
        </div>
    </body>
    </html>
    '''
    
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.html = html_body
    # Send the email
    mail.send(msg)


def generate_verification_token(email):
    return serializer.dumps(email)

def verify_token(token):
    try:
        email = serializer.loads(token, max_age=7200)  # Token expires after 20 Minutes (1200 seconds)
        return email
    except:
        return None

def send_password_reset_email(email):
    token = generate_password_reset_token(email)
    domain = request.host_url.rstrip('/')
    reset_link = f'{domain}/reset-password/{token}'

    sender = ('SYSTEM MAILER', 'WEB BASED ENROLLMENT MANAGEMENT SYSTEM')
    recipients = [email]
    subject = 'Password Reset'
    body = f'Please click the following link to reset your password: {reset_link}'

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)
    
def generate_password_reset_token(email):
    return serializer.dumps(email)

@app.route('/register', methods=['POST'])
def register_insert():
    try:
        # Extract form data
        username = request.form['username']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        uploaded_img = request.files['fileInput']
        role = 'user'

        if not (username and firstname and middlename and lastname and email and password and uploaded_img and role):
            return jsonify({'error': 'Missing form fields'}), 400

        # Check if an account with the same last name and email already exists
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM public.user_details_tbl WHERE (firstname = %s OR lastname = %s) AND email = %s AND username = %s", (firstname, lastname, email, username))
                result = cur.fetchone()
                if result and result[0] > 0:
                    return jsonify({'error': 'An account with the same last name and email already exists.'}), 400

        salt = bcrypt.gensalt().decode('utf-8')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

        if uploaded_img.filename == '' or not allowed_file(uploaded_img.filename):
            return jsonify({'error': 'Invalid file format. Only image files are allowed.'}), 400

        filename = secure_filename(uploaded_img.filename)
        file_path = os.path.join('static/assets/img/uploaded', filename).replace("\\", "/")
        uploaded_img.save(file_path)

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO public.user_details_tbl (username, firstname, middlename, lastname, email, password, profile, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (username, firstname, middlename, lastname, email, hashed_password, file_path, role)) 
                conn.commit()
                send_verification_email(email)  # Send verification email
                msg = {'msg': 1}
                return jsonify(msg)

    except KeyError:
        return jsonify({'error': 'Invalid form data'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/verify/<token>')
def verify_account(token):
    email = verify_token(token)
    if email:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE public.user_details_tbl SET activate = true WHERE email = %s", (email,))
                conn.commit()
                return redirect('/')
    else:
        return jsonify({'error': 'Invalid or expired token'}), 400
    
@app.route('/deactivate-account', methods=['POST'])
def deactivate_account():
    id = request.form['dataID']
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.user_details_tbl WHERE id = %s", (id,))
            conn.commit()
            return redirect('/')
        
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # Check if the email exists in the database
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM public.user_details_tbl WHERE email = %s", (email,))
                result = cur.fetchone()
                if result and result[0] > 0:
                    send_password_reset_email(email)  # Send password reset email
                    msg = {'msg': 1}
                    return jsonify(msg)
                else:
                    msg = {'msg': 2}
                    return jsonify(msg)

    return render_template('forgot-password.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, password, id ,activate,  profile, email, role , firstname , lastname , middlename  activate FROM public.user_details_tbl WHERE username = %s", (username,))
                result = cur.fetchone()
                if result:
                    _, hashed_password, id, activate, profile, email, role, firstname, lastname, middlename = result
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        if activate:
                            user = User(username, password, id, activate, profile, email, role, firstname, lastname, middlename)
                            login_user(user)
                            return redirect('/profile')
                        else:
                            return jsonify({'error': 'Account not verified. Please check your email for the verification link.'}), 401
                return jsonify({'error': 'Invalid email or username or password'}), 401

    return render_template('login.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/forgotPassword')
def forgotPassword():
    return render_template('forgot-password.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8085, debug=True)
