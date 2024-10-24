"""
    This program is to setup the flask application. After initializing the 
    app and connecting it with the DB the table is created in the DB. The 
    program also makes sure to keep only the latest data hence removes data
    pertaining to the previous fetches. Afterwards data is fetched from both
    user and API and tables get updated. Then the variables required for the
    desired ouput is passed on to the rendered template.

    Created Date : 22/10/2024
    Last Modified Date : 24/10/2024
"""

# importing necessary modules
from flask import Flask, request, render_template
from models import db, Weather2
import requests

# initializing the flask application
app = Flask(__name__)

# Configure the SQLite database wrt flask application.
# Initializing database connection.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Creating the weather table before any incoming requests.
@app.before_first_request
def setupDB():
    """ Delete all rows in the Weather2 table before each request.
    This will clear the existing data in the table but keep the schema intact.
    And make sure table structure exists in the DB.
    """
    Weather2.query.delete()
    db.session.commit()
    db.create_all()

# Defining route for the homepage.
@app.route('/', methods=['GET', 'POST'])
def index():
    """City will be taken from user input. From the API data for the next 15 days will be recieved.
    First record will be the current day's data. From this data required variables are taken.
    These variables are then added into the weather database.
    Returns:
        temperature variable is passed on to the index.html template.
    """
    temperature = None
    city = None
    description = None
    feelslike = None
    if request.method == 'POST':
        city = request.form['city']
        
        api_url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days&key=YZ52UXBEQZEMH3KVBR5LNNXCT&contentType=csv'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.text.splitlines()[1]
            temp_data = data.split(',')
            print(temp_data)
            description = temp_data[33].replace('"', '')
            feelslike = float(temp_data[9])
            city = temp_data[0].replace('"', '')
            temperature = float(temp_data[6])

            # Save to the database
            weather_entry = Weather2(city=city, temperature=temperature, feelslike=feelslike, description=description )
            db.session.add(weather_entry)
            db.session.commit()
        else:
            temperature = "Error fetching data"

    return render_template('index.html', city=city, temperature=temperature, feelslike=feelslike, description=description)

if __name__ == '__main__':
    app.run(debug=True)
