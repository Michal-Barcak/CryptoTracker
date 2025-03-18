# Crypto Tracker

## Requirements
- Python 3.10+
- PostgreSQL 12+

## Installation and Setup
### 1. Install PostgreSQL
   - Ubuntu/Debian:
      - `sudo apt update`
      - `sudo apt install postgresql`
      - `sudo systemctl start postgresql`
   - Windows: 
      - Download installer from [postgresql.org](https://www.postgresql.org/download/windows/)
   - macOS: 
      - `brew install postgresql` 
      - `brew services start postgresql`

### 2. Create Database and User
   - Ubuntu/Debian: `sudo -u postgres psql`
   - Windows: `psql -U postgres`
   - macOS: Simular as Ubuntu, or through Homebrew
   #### For all:
   - `CREATE DATABASE cryptodb;`
   - `CREATE USER cryptouser WITH PASSWORD 'heslo123';`
   - `GRANT ALL PRIVILEGES ON DATABASE cryptodb TO cryptouser;`
   - `\q`


### 3. Clone repo:
   - git clone [URL repo]


### 4. Create and activate virtual environment and install dependencies:
   - `python -m venv .venv`
   - Ubuntu/Debian: `source .venv/bin/activate` or Windows: `.venv\Scripts\activate`
   - `pip install -r requirements.txt`


### 5. Configure Database Connection 
   - The default database settings are in the `app/database.py` file
   - DATABASE_URL - complete connection string (e.g. postgresql://username:password@localhost/dbname)


### 6. Run application:
   - `uvicorn app.main:app --reload`
   - The application will be available at http://localhost:8000


# Using the Application
1. Open your web browser and go to http://localhost:8000

2. Use the search field to find a cryptocurrency by ID (e.g., bitcoin), check IDs here (https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?pli=1&gid=0#gid=0)

3. Information about the cryptocurrency will be displayed with an option to save it to the database

4. Locally stored crypto will be displayed in the table on the main page

5. If you want to update or delete a crypto stored in the db you need to search for it again and then press the update or delete button

6. Saved cryptocurrencies are automatically updated every 60 seconds

# API Endpoints
- GET /cryptocurrencies - Get all saved cryptocurrencies

- GET /cryptocurrency/{crypto_id} - Get a specific cryptocurrency from the database

- GET /cryptocurrency/info/{crypto_id} - Get cryptocurrency information from CoinGecko API

- POST /cryptocurrency?crypto_id={crypto_id} - Save a cryptocurrency to the database

- PUT /cryptocurrency/{crypto_id} - Update a cryptocurrency in the database

- DELETE /cryptocurrency/{crypto_id} - Delete a cryptocurrency from the database

# Swagger Documentation
- The API documentation is available at http://localhost:8000/docs

# Troubleshooting

## API Rate Limits
- CoinGecko has rate limits for the free API version. If you encounter rate limit errors, consider reducing the update frequency in the scheduler.py file.

