from flask import Flask
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)

Base = automap_base()
Base.prepare(engine)

M = Base.classes.measurement
S = Base.classes.station


app = Flask(__name__)


@app.route('/')
def homepage():
    return f''' 
    <h1>Hawaii's Climate App</h1>

    <h3>Available routes:</h3>

    <ul>
        <li>/api/v1.0/precipitation</li>
        <li>/api/v1.0/stations</li>
        <li>/api/v1.0/tobs</li>
        <li>/api/v1.0/[start]</li>
        <li>/api/v1.0/[start]/[end]</li>

    </ul>
'''

@app.route('/api/v1.0/precipitation')
def precipitation():


    return { d:p for d,p in session.query(M.date, M.prcp).all()}




