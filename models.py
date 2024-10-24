"""
    A database instance is created using SQLAlchemy. A table
    named model is defined aferwards. The data retrieved from 
    API will be stored in this table before retriving further.
    
    Created Date : 22/10/2024
    Last Modified Date : 24/10/2024 
"""

# importing necessary modules
from flask_sqlalchemy import SQLAlchemy

# Initializing instance of SQLAlchemy. 
# This is used to ensure connection between DB and app as well as other DB related tasks.
db = SQLAlchemy()

# Defining a class and creating a table named Model in the DB. 
# Attributes of the table is defined in the class
class Weather2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    feelslike = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """ Provides a string representation of objects in the class Weather.
        """
        return f'<Weather in {self.city} is {self.description}. Temperature is {self.temperature}°C but feelslike {self.feelslike}>'
