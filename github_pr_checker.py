import http.client
import json
import os
import sys
from datetime import datetime

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
REPOS = {
    "fcq": [
        "Flutter-Global/fcq-service",
        "Flutter-Global/fcq-chef-ppb",
        "Flutter-Global/fcq-configrepo-i2-ppb",
        "Flutter-Global/fcq-configrepo-i2-pp",
        "Flutter-Global/fcq-configrepo-i2-sbg",    
    ],
    "psa": [
        "Flutter-Global/psa-service",
        "Flutter-Global/psa-chef-ppb",
        "Flutter-Global/psa-configrepo-i2-ppb",
        "Flutter-Global/psa-configrepo-i2-pp",
        "Flutter-Global/psa-configrepo-i2-sbg",
    ],
    "sco": [
        "Flutter-Global/sco-service",
        "Flutter-Global/sco-chef-ppb",
        "Flutter-Global/sco-configrepo-i2-ppb",
        "Flutter-Global/sco-configrepo-i2-pp",
        "Flutter-Global/sco-configrepo-i2-sbg",
    ],
    "wlp": [
        "Flutter-Global/wlp-service",
        "Flutter-Global/wlp-chef-ppb",
        "Flutter-Global/wlp-configrepo-i2-ppb",
        "Flutter-Global/wlp-configrepo-i2-pp",
        "Flutter-Global/wlp-configrepo-i2-sbg",
    ],
    "foe": [
        "Flutter-Global/foe-service",
        "Flutter-Global/foe-configrepo-i2-bf",
        "Flutter-Global/foe-configrepo-i2-pp",
        "Flutter-Global/foe-configrepo-i2-sbg",
        "Flutter-Global/foe-ansible-ppb",
    ],
    "bme": [
        "Flutter-Global/bme-service",
        "Flutter-Global/bme-chef-uki",
        "Flutter-Global/bme-configrepo-i2-sbg",
    ],
}

def format_pr_with_link(repo, pr):
    base_url = "https://github.com"
    link = f"{base_url}/{repo}/pull/{pr['number']}"
    created_date = datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
    
    output = []
    output.append(f"\n  - PR #{pr['number']}: {pr['title']}")
    output.append(f"    Author: {pr['user']['login']}")
    output.append(f"    Opened: {created_date}")
    output.append(f"    Link: {link}")
    
    return "\n".join(output)

def isPREligible(pr):
    return "dependabot" not in pr['user']['login']

def print_repo_header(repo):
    print("=" * len(repo))
    print(repo)
    print("=" * len(repo))

def check_open_prs(repo):
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
        print_repo_header(repo)
        if open_prs:
            for pr in open_prs:
                if isPREligible(pr):
                    print(format_pr_with_link(repo, pr))
        else:
            print("No open PRs")
    else:
        print(f"Failed to fetch PRs for {repo}: {response.status}")
    conn.close()

repo = sys.argv[1] if len(sys.argv) > 1 else None
if repo == "all":
    for category, repos in REPOS.items():
        print(f"\n{'#' * 50}")
        print(f"# {category.upper()}")
        print(f"{'#' * 50}\n")
        for r in repos:
            check_open_prs(r)
            print()
elif repo:
    for r in REPOS[repo]:
        check_open_prs(r)
else:
    print("You need to specify a repo to check. E.g. python github_pr_checker.py fcq")
    print("Or use 'all' to check all repos: python github_pr_checker.py all")
