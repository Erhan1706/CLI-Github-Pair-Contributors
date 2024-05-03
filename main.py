import click
import requests
import os
from dotenv import load_dotenv
from pprint import pprint

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


def get_changed_files(commits: list[str], repo_owner: str, repo_name: str, access_token: str = None):
    headers = {"Authorization": f"token {access_token}"}
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"

    authors = {}
    for commit in commits:
        res = requests.get(f"{url}/{commit['sha']}", headers=headers).json()
        for file in res["files"]:
            if commit["author"]["login"] not in authors:
                authors[commit["author"]["login"]] = []
            cur_list = authors.get(commit["author"]["login"])
            if file["filename"] not in cur_list:
                cur_list.append( (file["filename"], 1))
            else:
                cur_list[file["filename"]] += 1
        print('')



access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
# res = get_repository_contributors("fesh0r", "fernflower", access_token)
#commits = get_repository_commits("fesh0r", "fernflower", access_token)
#get_changed_files(commits, "fesh0r", "fernflower", access_token)


#headers = {"Authorization": f"token {access_token}", "author": "gorrus"}
#pprint(requests.get("https://api.github.com/rate_limit", headers=headers).json())

#if __name__ == '__main__':
#  hello()