Setup and run instructions for Shantikunj Bedding Management System

Prerequisites
- Python 3.11+ (virtualenv recommended)
- Git (optional)

Local setup (Windows)
1. Open PowerShell or CMD.
2. Create and activate virtualenv:
   python -m venv .venv
   .\.venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Copy example env and edit if needed:
   copy .env.example .env
   (Edit .env to set SMS_ENABLED=true and FAST2SMS_API_KEY if you want SMS)
5. Initialize database:
   python -c "from app import create_app; from app.extensions import db; app=create_app(); with app.app_context(): db.create_all()"
   (Alternatively: `flask --app run.py init-db` if Flask CLI is configured)
6. Run the app:
   python run.py

Testing workflows
- Open http://127.0.0.1:5000/ and use the UI to Issue and Return bedding.
- Reports: http://127.0.0.1:5000/reports to export Excel and PDF.

SMS (Fast2SMS)
- To enable SMS, set in `.env`:
  SMS_ENABLED=true
  FAST2SMS_API_KEY=your_api_key_here
  FAST2SMS_SENDER_ID=SHKREG

Notes
- The app uses SQLite at `instance/shantikunj.db` for persistence.
- Removed all references to ID Type, ID Number, and Dormitory/Hall from the standalone HTML.
