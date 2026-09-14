# Harbor & Pine Outfitters

A small local online-store and order-management application for practicing QA and software-testing workflows.

## Setup

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment (recommended).
3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Initialize the sample database:

   ```powershell
   python reset_db.py
   ```

## Start the application

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## Test login

Username: `alex.morgan`  
Password: `Welcome123!`

## Reset the database

```powershell
python reset_db.py
```
