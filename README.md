# Voting Platform

A simple and secure Python web application for voting, built with Flask and deployable via Docker containers.

## Features

- **User Authentication**: Register and login functionality
- **Voting System**: Secure voting for registered users (one vote per user)
- **Candidate Management**: Admin interface to add and manage candidates
- **Real-time Results**: Live voting results with visual progress bars
- **Admin Dashboard**: Administrative interface with system statistics
- **Database Support**: Works with both SQLite and PostgreSQL
- **Docker Deployment**: Fully containerized application

## Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, Jinja2 Templates
- **Database**: SQLite (default) or PostgreSQL
- **Deployment**: Docker, Docker Compose

## Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   cd VotingPlatform
   ```

2. **Start with SQLite (simple setup)**:
   ```bash
   docker-compose up --build
   ```
   
3. **Access the application**:
   - Open http://localhost:5000 in your browser
   - Default admin credentials: `admin` / `admin123`
   - Sample user credentials: `john_doe` / `password123`, `jane_smith` / `password123`, `demo_voter` / `demo123`

### Option 2: PostgreSQL Database

1. **Start with PostgreSQL**:
   ```bash
   docker-compose --profile postgres up --build
   ```
   
2. **Access the application**:
   - Open http://localhost:5001 in your browser
   - Use the same sample credentials as listed above

### Option 3: Local Development

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Initialize database with sample users** (optional):
   ```bash
   python init_database.py
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## Sample Accounts

The application comes pre-configured with sample users for easy testing:

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Privileges**: Full admin access, can add candidates and view statistics

### Sample Voter Accounts
- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`
- **Username**: `mike_wilson` | **Password**: `password123`
- **Username**: `sarah_jones` | **Password**: `password123`
- **Username**: `demo_voter` | **Password**: `demo123`

**Note**: All sample accounts are regular voters (non-admin) and can cast one vote each.

## Usage Guide

### For Voters

1. **Register**: Create a new account on the registration page
2. **Login**: Use your credentials to access the voting dashboard
3. **Vote**: Select your preferred candidate and confirm your vote
4. **View Results**: Check real-time voting results

### For Administrators

1. **Login**: Use admin credentials to access administrative features
2. **Add Candidates**: Use the admin dashboard to add new candidates
3. **Monitor**: View system statistics and user activity
4. **Manage**: Access user and candidate information

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
SECRET_KEY=your-very-secret-key-change-this-in-production
DATABASE_URL=sqlite:///data/voting.db
FLASK_ENV=production
FLASK_DEBUG=False
```

### Database Configuration

- **SQLite** (default): `DATABASE_URL=sqlite:///data/voting.db`
- **PostgreSQL**: `DATABASE_URL=postgresql://user:password@host:port/database`

## Security Features

- Password hashing using Werkzeug security
- Session-based authentication
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection through Flask's built-in session management
- One vote per user enforcement

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with candidate overview |
| `/login` | GET/POST | User login |
| `/register` | GET/POST | User registration |
| `/dashboard` | GET | Voting dashboard (authenticated) |
| `/vote/<id>` | POST | Cast vote for candidate |
| `/results` | GET | View voting results |
| `/admin` | GET | Admin dashboard |
| `/logout` | GET | User logout |

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password`: Plain text password (⚠️ Not recommended for production)
- `has_voted`: Boolean flag
- `is_admin`: Admin privileges flag
- `created_at`: Registration timestamp

### Candidates Table
- `id`: Primary key
- `name`: Candidate name
- `party`: Political party (optional)
- `description`: Candidate description
- `votes`: Vote count
- `created_at`: Creation timestamp

### Votes Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `candidate_id`: Foreign key to Candidates
- `voted_at`: Vote timestamp

## Development

### Project Structure
```
VotingPlatform/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker image configuration
├── docker-compose.yml # Multi-container setup
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── login.html     # Login form
│   ├── register.html  # Registration form
│   ├── dashboard.html # Voting dashboard
│   ├── results.html   # Results display
│   └── admin.html     # Admin interface
└── .github/
    └── copilot-instructions.md
```

### Utility Scripts

- **`show_sample_users.py`**: Display all available sample accounts
- **`init_database.py`**: Initialize database with sample users and candidates

### Adding Features

1. **New Routes**: Add routes in `app.py`
2. **Templates**: Create HTML templates in `templates/`
3. **Models**: Extend database models in `app.py`
4. **Styling**: Modify Bootstrap classes in templates

## Deployment

### Production Deployment

1. **Update environment variables**:
   - Change `SECRET_KEY` to a secure random string
   - Set `FLASK_ENV=production` and `FLASK_DEBUG=False`
   - Configure production database

2. **Use production WSGI server**:
   ```dockerfile
   # Add to Dockerfile
   RUN pip install gunicorn
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

3. **Security considerations**:
   - Use HTTPS in production
   - Regular security updates
   - Database backups
   - Monitor access logs

### Scaling

- Use load balancers for multiple instances
- Separate database server
- Redis/Memcached for session storage
- CDN for static assets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Provide system information and error logs

---

**Note**: This is a demonstration application. For production use, implement additional security measures, comprehensive testing, and monitoring.