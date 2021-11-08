import ranking_module
from coverage import Coverage
from github import Github, GithubException
import sys
import datetime
import logging
import os


def run_test_suite(input_file1, input_file2):
    level = os.environ.get('$LOG_LEVEL')
    LOG_FILE = os.environ.get('$LOG_FILE')
    GITHUB_TOKEN = os.environ.get('$GITHUB_TOKEN')
    

    level = '0'

    if level == '0':
        LOG_LEVEL = logging.NOTSET
    elif level == '1':
        LOG_LEVEL = logging.INFO
    elif level == '2':
        LOG_LEVEL = logging.DEBUG
    else:
        logging.error(f"Log level {level} is not defined")
        sys.exit()

    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL)
    cov = Coverage()
    cov.start()
    try:
        g = Github(login_or_token=GITHUB_TOKEN)
    except GithubException:
        logging.error("Invalid token used")
        sys.exit()
        
        
    print (g)

    repos, others = ranking_module.parse_input(input_file1, g)
    before = datetime.datetime.now()  # Timing runtime of program

    repos = ranking_module.get_repos(g, repos)
    test_num = 0
    scores = [ranking_module.get_ramp_up_scores(repos), ranking_module.get_responsiveness_scores(repos),
              ranking_module.get_license_scores(repos), ranking_module.get_bus_factor_scores(repos),
              ranking_module.get_correctness_scores(repos)]

    score_1 = [item[0] for item in scores]
    if score_1 == [-1, -1. - 1. - 1. - 1, -1]:  # google should not output anything but -1
        test_num += 1
    score_2 = [item[1] for item in scores]
    if score_2 == [-1, -1. - 1. - 1. - 1, -1]:  # github.com is not a valid repo, only -1
        test_num += 1
    score_3 = [item[2] for item in scores]
    if score_3 == [-1, -1. - 1. - 1. - 1, -1]:  # not a valid repository, only -1
        test_num += 1
    score_4 = [item[3] for item in scores]  # valid repository, private, low score
    if score_4 != [-1, -1. - 1. - 1. - 1, -1]:
        test_num += 1

    ranking_module.output_result(scores, repos, others)

    logging.info('Runtime:', (datetime.datetime.now() - before).seconds, 'seconds')

    repos, others = ranking_module.parse_input(input_file2, g)  # checking if the algo works with just 1 url in the
    # file

    datetime.datetime.now()

    repos = ranking_module.get_repos(g, repos)

    if len(repos) == 1:
        logging.error("Input needs at least two links")
        print(f"{repos[0]} -1 -1 -1 -1 -1 -1")
        test_num += 1

    print("total tests = 2")
    print("tests passed = " + str(test_num))

    cov.stop()
    cov.save()
    cov.html_report()
