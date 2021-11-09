from flask import Flask
from flask import request
from test import scrape as sighting_scraper

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

# @app.route("/state/<state>/", defaults={'amount': 'All'})
# @app.route("/state/<state>/<amount>")
# def scrape(state, amount):
#     if amount == 'All':
#         results = sighting_scraper(state)
#     else:
#         results = sighting_scraper(state, int(amount))
#     return results

# app.run(host='0.0.0.0', port=5000)