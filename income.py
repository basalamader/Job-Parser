import re
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls


class SalaryEstimates:
    def __init__(self):
        pass

    def salary_parser(self, soup):
        '''
        :param soup: beautiful soup object defined at the main module.
        :return: returns a pandas DataFrame
        '''

        rx = re.compile('([+(),])')
        for post in soup.find_all("ul", {"class":"rbList"}):

            figures = post.get_text(' ', strip=True)
            figures = list(rx.sub(r'', figures).replace(' ', ', ').split())

            quantity = [elem.replace(',','') for elem in figures if '$' not in elem]

            salary = [elem.replace('$', '').replace(',','') for elem in figures if '$' in elem]

            d = {'Salary from jobs': pd.Series(salary, index=['a', 'b', 'c','d','e']),
                 'Quantity': pd.Series(quantity, index=['a', 'b', 'c', 'd', 'e'])}
            self.df5 = pd.DataFrame(d)
            self.df5 = self.df5.apply(pd.to_numeric, errors='coerce')
            print self.df5
            df5_median =self.df5['Salary from jobs'].median()
            df5_mean = self.df5['Salary from jobs'].mean()

            print "The median for this job is:", df5_median
            print "The mean for this job is:", df5_mean
            return self.df5

    def graphing_salary(self, username, api_key):
        '''

        :param username: str. This is the Plotly api username that you gave beforehand
        :param api_key: str. Plotly api_key
        :return: graphical output of the job selected.
        '''

        # authorizing the user Plotly credentials
        tls.set_credentials_file(username=username, api_key=api_key)

        # creating a Plotly scatter object
        data = [
            go.Scatter(
                x=self.df5['Quantity'],
                y=self.df5['Salary from jobs']

            )
        ]
        final_graph = py.plot(data, filename='pandas/basic-bar')
        return final_graph



