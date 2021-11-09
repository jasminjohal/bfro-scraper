import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

def find_counties(state):
    state_abbrev = us_state_to_abbrev[state].lower()
    STATE_URL = f'http://www.bfro.net/GDB/state_listing.asp?state={state_abbrev}'
    state_page = requests.get(STATE_URL)
    soup = BeautifulSoup(state_page.content, "html.parser")
    table = soup.find_all('table', {'class': 'countytbl'})

    table1 = table[0]
    table2 = table[1]
    data = []
    urls_to_visit = []
    table1_rows = table1.find_all('tr')
    table2_rows = table2.find_all('tr')
    for row in table1_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols[1] != "":
            data.append(cols[0].replace(" ", "+"))
    for row in table2_rows[1:]: # do not add header
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols[1] != "":
            data.append(cols[0].replace(" ", "+"))
    data.pop(0) # remove 'County' header
    return data

def scrape(state, num_sightings='All'):
    reports_df = [] # format: {'state': '', 'county': '', 'date': '', 'description': ''}
    state_abbrev = us_state_to_abbrev[state].lower()
    counties = find_counties(state)
    
    for county in counties:
        reports_available = False

        URL = f'https://www.bfro.net/GDB/show_county_reports.asp?state={state_abbrev.lower()}&county={county}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        headers = soup.body.find_all('h3')
        for header in headers:
            if header.text.strip() == "Reports:":
                reports_available = True
                break

        if reports_available:
            report_list = soup.find_all('ul')[0]
            reports = report_list.find_all('li')
            
            for report in reports:
                spans = report.find_all('span')
                date = spans[0].text.strip()
                # arbitrary set month to January if no month or season is included
                months_or_seasons = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Winter', 'Spring', 'Summer', 'Fall', 'Autumn']
                date_content = date.split(" ")
                if not any(x in date_content for x in months_or_seasons):
                    # print("BEFORE: ", date_content)
                    date = "January " + date
                    # print("AFTER: ", date)

                # replace 'Summer' with 'June', replace 'Fall' or 'Autumn' with September, 'Winter' with 'December', and 'Spring' with 'March'
                date = date.replace("Summer", "June")
                date = date.replace("Fall", "September")
                date = date.replace("Autumn", "September")
                date = date.replace("Winter", "December")
                date = date.replace("Spring", "March")

                # handle odd data entry
                if state == "New York" and county == "Steuben" and date == "August":
                    date = "August 1995" # https://www.bfro.net/GDB/show_report.asp?id=4643
                date = date.replace("May May 2020", "May 2020")
                date = date.replace("May May 29 201", "May 2016") # https://www.bfro.net/GDB/show_report.asp?id=51994
                date = date.replace("September Sep 2014", "September 2014")
                date = date.replace("Mid- to Late-1970s", "1975")
                date = date.replace("Mid 80", "1985")
                date = date.replace("est mid-70", "1975")
                date = date.replace("June Ongoing", "June 2000")
                date = date.replace("1/5/1998", "1998")
                date = date.replace("1970  1990", "1970")
                date = date.replace("2011 2012", "2011")
                date = date.replace("2002 1990", "2002")
                date = date.replace("1961 1962", "1961")
                date = date.replace("2005 2009", "2005")
                date = date.replace("1985   86", "1985")
                date = date.replace("197?", "1970")
                date = date.replace("(?)", "")
                date = date.replace("?", "")
                date = date.replace("~", "")
                date = date.replace("`", "")
                date = date.replace(" circa", "")
                date = date.replace("/", "-")
                date = date.replace(".", "-")
                date = date.replace("; ", "-")
                date = date.replace(";", "-")
                date = date.replace(" and ", "-")
                date = date.replace(" & ", "-")
                date = date.replace(" &", "-")
                date = date.replace(" or ", "-")
                date = date.replace(" to ", "-")
                date = date.replace(" thru ", "-")
                date = date.replace(" about ", " ")
                date = date.replace(" About ", " ")
                date = date.replace(" Around ", " ")
                date = date.replace(" app- ", " ")
                date = date.replace(" Maybe ", " ")
                date = date.replace(" maybe ", " ")
                date = date.replace(" mid ", " ")
                date = date.replace(" near ", " ")
                date = date.replace(" appro", "")
                date = date.replace("est-", "")
                date = date.replace(" until a few years ago", "")
                date = date.replace(" In the 1980's", "1980")
                date = date.replace("November1980", "November 1980")
                date = date.replace("Early 1990's", "1990")
                date = date.replace("early90s", "1990")
                date = date.replace("early 90", "1990")
                date = date.replace("90s", "1990")
                date = date.replace("'96", "1996")
                date = date.replace("71'", "1971")
                date = date.replace("'73", "1973")
                date = date.replace("'92", "1992")
                date = date.replace("20010", "2010")
                date = date.replace("Late 1950's", "1959")
                date = date.replace("Late1960", "1969")
                date = date.replace("late 60s", "1969")
                date = date.replace("Late 60", "1969")
                date = date.replace("Late 70's", "1979")
                date = date.replace("Late 70s", "1979")
                date = date.replace("Late '70's", "1979")
                date = date.replace("Late 1970s", "1970")
                date = date.replace("late 70", "1979")
                date = date.replace("Early 70", "1970")
                date = date.replace("Late 1970's", "1979")
                date = date.replace("1970s-1980s", "1975")
                date = date.replace("Early 1980s", "1980")
                date = date.replace("early 80", "1980")
                date = date.replace("1980s", "1980")
                date = date.replace("Late 1980", "1989")
                date = date.replace("Late 80", "1989")
                date = date.replace("Late 1980s", "1989")
                date = date.replace("79, 80, 99", "1999")
                date = date.replace("early 2000", "2000")
                date = date.replace("'s", "")
                date = date.replace(",", "-")
                
                # clip last year (e.g. "August 1976-77" -> "August 1976")
                if date.find('-') != -1:
                    date = date[0:date.find('-')].strip()

                # pad year if necessary (e.g. "July 99" -> "July 1999")
                date_content = date.split(" ")
                if len(date_content[1]) == 2:
                    # print("BEFORE: ", date_content)
                    if int(date_content[1]) >= 30:
                        date_content[1] = "19" + date_content[1]
                    else:
                        date_content[1] = "20" + date_content[1]
                    # print("AFTER: ", date_content)
                    date = " ".join(date_content)
                
                date = date.strip()
                formatted_date = dt.strptime(date, '%B %Y').strftime("%Y-%m")
                description = spans[2].text[3:] # exclude " - " 
                cur_report = {'state': state, 'county': county.replace("+", " "), 'date': formatted_date, 'description': description}
                reports_df.append(cur_report)
                # print("successful: ", county)

    reports_df.sort(key=lambda x: x["date"], reverse=True)
    if num_sightings == 'All':
        return reports_df
    else:
        return reports_df[0:num_sightings]
    
def main():
    state = "Virginia"
    sightings = scrape(state, 5)
    print(sightings)

    # starting = "Alabama"
    # states = list(us_state_to_abbrev.keys())
    # for state in states[states.index(starting):]:
    #     print(f"Scraping sightings for {state}...")
    #     results = scrape(state, 5)
    #     print(results)
    #     print("----------------------------------------")

if __name__ == "__main__":
    main()


