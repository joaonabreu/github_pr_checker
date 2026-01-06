# GitHub Open Pull Requests Checker

This script checks for open PRs in specified GitHub repositories and lists them in the console. It fetches the data using GitHub's API and displays each PR's title, author, and a link.

## Requirements

- Python 3.x.
- A GitHub personal access token with `repo` scope for accessing private repositories.

## Setup

1. **Create a GitHub Personal Access Token**:
   - Go to [GitHub Developer Settings](https://github.com/settings/tokens) > **Personal access tokens** > **Tokens (classic)** > **Generate new token**.
   - Name the token and set its expiration date.
   - Check the `repo` scope to ensure access to private repositories.
   - Click **Generate token** and copy the token.

2. **Create a `.env` File**:
   - In the project directory, create a file named `.env`.
   - Paste the token into this file in the following format:
     ```plaintext
     GITHUB_TOKEN=your_personal_access_token
     ```

3. **Specify Your Repositories**:
   - In the script (`github_pr_checker.py`), add your repositories in the `REPOS` list using the format `"org/service_name"`:
     ```python
     REPOS = {
        "abc": [
            "org/abc-service",
            "org/abc-chef-ppb",
            "org/abc-configrepo-i2-ppb",
            "org/abc-configrepo-i2-pp",
            "org/abc-configrepo-i2-sbg",    
        ],
        "def": [
            "org/def-service",
            "org/def-chef-ppb",
            "org/def-configrepo-i2-ppb",
            "org/def-configrepo-i2-pp",
            "org/def-configrepo-i2-sbg",
        ],
     }
     ```

## Usage

1. **Run the Script**:
   - Run the script with Python:
     ```bash
     python3 github_pr_checker.py service_name
     ```
    - e.g.
        ```bash
        python3 github_pr_checker.py abc
        ```
   - To check all repositories at once:
        ```bash
        python3 github_pr_checker.py all
        ```

2. **Output**:
   - The script will print open PRs for each repository in a visually distinct format, with a title, author, and link for each PR.

## Example Output

```
==========================
org/abc-service
==========================
- Flutter-Global/abc-service#23: Fix bug in login by [user123]
- Flutter-Global/abc-service#45: Add new feature by user456 [user456]
===========================
Flutter-Global/abc-chef-ppb
===========================
- Flutter-Global/abc-chef-ppb#1: Fix bug by [user123]
====================================
Flutter-Global/abc-configrepo-i2-ppb
====================================
- Flutter-Global/abc-configrepo-i2-ppb#1: Fix bug in login by [user123]
===================================
Flutter-Global/abc-configrepo-i2-pp
===================================
No open PRs
====================================
Flutter-Global/abc-configrepo-i2-sbg
====================================
No open PRs
```

## Notes

- Ensure your token has permission to access each repository listed.
- Make sure the `.env` file is in the same directory as the script to allow it to load the token correctly.

## Make the Script Globally Accessible

To make the script accessible from any directory using an alias:

1. **Edit your Shell Configuration File**:
   - Open your shell's configuration file (e.g., `.bashrc` or `.zshrc`) in a text editor:
     ```bash
     nano ~/.bashrc  # For Bash
     # or
     nano ~/.zshrc   # For Zsh
     ```

2. **Add the Alias**:
   - Add the following line to create an alias for the script:
     ```bash
     alias check_prs="python3 /path/to/github_pr_checker.py"
     ```
   - Replace `/path/to/github_pr_checker.py` with the full path to the script file.

3. **Reload the Configuration**:
   - After saving the file, reload the shell configuration:
     ```bash
     source ~/.bashrc  # For Bash
     # or
     source ~/.zshrc   # For Zsh
     ```

4. **Run the Script Using the Alias**:
   - Now, you can run the script from any directory by typing:
     ```bash
     check_prs
     ``` 

This setup enables you to use `github_pr_checker` from any location without needing to change directories.

## Troubleshooting

- **401 Unauthorized**: This error means the token is incorrect or doesn't have the correct permissions.
- **403 Forbidden**: You may be hitting the API rate limit or the token does not have the necessary permissions.
- **FileNotFoundError for `.env`**: Ensure the `.env` file exists and is correctly formatted.
