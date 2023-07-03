import bcrypt
from flask import Flask, render_template, jsonify, request
import os
from flask import Flask, render_template, jsonify, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import psycopg2
import psycopg2.extras
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


db_config = {
    'host': 'localhost',
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
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    # Load user from the database based on the user_id
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username, password FROM public.user_details_tbl WHERE username = %s", (user_id,))
            result = cur.fetchone()
            if result:
                username, password = result
                return User(username, password)
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
    body = f'Please click the following link to activate your account: {verification_link}'

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)


def generate_verification_token(email):
    return serializer.dumps(email)


def verify_token(token):
    try:
        email = serializer.loads(token, max_age=1200)  # Token expires after 20 Minutes (1200 seconds)
        return email
    except:
        return None


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
                cur.execute("SELECT COUNT(*) FROM public.user_details_tbl WHERE firstname = %s OR lastname = %s AND email = %s AND username = %s ", (firstname, lastname, email, username))
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
                msg = "INSERT SUCCESS"
                return jsonify({'message': msg}), 200

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
                return redirect('/login')  # Redirect to the login page after successful activation
    else:
        return jsonify({'error': 'Invalid or expired token'}), 400


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, password FROM public.user_details_tbl WHERE username = %s", (username,))
                result = cur.fetchone()
                if result:
                    _, hashed_password = result
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        user = User(username, hashed_password)
                        login_user(user)
                        return redirect('/profile')
                return jsonify({'error': 'Invalid username or password'}), 401

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8085, debug=True)
