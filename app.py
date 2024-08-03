from flask import Flask, jsonify
import numpy as np
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
        <li><a href="/api/v1.0/precipitation">Precipitation</a></li>
        <li><a href="/api/v1.0/stations">Stations</a></li>
        <li><a href="/api/v1.0/tobs">Tobs</a></li>
        <li><a href="/api/v1.0/2016-01-01">Start date can be between 2010-01-01 and 2017-08-23</a></li>
        <li><a href="/api/v1.0/2016-08-23/2017-08-23">Start and End dates can be between 2010-01-01 and 2017-08-23</a></li>

    </ul>
'''

@app.route('/api/v1.0/precipitation')
def precipitation():
    return { d:p for d,p in session.query(M.date, M.prcp).filter(M.date>='2016-08-23').all()}

@app.route('/api/v1.0/stations')
def stations():
    return { id:loc for id,loc in session.query(S.station, S.name).all()}

@app.route('/api/v1.0/tobs')
def tobs():
    return { d:t for d,t in session.query(M.date, M.tobs).all()}

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def date_range(start,end='2017-08-23'):

    sel = [func.min(M.tobs),func.avg(M.tobs),func.max(M.tobs)]
    filter = (M.date>=start)&(M.date<=end)

    result = session.query(*sel).filter(filter).first()
    
    return { 
        '1_Min_Temp':result[0], 
        '2_Avg_Temp': result[1], 
        '3_Max_Temp':result[2], 
        '4_Start_date':start, 
        '5_End_date':end 
    }


