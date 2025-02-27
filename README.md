Dependencies
Listed in requirements.txt:

fastapi: Web framework
sqlalchemy: ORM
pydantic: Validation
mysql-connector-python: MySQL driver
python-jose: JWT handling
fastapi-cache2: Caching

Install with:
pip install -r requirements.txt

Environment Configuration
Database URL: Set in models/database.py.
JWT Secret: Hardcoded as SECRET_KEY in dependencies/auth.py (consider using environment variables in production).
Example with .env (not implemented but recommended):
bash
Wrap
Copy
echo "SECRET_KEY=your-secret-key" > .env
Then use python-dotenv to load it.