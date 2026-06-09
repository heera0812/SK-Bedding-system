# Shantikunj Accommodation Register

Production-ready MVP for the Shantikunj Haridwar bedding counter. This system is only for issuing and returning bedding after visitors have already been registered and allotted rooms by the registration office.

## Features

- Flask backend with Blueprints
- SQLite development database through SQLAlchemy ORM
- Flask-Migrate/Alembic migration setup
- Persistent visitor issue/return records
- Inventory tracking for Gadda and Rajai
- Negative inventory prevention
- Fast2SMS integration hook using environment variables
- Dashboard metrics from database
- Issue bedding workflow with unique Issue ID like `SHK-000001`
- Return workflow searchable by Issue ID or mobile number
- Excel register export
- PDF daily summary export
- Responsive Bootstrap UI with Shantikunj branding

## Setup

1. Create virtual environment:

```bash
python -m venv .venv
```

2. Activate it:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment file:

```bash
copy .env.example .env
```

5. Initialize database:

```bash
flask db upgrade
flask init-db
```

6. Run the app:

```bash
flask run
```

Open `http://127.0.0.1:5000`.

## SMS Configuration

Local SMS is disabled by default.

Set these in `.env` when ready:

```env
SMS_ENABLED=true
FAST2SMS_API_KEY=your_api_key_here
```

SMS template:

```text
🙏 Shantikunj Haridwar

Issue ID: {issue_id}

Gadda: {gadda_qty}
Rajai: {rajai_qty}

Security Deposit: ₹{deposit}

Please show this message while returning bedding.
```

## Database Tables

`visitors`

- `id`
- `issue_id`
- `full_name`
- `mobile`
- `stay_days`
- `gadda_qty`
- `rajai_qty`
- `deposit_amount`
- `issue_datetime`
- `return_datetime`
- `status`

`inventory`

- `total_gadda`
- `available_gadda`
- `total_rajai`
- `available_rajai`
- `deposit_per_item`

## MySQL Upgrade Later

Change `DATABASE_URL` in `.env`, for example:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost/shantikunj
```

Then install the MySQL driver and run migrations:

```bash
pip install pymysql
flask db upgrade
```
