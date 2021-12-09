import datetime as dt
import os
import dateutil.relativedelta as du
import requests
import sys
from bs4 import BeautifulSoup
from bs4 import re
from github import Github
from scoringscript import *


def metadata_collect(url):
    npm_flag = "https://www.npmjs.com"
    if npm_flag in url:
        headers = {'Accept-Encoding': 'identity'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        all_links = soup.find_all('a', attrs={'aria-labelledby':'repository'})
        url = all_links[0].get('href')

    url = url.replace("https://github.com/", "")

    token = os.getenv('GITHUB_TOKEN')

    g = Github(token)
    reps = g.get_repo(url)

    content_list = reps.get_contents("")
    p_list = []

    for elem in content_list:
        p_list.append(elem.path)
    mit = "MIT"
    gnu = "GNU"
    apache = "Apache"
    affero = "Affero"
    bsd = "BSD"
    mit_l = mit.lower()
    gnu_l = gnu.lower()
    apache_l = apache.lower()
    affero_l = affero.lower()
    bsd_l = bsd.lower()

    git_name = 'LICENSE'
    if git_name in p_list:
        li = reps.get_license().decoded_content
        li = li.title().decode()
        if mit_l in li.lower() or gnu_l in li.lower() or apache_l in li.lower() or affero_l in li.lower() \
                or bsd_l in li.lower():
            lic = 1
        else:
            lic = 0
    else:
        lic = 0

    git_name = 'README.md'
    if git_name in p_list:
        li = reps.get_readme().decoded_content
        li = li.title().decode()
        if lic != 1:
            if mit_l in li.lower() or gnu_l in li.lower() or apache_l in li.lower() or affero_l in li.lower() \
                    or bsd_l in li.lower():
                lic = 1
            else:
                lic = 0
        rm = 1
    else:
        rm = 0

    if reps.has_wiki:
        wiki = 1
    else:
        wiki = 0

    git_name = 'CONTRIBUTING.md'
    if (git_name or 'ISSUE_TEMPLATE') in p_list:
        contri = 1
    else:
        contri = 0

    today = dt.datetime.now()
    date_lm = today + du.relativedelta(months=-1)

    # trying to get issues from the last month
    issues_total1 = reps.get_issues(since=date_lm, state='all').totalCount
    issues_closed1 = reps.get_issues(since=date_lm, state='closed').totalCount
    if issues_total1:
        per_close_1 = (issues_closed1 / issues_total1) * 100
    else:
        per_close_1 = 0
    date_llm = date_lm + du.relativedelta(months=-1)
    issues_total2 = reps.get_issues(since=date_llm, state='all').totalCount - issues_total1
    issues_closed2 = reps.get_issues(since=date_llm, state='closed').totalCount - issues_closed1
    if issues_total2:
        per_close_2 = (issues_closed2 / issues_total2) * 100
    else:
        per_close_2 = 0

    date_lllm = date_llm + du.relativedelta(months=-1)
    issues_total3 = reps.get_issues(since=date_lllm, state='all').totalCount - issues_total1 - issues_total2
    issues_closed3 = reps.get_issues(since=date_lllm, state='closed').totalCount - issues_closed1 - issues_closed2
    if issues_total3:
        per_close_3 = (issues_closed3 / issues_total3) * 100
    else:
        per_close_3 = 0

    avg_per_close = (per_close_1 + per_close_2 + per_close_3) / 3
    # print(avg_per_close)

    cont = reps.get_contributors(anon='True').totalCount  # number of contributors for the repo
    issues_close_time = reps.get_issues(since=date_lm, state='closed')
    cr_time = []
    end_time = []
    # print((cr_time))
    iss_check = reps.get_issues(since=date_lm, state='closed').totalCount
    if iss_check > 0:
        for issues in issues_close_time:
            cr_time.append(issues.created_at.day)
            end_time.append(issues.closed_at.day)
        time_taken = [m - n for m, n in zip(end_time, cr_time)]
        avg_response_time = sum(time_taken) / len(time_taken)
        # print(avg_response_time)
    else:
        avg_response_time = 10000

    metadata_dict = {
        "readme": rm,  # Ramp-up score
        "contributing": contri,  # Ramp-up score
        "documentation": wiki,  # Ramp-up score
        "average %issues closed": avg_per_close,  # Correctness score
        "number_contributors": cont,  # Bus-factor score
        "average time": avg_response_time,  # Responsive Maintainer Score
        "license": lic  # License score
    }
    return metadata_dict


# Code by @Richard-Rhee
def url_parser(filename):
    # urls = []
    with open(filename) as f:
        urls = f.read().splitlines()
    return urls


def api_url_generator(urls):
    github_api = "https://github.api.com"
    api_urls = []
    for url in urls:
        url = url.replace("https://github.com", "/repos")
        url = github_api + url
        api_urls.append(url)
    return api_urls


# Code by @Richard-Rhee

def main():
    filename = "URL.txt"
    url = url_parser(filename)
    # api_urls = api_url_generator(urls)
    # i = 0
    url = url[0]
    backup_url = url
    # print(url)
    metadata_dict = metadata_collect(url)
    # print(metadata_dict)
    scoring(backup_url, metadata_dict)


if __name__ == "__main__":
    main()
