import requests
from bs4 import BeautifulSoup

def request_github_trending(url):
    return requests.get(url)

def extract(page):
    soup = BeautifulSoup(page.text, "html.parser")
    return soup.find_all("article")

def transform(html_repos):
    result = []
    for row in html_repos:
        REPOS_NAME = ''.join(row.select_one('h1.h3.lh-condensed').text.split())
        NBR_STARS = ' '.join(row.select_one('span.d-inline-block.float-sm-right').text.split())
        try:
            NAME = row.select_one('img.avatar.mb-1.avatar-user')['alt']
        except:
            NAME = 'hidden_name'
        result.append({'developer': NAME, 'repository_name': REPOS_NAME, 'nbr_stars': NBR_STARS})
    return result

def format(repositories_data):
    result = ['Developer, Repository Name, Number of Stars']
    for repos in repositories_data:
        row = [repos['developer'], repos['repository_name'], repos['nbr_stars']]
        result.append(', '.join(row))
    return '\n'.join(result)


def _main():
    url = 'https://github.com/trending'
    page = request_github_trending(url)
    html_repos = extract(page)
    repositories_data = transform(html_repos)
    print(format(repositories_data))

_main()
