import itertools
import urllib2 as u
import pandas as pd

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

import robotparser
from bs4 import BeautifulSoup

from income import SalaryEstimates
# The Required dictionaries to be used later on in the script.
Dict, profile, profile_company = {}, {}, {}
# Lists
location_list = []
company_list = []
job_title = []


def allow():

    '''
    The purpose of this module will be to go to the robots.txt file and ask for access for  the parsing process
    to begin. If the robot.txt denies the required access, then the program will be halted and a message will be
    displayed explaining that we do not have the rights to parse the site.
    '''

    rp = robotparser.RobotFileParser()
    rp.set_url("http://www.indeed.com/robots.txt")
    rp.read()
    access = rp.can_fetch("*","http://www.indeed.com/jobs?q=python+analyst&l=CA" )
    return access


class Parser:
    def __init__(self):
        pass

    def data_parse(self, x, soup, job):

        '''

        :param x: x is the boolean parameter that is passed from the previous query with the robots.txt file./
         Once passed        then the first process will be to validate the required access, displaying a message/
            if it does not agree.
        :param job: (str) a list of jobs will be passed to determine which one has the most amount of jobs possible.
        :param soup: bs4 object
        :return: The process will return a Pandas DataFrame table that displays the quantity of jobs available/
         per query. For instance, Python engineer- 10,000 jobs available, Python Analyst- 5000 jobs e.t.c.

        '''

        # To check for access of the scraping process.
        if not x:
            print "defies the site rules"
            quit()

        # Once access is granted then the process starts parsing the data by first comparing the number/
        # of jobs available and returning the facts and figures.
        for text in soup.find_all("div", id="searchCount"):
            self.data = str(text.get_text()[16:]).replace(",","")
            job2 = job.replace("+", " ")
            Dict[job2] = self.data

        self.df = pd.DataFrame(Dict.items(), columns=['jobs', 'number of openings'])
        self.df = self.df.apply(pd.to_numeric, errors='ignore')
        return self.df

    def graph_parsed_data(self, username, api_key):

        '''
         At this process the program will access the Plotly api and graph the features that/
        were given by the first parsing process. The attributes that it will take in will be Api Username,
        ApiPassword or api_key
        :param username: this accesses is the api Username that you initially added in the first process.
        :param api_key: this is the api key that you receive after registration.
        :return: Final graph
        '''

        tls.set_credentials_file(username=username, api_key=api_key)
        data = [
            go.Scatter(
                x=self.df['jobs'], # assign x as the dataframe column 'x'
                y=self.df['number of openings']

            )
        ]
        final_graph = py.plot(data, filename='pandas/basic-bar')
        return final_graph


class TextParser:

    def __init__(self):
        pass

    def listed_jobs(self, jobs, soup):

        for post in soup.find_all("div", {"class":"  row  result"}):
            # job title
            jobs = post.find_all("a", {"class": "turnstileLink"})

            job_contents = (job.get_text(' ', strip=True) for job in jobs)
            job_title.append(job_contents)
            #           company Name
            companies = post.find_all("span", {"itemprop":"name"})
            company_content = (company.get_text(' ', strip=True) for company in companies)
            company_list.append(company_content)
            #           location
            locations = post.find_all("span", {"itemprop":"addressLocality"})
            locality = (location.get_text(' ', strip=True) for location in locations)
            location_list.append(locality)
        # return location_list
        profile["Job Title"] =(list(itertools.chain.from_iterable(job_title)))
        profile["Location"] = (list(itertools.chain.from_iterable(location_list)))
        profile_company["Company"] = (list(itertools.chain.from_iterable(company_list)))

        # Turning the list into a panda DataFrame which will have 3 columns. These columns/
        # include jobtitle, job location, and Company
        df3 = pd.DataFrame(profile_company)
        df4 = pd.DataFrame(profile).join(df3, how='left')
        return df4


# main module that manages all the other modules in the  script
def main(jobs):

    username = raw_input("please enter your Plotly Username: \n")
    api_key = raw_input("please enter your Plotly Api Key: \n")
    state = "CA"
    for job in jobs:
            url = "http://www.indeed.com/jobs?q=" + str(job) + "&l="+ str(state)+ "&rq=1&fromage=last"
            response = u.urlopen(url)

            response = response.read()
            soup = BeautifulSoup(response, "html.parser")
            allowance = allow()

            # Declaring the classes that have been used sequentially
            parser = Parser()
            text = TextParser()
            salary = SalaryEstimates()

            # functions that are present in these classes respectively
            items = parser.data_parse(allowance, soup, job)

            final = text.listed_jobs(job, soup)
            print "-~"*50
            print "-~"*50
            print "the requested job was", job
            print "-~"*50
            print final
            print "-~"*50
            print "-~"*50
            print "the requested job salary was "+job+" salary"
            print "-~"*50
            wage_compiled = salary.salary_parser(soup)
    print "\n"
    print "-~"*50
    print "-~"*50
    print "The total number of jobs in each field is"
    print "-~"*50
    print items
    # compares the total number of jobs visually on Plotly
    parser.graph_parsed_data(username, api_key)

    # runs the salary graph on Plotly
    salary.graphing_salary(username, api_key)

main(["python analyst", "civil engineer", "python"])
