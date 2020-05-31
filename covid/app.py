
from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
import bs4
from   bs4 import BeautifulSoup as bs
from urllib.request import urlopen,Request

app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
@cross_origin()
def home_page():
    return  render_template('index.html')

@app.route('/details',methods = ['GET','POST'])
@cross_origin()
def display_name():
    if(request.method == 'POST'):
        s = str(request.form['content'])
        header = {'User-Agent': 'Mozilla'}

        url = "https://www.worldometers.info/coronavirus/country/" + s
        req = Request(url, headers=header)

        html = urlopen(req)
        html_content = bs(html, 'html.parser')

        total_cases = html_content.find_all("div", {"class": "maincounter-number"})
        tot_cases = total_cases[0].text.split()[0]
        tot_deaths = total_cases[1].text.split()[0]
        tot_recovered = total_cases[2].text.split()[0]

        new_cases = html_content.find("li", {"class": "news_li"}).strong.text.split()[0]

        death = list(html_content.find("li", {"class": "news_li"}).strong.next_siblings)
        deaths = death[1].text.split()[0]
        if (deaths.isnumeric()):
            pass
        else:
            deaths = "No Updates"

        r = [s,tot_cases,tot_deaths,tot_recovered,new_cases,deaths]
    return render_template('result.html',res=r)




if __name__ == "__main__":
    app.run(port=8000,debug=True)