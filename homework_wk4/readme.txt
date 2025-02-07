- pip install -r requirements.txt

- start the flask application by running 'flask run'

- the app should now be running locally at http://127.0.0.1:5000/ (open http://127.0.0.1:5000/ or localhost:5000 in your browser)

Project Structure
- app/: contains the flask app and routes for handling search requests
- templates/: HTML templates for the app (e.g., index.html and results.html).
- search_engine_tfidf.py: ze main thing we've been working on
- .flaskenv: environment configuration. with this you don’t need to manually set the environment variables. flask will  automatically pick them up. (if you are not using .flaskenv, you would need to manually set the environment variables using commands like this:
For Windows:
set FLASK_APP=app
set FLASK_ENV=development
For Mac/Linux:
export FLASK_APP=app
export FLASK_ENV=development)
