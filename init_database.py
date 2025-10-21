#!/usr/bin/env python3
"""
Database Initialization Script
Initializes the database with sample users and candidates without starting the web server.
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app and database
from app import app, db, User, Candidate

def initialize_database():
    """Initialize the database with sample data."""
    print("🔧 Initializing database...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                password='admin123',
                is_admin=True
            )
            db.session.add(admin_user)
            print("✅ Admin user created")
        
        # Add sample users if they don't exist
        sample_users = [
            {'username': 'john_doe', 'password': 'password123', 'is_admin': False},
            {'username': 'jane_smith', 'password': 'password123', 'is_admin': False},
            {'username': 'mike_wilson', 'password': 'password123', 'is_admin': False},
            {'username': 'sarah_jones', 'password': 'password123', 'is_admin': False},
            {'username': 'demo_voter', 'password': 'demo123', 'is_admin': False},
        ]
        
        users_added = 0
        for user_data in sample_users:
            if not User.query.filter_by(username=user_data['username']).first():
                new_user = User(
                    username=user_data['username'],
                    password=user_data['password'],
                    has_voted=False
                )
                db.session.add(new_user)
                users_added += 1
        
        print(f"✅ {users_added} sample users created")
        
        # Add sample candidates if none exist
        candidates_added = 0
        if Candidate.query.count() == 0:
            candidates = [
                Candidate(name='Alice Johnson', party='Progressive Party', description='Experienced leader focused on education and healthcare.'),
                Candidate(name='Bob Smith', party='Conservative Alliance', description='Business-oriented candidate advocating for economic growth.'),
                Candidate(name='Carol Davis', party='Green Movement', description='Environmental activist promoting sustainable policies.'),
            ]
            for candidate in candidates:
                db.session.add(candidate)
                candidates_added += 1
        
        print(f"✅ {candidates_added} sample candidates created")
        
        # Commit all changes
        db.session.commit()
        print("✅ Database initialization complete!")
        
        # Display summary
        total_users = User.query.count()
        total_candidates = Candidate.query.count()
        admin_users = User.query.filter_by(is_admin=True).count()
        
        print(f"\n📊 DATABASE SUMMARY:")
        print(f"   • Total Users: {total_users}")
        print(f"   • Admin Users: {admin_users}")
        print(f"   • Voter Users: {total_users - admin_users}")
        print(f"   • Total Candidates: {total_candidates}")
        print(f"\n🎉 Ready to start voting!")

if __name__ == "__main__":
    initialize_database()