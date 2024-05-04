# Github Pair Contributors CLI
CLI tool developed with Python 3.10.2 to calculate the pairs of developers who most frequently contribute to the same files/modules in a GitHub repository. 
## Installation
Clone the repository with: 
~~~ 
git clone https://github.com/Erhan1706/CLI-Github-Pair-Contributors.git
~~~ 
Navigate to the directory
~~~
cd CLI-Github-Pair-Contributors
~~~
*(Optional)* Create a virtual environment
~~~ 
python3 -m venv .venv
~~~ 
*(Optional)*  Activate the virtual environment
~~~ 
.venv\Scripts\activate (Windows)
source .venv/bin/activate (Linux)
~~~ 
Install all the dependencies
~~~ 
pip install -r requirements.txt
~~~
Create a .env file and add your personal access token:
~~~ 
GITHUB_ACCESS_TOKEN=<token>
~~~
Or add your access token to the following line in main.py: 
~~~ 
access_token = <token>
~~~
Note that this is highly recommended, since calls to the GitHub REST API without an access token will have a much lower API rate limit. Some requests might also be unauthorized without an access token.

## Running from the command line
Use <code> python main.py</code> to run the program. A minimal working example is:
~~~ 
python main.py -owner fesh0r -repo fernflower
~~~
### Extra options
The following options can be used to configure the result obtained:
~~~ 
python main.py --a -owner <owner> -repo <repo> --n <int> --num_pairs <int>
~~~
* <code>-owner </code>: owner of the repository *[required]*
* <code>-repo </code>: name of the repository *[required]*
* <code>--a </code>: flag, when active will display extra information about the repository
* <code>--n </code>: number of commits to fetch. By default it fetches the 50 latest commits.
*  <code>--num_pairs </code>: number of contributor pairs that will be displayed. By default it display the top 3 pairs. 

Running <code> python main.py --help</code> will also display this information in the terminal.