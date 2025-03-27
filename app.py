from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-a-secure-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model with roles: Admin, Organizer, Participant
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Note: In production, store hashed passwords!
    role = db.Column(db.String(50), nullable=False, default='Participant')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Landing page with a countdown timer
@app.route('/')
def index():
    # Set the event date (adjust to your symposium date)
    event_date = datetime.datetime(2024, 10, 1, 9, 0, 0)
    return render_template('index.html', event_date=event_date)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # In production, check hashed passwords!
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # For demonstration: password stored in plain text (DO NOT use in production)
        new_user = User(username=username, password=password, role='Participant')
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# User dashboard (accessible after login)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Additional sections
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
