# Stack Exchange API (no authentication)

import csv
import requests

def main():
    host = "https://api.stackexchange.com/2.2/search"
    subset = "?fromdate=2016-08-06&todate=2017-08-06&order=desc&sort=votes"
    site = "stackoverflow"
    query = "zelig"
    tag = "r"

    sites = ['stackoverflow', 'stats', 'datascience']
    queries = ['zelig', 'weights', 'bootstrap', 'hierarchical', 'multilevel',
               'time series', 'visualization', 'plot', 'database']
    tags = ['r', 'r-zelig', 'statistics']
    
    # request data from stackexchange api 
    response = get_questions('2017-01-01', '2017-08-06', 'stackoverflow',
                         search = 'zelig', search_type = 'query')
    data = response.json()
    print("StackExchange API quota remaining: " + str(data['quota_remaining']))
    questions = data['items']  # list of dictionaries
    
    # save results to csv file
    fieldnames = ['tags', 'view_count', 'answer_count', 'last_activity_date',
                  'creation_date', 'link', 'title', 'site', 'query']

    with open("stackexchange.csv", "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        for question in questions:
            tmp = {}
            for field in fieldnames:
                tmp[field] = str(question.get(field))
            writer.writerow(tmp)


def get_questions(from_date, to_date, site, search, search_type = 'query'):
    """Returns the results of an http GET request to the StackExchange API v2.2.
    Accepts dates in format YYYY-MM-DD.  Accepts search_type of 'query' to
    search question titles or 'tag' to search question tags.
    str -> Response object from requests library"""
    
    url = "https://api.stackexchange.com/2.2/search?" + "fromdate=" + \
          from_date + "&todate=" + to_date + "&order=desc&sort=votes&site=" + \
          site
    
    if search_type == 'query':
        return requests.get(url + "&intitle=" + search)
    elif search_type == 'tag':
        return requests.get(url + "&tagged=" + search)
    else:
        print("Invalid search_type value ('query' or 'tag' only).")


if __name__ == '__main__':
    main()
