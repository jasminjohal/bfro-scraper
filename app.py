from flask import Flask
from flask import request
from scraper import scrape as sighting_scraper

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    state = request.args['state']
    num_sightings = request.args.get('numSightings', None)
    print(state, num_sightings)
    try:
        if num_sightings:
            results = sighting_scraper(state, int(num_sightings))
        else: 
            results = sighting_scraper(state)
        return {"data": results}
    except KeyError:
        return f'Invalid input'