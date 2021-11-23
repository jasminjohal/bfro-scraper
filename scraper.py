import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

from requests.api import get

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

def get_state_abbrev(state):
    """Accept a state and return its lowercased abbreviation"""
    return us_state_to_abbrev[state].lower()

def get_state_page_content(state):
    """Return the scraped contents of a state page on bfro.net"""
    state_abbrev = get_state_abbrev(state)
    STATE_URL = f'http://www.bfro.net/GDB/state_listing.asp?state={state_abbrev}'
    state_page = requests.get(STATE_URL)
    soup = BeautifulSoup(state_page.content, "html.parser")
    return soup

def get_county_names_from_table(table):
    """Return a list of county names from an HTML table on bfro.net"""
    county_list = []
    table_rows = table.find_all('tr')
    for row in table_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # store a county only if it has listings
        if cols[1] != "": 
            # transform the county name if there is a space so that the resulting URL is valid
            # (e.g. 'Chesapeake City' -> 'Cheseapeake+City')
            county_list.append(cols[0].replace(" ", "+"))
    county_list.pop(0) # remove table header
    return county_list

def get_all_counties(state_page):
    """Return a list of counties that have listings for the passed state page on bfro.net"""

    # each state webpage contains two tables side-by-side
    table = state_page.find_all('table', {'class': 'countytbl'})
    table1 = table[0]
    table2 = table[1]

    # get list of counties from the two tables
    table1_counties = get_county_names_from_table(table1) 
    table2_counties = get_county_names_from_table(table2) 

    # combine data from 2 tables into 1 array 
    counties = table1_counties + table2_counties
    return counties

def get_county_page_content(county, state):
    """Return HTML content of a county page on bfro.net"""
    state_abbrev = get_state_abbrev(state)
    URL = f'https://www.bfro.net/GDB/show_county_reports.asp?state={state_abbrev.lower()}&county={county}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def county_has_reports(county_page):
    """Return True if the county page contains reports; return False otherwise"""
    headers = county_page.body.find_all('h3')
    for header in headers:
        if header.text.strip() == "Reports:":
            return True
    return False

def handle_data_entry(state, county, date):
    """Accept a date string, wrangle it to handle data entry issues, and return date"""
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
    return date

def season_to_month(date):
    """Accept a date string, replace a season with a month (if applicable), and return the date"""
    date = date.replace("Summer", "June")
    date = date.replace("Fall", "September")
    date = date.replace("Autumn", "September")
    date = date.replace("Winter", "December")
    date = date.replace("Spring", "March")
    return date

def add_month_to_date(date):
    """Accept a date string, arbitrarily set month to January if no month or season is included, and return the date"""
    months_or_seasons = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Winter', 'Spring', 'Summer', 'Fall', 'Autumn']
    date_content = date.split(" ")
    if not any(x in date_content for x in months_or_seasons):
        date = "January " + date
    return date

def format_date(date):
    """Accept a date string, format it as needed to the form 'Month YYYY', and return the date"""

    # clip last year (e.g. "August 1976-77" -> "August 1976")
    if date.find('-') != -1:
        date = date[0:date.find('-')].strip()

    # pad year if necessary (e.g. "July 99" -> "July 1999")
    date_content = date.split(" ")
    if len(date_content[1]) == 2:
        if int(date_content[1]) >= 30:
            date_content[1] = "19" + date_content[1]
        else:
            date_content[1] = "20" + date_content[1]
        date = " ".join(date_content)

    return date

def process_date(state, county, date):
    """Accept a date string, wrangle it to the form 'Month YYYY' and convert it to datetime, and return it"""
    # date entries are prone to data entry and must be heavily wrangled
    date = add_month_to_date(date) # arbitrarily set the month to 'January' if there is only a year
    date = season_to_month(date) # replace 'Summer' with 'June', replace 'Fall' or 'Autumn' with September, 'Winter' with 'December', and 'Spring' with 'March'
    date = handle_data_entry(state, county, date) # process data entry issues in date such as unexpected characters
    formatted_date = format_date(date)
    formatted_date = convert_str_to_date(formatted_date)
    return formatted_date

def convert_str_to_date(date):
    """Transform date string to date from format 'July 2019' to 2019-07"""
    date = date.strip()
    formatted_date = dt.strptime(date, '%B %Y').strftime("%Y-%m")
    return formatted_date

def get_county_reports(state, county, county_page):
    """Returns an object containing all reports on a county page"""

    reports_df = [] # format: {'state': '', 'county': '', 'date': '', 'description': ''}
    report_list = county_page.find_all('ul')[0]
    reports = report_list.find_all('li')
    
    for report in reports:
        spans = report.find_all('span')

        # get date from report 
        date = spans[0].text.strip()
        date = process_date(state, county, date)

        # get description from report
        description = spans[2].text[3:] # exclude " - " 

        # store report
        cur_report = {'state': state, 'county': county.replace("+", " "), 'date': date, 'description': description}
        reports_df.append(cur_report)

    return reports_df

def scrape(state, num_sightings='All'):
    """Return an object containing the designated number of sightings for the passed state"""

    reports_df = [] 
    state_page = get_state_page_content(state)
    counties = get_all_counties(state_page) 

    # visit each county page for a state
    for county in counties:
        # scrape content of county page
        county_page = get_county_page_content(county, state)

        # check if county page has any reports; if so, store them
        reports_available = county_has_reports(county_page)
        if reports_available:
            county_reports = get_county_reports(state, county, county_page)
            reports_df.extend(county_reports)
            # print("SUCCESSFULLY SCRAPED: ", county)

    # sort the reports by date in descending order
    reports_df.sort(key=lambda x: x["date"], reverse=True)

    # return the number of sightings specified by the user; return all by default
    if num_sightings == 'All':
        return reports_df
    else:
        return reports_df[0:num_sightings]

def main():
    # test single state
    state = "Virginia"
    sightings = scrape(state, 5)
    print(sightings)

    # test multiple states
    # starting = "Alabama"
    # states = list(us_state_to_abbrev.keys())
    # for state in states[states.index(starting):]:
    #     print(f"Scraping sightings for {state}...")
    #     results = scrape(state, 5)
    #     print(results)
    #     print("----------------------------------------")

if __name__ == "__main__":
    main()


