import click
import requests
import os
from dotenv import load_dotenv
from pprint import pprint
import itertools


load_dotenv()

@click.command()
def hello():
    click.echo('Hello World!')


"""
def get_repository_contributors(repo_owner, repo_name, access_token= None):
    params = {"per_page": 100}
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(url, params=params, headers=headers)
    return response.json()
"""

def get_repository_commits(repo_owner: str, repo_name: str, access_token: str = None, per_page: int = 10):
    params = {"per_page": per_page}
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(url, params=params, headers=headers)

    return response.json()


def get_changed_files_by_author(commits: list[str], repo_owner: str, repo_name: str, access_token: str = None):
    headers = {"Authorization": f"token {access_token}"}
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"

    authors = {}
    for commit in commits:
        res = requests.get(f"{url}/{commit['sha']}", headers=headers).json()
        author = commit["commit"]["author"]["name"]
        if author not in authors:
                authors[author] = {}
        for file in res["files"]:
            filename = file["filename"]
            if filename not in authors[author]:
                authors[author][filename] = 1
            else:
                authors[author][filename] += 1
    return authors

def pairwise_comparison(top_k: int, authors: dict[str, dict[str, int]]):
    combinations = itertools.combinations(authors.keys(), 2)
    res = []
    for c in combinations:
        a1, a2 = c
        common_files = authors[a1].keys() & authors[a2].keys()
        sum = 0
        for file in common_files:
            sum += min(authors[a1][file],authors[a2][file])
        res.append((a1, a2, sum))
    res.sort(key=lambda tup: tup[2], reverse=True)
    return res[:top_k]


access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
commits = get_repository_commits("fesh0r", "fernflower", access_token)
authors = get_changed_files_by_author(commits, "fesh0r", "fernflower", access_token)
pairwise_comparison(5, authors=authors)

#headers = {"Authorization": f"token {access_token}", "author": "gorrus"}
#pprint(requests.get("https://api.github.com/rate_limit", headers=headers).json())

#if __name__ == '__main__':
#  hello()