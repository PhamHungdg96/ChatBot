import requests
import csv
from cachetools import cached, TTLCache
from dateutil.parser import parse
"""
Base URL for fetching data.
"""
base_url = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-%s.csv';

def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False

def to_date(string, fuzzy=False):
    try:
        return parse(string, fuzzy=fuzzy)
    except ValueError:
        return ""

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_data(category):
    """
    Retrieves the data for the provided type.
    """

    # Adhere to category naming standard.
    category = category.lower().capitalize();

    # Request the data
    request = requests.get(base_url % category)
    text = request.text

    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))
    locations=[]
    for item in data:
        # Filter out all the dates.
        history = dict(filter(lambda element: is_date(element[0]), item.items()))

        # Normalize the item and append to locations.
        locations.append({
            # General info.
            'country': item['Country/Region'],
            'province': item['Province/State'],

            # Coordinates.
            'coordinates': {
                'lat': item['Lat'],
                'long': item['Long'],
            },

            # History.
            'history': history,

            # Latest statistic.
            'latest': int(list(history.values())[-1]),

            # Latest datetime.
            'latest_date': to_date(list(history.keys())[-1]).strftime("%d/%m/%Y"),
        })

    # Latest total.
    latest = sum(map(lambda location: location['latest'], locations))
    vn_latest = sum([location['latest'] for location in locations if location['country'] == 'Vietnam'])
    # Return the final data.
    return {
        'locations': locations,
        'latest': latest,
        'vn_latest': vn_latest,
        'global_latest': latest - vn_latest,
        'latest_date': locations[0]['latest_date']
    }