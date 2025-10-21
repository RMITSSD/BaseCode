#!/usr/bin/env python3
"""
Sample Users Display Script
Shows all pre-configured sample users in the voting platform.
"""

def display_sample_accounts():
    """Display all sample user accounts for easy reference."""
    print("=" * 60)
    print("VOTING PLATFORM - SAMPLE ACCOUNTS")
    print("=" * 60)
    
    print("\n🔐 ADMIN ACCOUNT:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Role: Administrator")
    print("   Privileges: Add candidates, view statistics, full access")
    
    print("\n👥 SAMPLE VOTER ACCOUNTS:")
    sample_users = [
        ("john_doe", "password123"),
        ("jane_smith", "password123"),
        ("mike_wilson", "password123"),
        ("sarah_jones", "password123"),
        ("demo_voter", "demo123"),
    ]
    
    for i, (username, password) in enumerate(sample_users, 1):
        print(f"   {i}. Username: {username}")
        print(f"      Password: {password}")
        print(f"      Role: Voter")
        print()
    
    print("💡 USAGE NOTES:")
    print("   • Each voter can cast exactly one vote")
    print("   • Admin can add new candidates")
    print("   • All passwords should be changed in production")
    print("   • New users can register via the registration page")
    
    print("\n🌐 ACCESS:")
    print("   • Local: http://localhost:5000")
    print("   • Docker: http://localhost:5000 (SQLite) or http://localhost:5001 (PostgreSQL)")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    display_sample_accounts()