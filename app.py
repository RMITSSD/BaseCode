"""
Voting Platform Application
A simple Flask web application for voting.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Handle database path for both local and Docker environments
database_url = os.environ.get('DATABASE_URL')
if database_url is None:
    # Local development - use instance folder
    database_url = 'sqlite:///voting.db'
elif '/app/data/' in database_url:
    # Docker environment - ensure directory exists
    os.makedirs('/app/data', exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    has_voted = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    votes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    candidates = Candidate.query.all()
    return render_template('index.html', candidates=candidates)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        new_user = User(
            username=username,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    candidates = Candidate.query.all()
    return render_template('dashboard.html', user=user, candidates=candidates)

@app.route('/vote/<int:candidate_id>', methods=['POST'])
def vote(candidate_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user.has_voted:
        flash('You have already voted!')
        return redirect(url_for('dashboard'))
    
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        flash('Candidate not found!')
        return redirect(url_for('dashboard'))
    
    # Record the vote
    vote = Vote(user_id=user.id, candidate_id=candidate.id)
    db.session.add(vote)
    
    # Update candidate vote count
    candidate.votes += 1
    
    # Mark user as voted
    user.has_voted = True
    
    db.session.commit()
    flash(f'Your vote for {candidate.name} has been recorded!')
    return redirect(url_for('results'))

@app.route('/results')
def results():
    candidates = Candidate.query.order_by(Candidate.votes.desc()).all()
    total_votes = sum(c.votes for c in candidates)
    return render_template('results.html', candidates=candidates, total_votes=total_votes)

@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    
    candidates = Candidate.query.all()
    users = User.query.all()
    return render_template('admin.html', candidates=candidates, users=users)

@app.route('/admin/add_candidate', methods=['POST'])
def add_candidate():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    name = request.form['name']
    party = request.form['party']
    description = request.form['description']
    
    candidate = Candidate(name=name, party=party, description=description)
    db.session.add(candidate)
    db.session.commit()
    flash(f'Candidate {name} added successfully!')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

def init_db():
    """Initialize the database with sample data."""
    db.create_all()
    
    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password='admin123',
            is_admin=True
        )
        db.session.add(admin)
    
    # Add sample users if they don't exist
    sample_users = [
        {'username': 'john_doe', 'password': 'password123', 'is_admin': False},
        {'username': 'jane_smith', 'password': 'password123', 'is_admin': False},
        {'username': 'mike_wilson', 'password': 'password123', 'is_admin': False},
        {'username': 'sarah_jones', 'password': 'password123', 'is_admin': False},
        {'username': 'demo_voter', 'password': 'demo123', 'is_admin': False},
    ]
    
    for user_data in sample_users:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(
                username=user_data['username'],
                password=user_data['password'],
                is_admin=user_data['is_admin']
            )
            db.session.add(user)
    
    # Add sample candidates if none exist
    if Candidate.query.count() == 0:
        candidates = [
            Candidate(name='Alice Johnson', party='Progressive Party', description='Experienced leader focused on education and healthcare.'),
            Candidate(name='Bob Smith', party='Conservative Alliance', description='Business-oriented candidate advocating for economic growth.'),
            Candidate(name='Carol Davis', party='Green Movement', description='Environmental activist promoting sustainable policies.'),
        ]
        for candidate in candidates:
            db.session.add(candidate)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)