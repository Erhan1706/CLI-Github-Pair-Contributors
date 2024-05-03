import click
import requests
import os
from dotenv import load_dotenv
import itertools


def get_repository_commits(repo_owner: str, repo_name: str, access_token: str = None, per_page: int = 10):
    """
    Retrieves the commits for a given repository.

    Args:
        repo_owner (str): The owner of the repository.
        repo_name (str): The name of the repository.
        access_token (str, optional): The access token for authentication. Defaults to None.
        per_page (int, optional): The number of commits to retrieve per page. Defaults to 10.

    Returns:
        Response: The response object containing the commits.
    """
    params = {"per_page": per_page}
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(url, params=params, headers=headers)

    return response


def get_changed_files_by_author(commits: list[str], repo_owner: str, repo_name: str, access_token: str = None):
    """
    Retrieves the number of times each file has been changed by each author in a given list of commits.

    Args:
        commits (list[str]): A list of commit hashes.
        repo_owner (str): The owner of the repository.
        repo_name (str): The name of the repository.
        access_token (str, optional): An optional access token for authentication. Defaults to None.

    Returns:
        dict: A dictionary containing the number of changes per file per author. The dictionary is structured as follows:
            {
                "author1": {
                    "file1": num_changes,
                    "file2": num_changes,
                    ...
                },
                "author2": {
                    "file1": num_changes,
                    "file3": num_changes,
                    ...
                },
                ...
            }
    """
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

def pairwise_comparison(top_k: int, authors: dict[str, dict[str, int]], extra_info=True):
    combinations = itertools.combinations(authors.keys(), 2)
    res = []
    for c in combinations:
        a1, a2 = c
        common_files = authors[a1].keys() & authors[a2].keys()
        sum, max = 0, 0
        max_file = None
        for file in common_files:
            n = min(authors[a1][file],authors[a2][file])
            sum += n
            if extra_info and n > max:
                max = n
                max_file = file
        if extra_info: res.append((a1, a2, sum, max, max_file))
        else: res.append((a1, a2, sum))

    res.sort(key=lambda tup: tup[2], reverse=True)
    display_results(res[:top_k], extra_info)

def display_results(res, extra_info):
    for i, r in enumerate(res):
        click.echo(f"{i+1}. {r[0]} and {r[1]}: {r[2]} common contributions")
        if extra_info:
            click.echo(f"    - Most commonly contributed file: {r[4]} with {r[3]} contributions")
        click.echo("\n")


@click.command()
@click.option('-owner', prompt=True, required= True, help='Repository owner')
@click.option('-repo', prompt=True, required = True, help='Repository name')
@click.option('--n', default=50, help='Number of commits to fetch')
@click.option('--num_pairs', default=5, help='Number of contributor pairs that will be displayed')
@click.option('--a', is_flag=True, help='Display extra repository information')
def main(num_pairs: int, owner: str, repo: str, n: int, a: bool):
    load_dotenv()
    access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
    commits = get_repository_commits(owner, repo , access_token, per_page=n)
    if not commits.ok:
        click.echo(f"Failed to fetch commits, check if the owner and repository name are correct. Error code: {commits.status_code}")
        return
    
    authors = get_changed_files_by_author(commits.json(), owner, repo, access_token)
    pairwise_comparison(num_pairs , authors=authors, extra_info=a)

if __name__ == '__main__':
    main()
