import subprocess
import os
import sys
import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter

# Store the original working directory
original_cwd = os.getcwd()

# Load configuration from config.json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: 'config.json' file not found.")
    sys.exit(1)

# Get the repository URL from config
repo_url = config.get('repo_url')
if not repo_url:
    print("Error: 'repo_url' not specified in config.json")
    sys.exit(1)
repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')

# Get the SSH key file path from config
ssh_key_file = config.get('ssh_key_file')
if not ssh_key_file:
    print("Error: 'ssh_key_file' not specified in config.json")
    sys.exit(1)
if not os.path.isfile(ssh_key_file):
    print(f"Error: SSH key file '{ssh_key_file}' does not exist.")
    sys.exit(1)

# Create 'repos' directory if it doesn't exist
repos_dir = os.path.join(original_cwd, 'repos')
if not os.path.exists(repos_dir):
    os.makedirs(repos_dir)

# Create 'graphs' directory if it doesn't exist
graphs_dir = os.path.join(original_cwd, 'graphs')
if not os.path.exists(graphs_dir):
    os.makedirs(graphs_dir)

# Default the output file name to the repo name if not specified
output_file = config.get('output_file')
if not output_file:
    output_file = f"{repo_name}.png"

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
        print("Error: Invalid GitHub URL format.")
        sys.exit(1)
elif repo_url.startswith('git@github.com:'):
    ssh_url = repo_url
else:
    print("Error: Unsupported GitHub URL format.")
    sys.exit(1)

# Check if the repository exists in the 'repos' directory
repo_path = os.path.join(repos_dir, repo_name)
git_folder = os.path.join(repo_path, '.git')

if not os.path.exists(repo_path) or not os.path.exists(git_folder):
    print("Cloning the repository into 'repos' directory...")
    env = os.environ.copy()
    env['GIT_SSH_COMMAND'] = f"ssh -i {ssh_key_file}"
    result = subprocess.run(['git', 'clone', ssh_url, repo_path], env=env)
    if result.returncode != 0:
        print("Error: Git clone failed. Please check your SSH key and repository URL.")
        sys.exit(1)
    os.chdir(repo_path)
else:
    print(f"Repository '{repo_name}' already exists in 'repos' directory and is a valid Git repository.")
    os.chdir(repo_path)

# Get the git log
try:
    log_output = subprocess.check_output(
        ['git', 'log', '--pretty=format:%ad', '--date=short']
    ).decode('utf-8')
except subprocess.CalledProcessError as e:
    print("Error executing git log:", e)
    sys.exit(1)

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

# Change back to the original working directory
os.chdir(original_cwd)

# Save the figure to the 'graphs' directory
output_path = os.path.join(graphs_dir, output_file)
plt.savefig(output_path)
print(f"Figure saved to {output_path}")

# Optionally, display the figure
plt.show()
