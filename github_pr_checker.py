import argparse
import http.client
import json
import os
from datetime import datetime

GITHUB_BASE_URL = "https://github.com"
_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')


def load_dotenv():
    with open(_ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
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


def format_pr(repo, pr):
    link = f"{GITHUB_BASE_URL}/{repo}/pull/{pr['number']}"
    created_date = datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
    labels = ", ".join(lbl['name'] for lbl in pr['labels']) or "none"
    return (
        f"\n  - PR #{pr['number']}: {pr['title']}\n"
        f"    Author: {pr['user']['login']}\n"
        f"    Opened: {created_date}\n"
        f"    Labels: {labels}\n"
        f"    Link: {link}"
    )


def has_label(pr, label):
    return any(lbl['name'].lower() == label.lower() for lbl in pr['labels'])


def is_pr_eligible(pr, label=None):
    if "dependabot" in pr['user']['login']:
        return False
    if label and not has_label(pr, label):
        return False
    return True


def print_repo_header(repo):
    sep = "=" * len(repo)
    print(f"{sep}\n{repo}\n{sep}")


def check_open_prs(repo, label=None):
    conn = http.client.HTTPSConnection("api.github.com")
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "PR-Checker"}
    conn.request("GET", f"/repos/{repo}/pulls?state=open", headers=headers)
    response = conn.getresponse()
    body = response.read()
    conn.close()

    print_repo_header(repo)
    if response.status != 200:
        print(f"Failed to fetch PRs for {repo}: {response.status}")
        return

    prs = [pr for pr in json.loads(body.decode()) if is_pr_eligible(pr, label)]
    if prs:
        for pr in prs:
            print(format_pr(repo, pr))
    else:
        print("No open PRs")


def main():
    parser = argparse.ArgumentParser(description="Check open GitHub PRs")
    parser.add_argument("repo", help=f"Repo group to check, or 'all'. Available: {', '.join(REPOS)}")
    parser.add_argument("-l", "--label", help="Filter PRs by label (e.g. 'major')", default=None)
    args = parser.parse_args()

    if args.repo == "all":
        for category, repos in REPOS.items():
            print(f"\n{'#' * 50}\n# {category.upper()}\n{'#' * 50}\n")
            for r in repos:
                check_open_prs(r, args.label)
                print()
    else:
        for r in REPOS[args.repo]:
            check_open_prs(r, args.label)


if __name__ == "__main__":
    main()
