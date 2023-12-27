import sys
import yaml
import requests
import tldextract
import time

#Loading yaml file
with open(sys.argv[1], 'r') as file:
    http_input = yaml.safe_load(file)

#data structure to store availability of domain
url_domain={}  

#Parsing yaml contents to dictionary
def parse_input(input):
    for http_request in input:
        url = http_request['url']
        ext = tldextract.extract(url)
        domain = ext.domain + '.' + ext.suffix
        http_request['domain'] = domain
        if domain not in url_domain:
            url_domain[domain] = {'UP': 0,
                                'DOWN':0}

        if 'headers' not in http_request:
            http_request['headers'] = None
        
        if 'body' not in http_request:
            http_request['body'] = None

        if 'method' not in http_request:
            http_request['method'] = 'GET'

    return input

#Checking availability of url
def check_url(http_request):
    response = requests.request(method=http_request['method'],url=http_request['url'],headers=http_request['headers'],data=http_request['body'])

    if response.status_code >= 200 and response.status_code <= 299:
        if response.elapsed.total_seconds() < 0.5:
            url_domain[http_request['domain']]['UP']+=1
            return

    url_domain[http_request['domain']]['DOWN']+=1



http_input = parse_input(http_input)
while True:
    #Test Cycle
    for http_request in http_input:
        check_url(http_request)

    #Calculating availability at the end of the cycle
    for domain,domain_availability in url_domain.items():
        availability = round(domain_availability['UP']*100/(domain_availability['UP']+domain_availability['DOWN']))
        print('{0} has {1}% availabilty percentage'.format(domain,availability))

    #Sleeping 15 sec before running test cycle again
    time.sleep(15)





