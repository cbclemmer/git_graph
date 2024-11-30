import subprocess
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import sys

# Get the repository URL
repo_url = input("Enter the GitHub repository SSH or HTTPS URL: ")
repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')

# Get the SSH key file path
ssh_key_file = input("Enter the path to your SSH key file: ")

# Verify SSH key file exists
if not os.path.isfile(ssh_key_file):
    print(f"SSH key file '{ssh_key_file}' does not exist.")
    sys.exit(1)

# Convert HTTPS URL to SSH URL if necessary
if repo_url.startswith('https://github.com/'):
    # Extract the user and repository name
    parts = repo_url.rstrip('/').split('/')
    if len(parts) >= 5:
        user = parts[3]
        repo = parts[4].replace('.git', '')
        ssh_url = f'git@github.com:{user}/{repo}.git'
        print(f"Converting HTTPS URL to SSH URL: {ssh_url}")
    else:
        print("Invalid GitHub URL format.")
        sys.exit(1)
elif repo_url.startswith('git@github.com:'):
    ssh_url = repo_url
else:
    print("Unsupported GitHub URL format.")
    sys.exit(1)

# Clone the repository if not already cloned
if not os.path.exists(repo_name):
    env = os.environ.copy()
    env['GIT_SSH_COMMAND'] = f"ssh -i {ssh_key_file}"
    result = subprocess.run(['git', 'clone', ssh_url], env=env)
    if result.returncode != 0:
        print("Git clone failed. Please check your SSH key and repository URL.")
        sys.exit(1)
else:
    print(f"Repository '{repo_name}' already exists.")

# Change directory to the repository
os.chdir(repo_name)

# Get the git log
log_output = subprocess.check_output(
    ['git', 'log', '--pretty=format:%ad', '--date=short']
).decode('utf-8')

# Split the output into lines
commit_dates = log_output.strip().split('\n')

# Number of commits
num_commits = len(commit_dates)
print(f"Number of commits: {num_commits}")

# Parse dates
commit_dates = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in commit_dates]

# Get months (set day=1)
months = [date.replace(day=1) for date in commit_dates]

# Count commits per month
commit_counts = Counter(months)

# Sort the months
sorted_months = sorted(commit_counts)

# Get counts
counts = [commit_counts[month] for month in sorted_months]

# Plot the graph
plt.figure(figsize=(12, 6))
plt.plot(sorted_months, counts, marker='o')
plt.title('Commits Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Commits')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
