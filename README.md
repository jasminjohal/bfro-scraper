# BFRO Scraper

Flask application that scrapes Bigfoot sightings from [https://bfro.net/](https://bfro.net/) for a particular state and returns a JSON object containing a list of the sightings. It was developed for the CS 361 course (Software Engineering I) at Oregon State University.

## Get list of sightings in a state

### Request

`GET /`

```sh
curl -X GET 'https://bfro-scraper.herokuapp.com/?state=Vermont'
```

_Make sure the state is capitalized._

### Response

    HTTP/1.1 200 OK
    Date: Sun, 26 Jun 2022 21:53:52 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 1397

```json
{
  "data": [
    {
      "county": "Lamoille",
      "date": "2019-08",
      "description": "Daylight sighting of a Bigfoot near N. Branch Lamoille River in Eden",
      "state": "Vermont"
    },
    {
      "county": "Washington",
      "date": "2015-11",
      "description": "Possible encounter while hunting near Northfield Falls",
      "state": "Vermont"
    },
    {
      "county": "Windham",
      "date": "2015-10",
      "description": "Couple have possible early morning sighting while driving outside Brattleboro",
      "state": "Vermont"
    },
    {
      "county": "Windsor",
      "date": "2015-05",
      "description": "Possible footprints found by a hiker on Mt. Ascutney",
      "state": "Vermont"
    },
    {
      "county": "Windsor",
      "date": "2005-10",
      "description": "Evening sighting by motorists on Tyson Road, off Route 100, outside Ludlow",
      "state": "Vermont"
    },
    {
      "county": "Bennington",
      "date": "2005-08",
      "description": "Possible stalking at Hildene Mansion grounds, near Manchester",
      "state": "Vermont"
    },
    {
      "county": "Lamoille",
      "date": "1995-06",
      "description": "Highpitched vocalizations heard near Morrisville",
      "state": "Vermont"
    },
    {
      "county": "Rutland",
      "date": "1995-06",
      "description": "Possible prowling at TinkerBrook shelter in Calvin Coolidge State Forest",
      "state": "Vermont"
    },
    {
      "county": "Lamoille",
      "date": "1989-12",
      "description": "Family discovers fresh footprints in the snow while cutting down a Christmas tree",
      "state": "Vermont"
    },
    {
      "county": "Chittenden",
      "date": "1984-11",
      "description": "Stranded motorists observe white creature near Colchester",
      "state": "Vermont"
    }
  ]
}
```
