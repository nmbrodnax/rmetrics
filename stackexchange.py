# Stack Exchange API (no authentication)

import csv
import requests


def main():
    # test mode
    sites = ['stackoverflow']
    queries = ['zelig']

    # run mode
    # sites = ['stackoverflow', 'stats', 'datascience']
    # queries = ['zelig', 'time series', 'survey weight', 'bayes', 'gee', 'glm',
    #            'poisson', 'gamma', 'normal', 'probit', 'logit', 'ordered',
    #            'relogit', 'quantile', 'tobit', 'lognorm', 'exponential',
    #            'negative binomial', 'ivreg', 'hierarchical', 'multilevel',
    #            'random effects', 'mixed effects', 'fixed effects']

    # request data from stackexchange api
    questions = []
    for site in sites:
        for query in queries:
            q = get_questions('2016-08-06', '2017-08-06', site=site,
                              search=query + "&tagged=r", search_type='query',
                              page=1, pagesize=100)
            questions = [*questions, *q]

    # save results to csv file
    fieldnames = ['tags', 'view_count', 'answer_count', 'last_activity_date',
                  'creation_date', 'link', 'title', 'site', 'question_id',
                  'topic', 'search_type']

    with open("questions_by_topic.csv", "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        for question in questions:
            tmp = {}
            for field in fieldnames:
                tmp[field] = str(question.get(field))
            writer.writerow(tmp)


def get_questions(from_date, to_date, site, search, search_type='query',
                  page=1, pagesize=100):
    """Returns the results of an http GET request to the StackExchange API v2.2.
    Accepts dates in format YYYY-MM-DD.  Accepts search_type of 'query' to
    search question titles or 'tag' to search question tags.
    str, int -> Response object from requests library"""
    
    host = "https://api.stackexchange.com/2.2/search?"
    options = "&pagesize=" + str(pagesize) + "&fromdate=" + from_date + \
              "&todate=" + to_date + "&order=desc&sort=votes&site=" + site
    has_more = True 
    questions = []

    while has_more:
        if search_type not in ('query', 'tag'):
            has_more = False
            print("Invalid search_type value ('query' or 'tag' only).")
        elif search_type == 'query':
            url = host + "page=" + str(page) + options + "&intitle=" + search
        else:
            url = host + "page=" + str(page) + options + "&tagged=" + search
        response = requests.get(url)
        # print("API response: " + str(response))
        
        data = response.json()
        
        for dict_i in data['items']:
            dict_i['site'] = site
            dict_i['topic'] = search.split('&')[0]
            dict_i['search_type'] = search_type
            questions.append(dict_i)
        has_more = data['has_more']
        page += 1
    print(str(len(questions)) + " questions returned.")
    print("API quota remaining: " + str(data['quota_remaining']))
    return questions
    

if __name__ == '__main__':
    main()
