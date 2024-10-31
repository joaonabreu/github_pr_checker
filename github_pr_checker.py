import http.client
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
def load_dotenv():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPOS = ["org/repo1", "org/repo2"]


def print_repo_header(repo):
    header = f" Open PRs for {repo} "
    print("=" * len(header))
    print(header)
    print("=" * len(header))

def check_open_prs(repo):
    print_repo_header(repo)
    conn = http.client.HTTPSConnection("api.github.com")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "PR-Checker"
    }
    url = f"/repos/{repo}/pulls?state=open"
    conn.request("GET", url, headers=headers)
    
    response = conn.getresponse()
    if response.status == 200:
        open_prs = json.loads(response.read().decode())
        if open_prs:
            for pr in open_prs:
                if "dependabot" not in pr['user']['login']:
                    print(f"- #{pr['number']}: {pr['title']} by {pr['user']['login']}")
                    print(f"  Link: {pr['html_url']}")
        else:
            print("No open PRs")
    else:
        print(f"Failed to fetch PRs for {repo}: {response.status}")
    conn.close()

for repo in REPOS:
    check_open_prs(repo)
