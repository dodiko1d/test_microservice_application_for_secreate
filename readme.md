# Microservice for stock counting.

## Main Stack
* [Python 3.8](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [pytest](https://docs.pytest.org/) feat [FastAPI Test Testing](https://fastapi.tiangolo.com/tutorial/testing/) usage

## Easy launch

####1. [install python 3.8](https://www.python.org/downloads/release/python-383/)

####2. run command below in terminal
        pip install -r requirements.txt

####3. run next command to create SQLite database.
        python -m database.py (python3 for linux)
####4. Start development server:
        uvicorn main:app --reload

####5. Run tests using:
        python -m pytest (python3 for linux)

