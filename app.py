import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()
year = str(1986)
URL = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fleagues%2FMLB%2F" + year + \
    "-standings.shtml&div=div_expanded_standings_overall&del_col=1,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30"
r = session.get(URL)
print(r)

soup = BeautifulSoup(r.content, 'html.parser')

results = soup.find(id="expanded_standings_overall")

f = open("view.html", "w")
f.write(results.prettify())
f.close()

# 2020_record = results.find_all('section', class_='')
# print(results.prettify())
