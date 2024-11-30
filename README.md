# GitHub Repository Commit Graph Generator

This project is a Python script that clones a GitHub repository, analyzes its commit history, and generates a graph showing the number of commits over time. The script uses SSH authentication with a specified SSH key file, reads input from a `config.json` file, and saves the generated graph as a PNG image in a designated `graphs` folder. Repositories are cloned into a `repos` folder.

## Features

- Clones GitHub repositories using SSH authentication with a specified SSH key file.
- Reads repository URL and SSH key file path from a `config.json` file.
- Saves cloned repositories in a `repos` directory.
- Analyzes the commit history and counts commits per month.
- Generates a commit graph and saves it as a PNG image in a `graphs` directory.
- Defaults the graph filename to the repository name if not specified.
- Creates `repos` and `graphs` directories if they do not exist.

## Prerequisites

- **Python 3.x**
- **Git**
- **Matplotlib** Python library

  Install Matplotlib using:

  ```bash
  pip install matplotlib
  ```

## Installation

1. **Clone the Project Repository**

   Clone this project to your local machine:

   ```bash
   git clone https://github.com/your_username/commit-graph-generator.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd commit-graph-generator
   ```

3. **Install Required Python Packages**

   Install the `matplotlib` library if you haven't already:

   ```bash
   pip install matplotlib
   ```

## Configuration

Create a `config.json` file in the project root directory with the following structure:

```json
{
  "repo_url": "git@github.com:username/repository.git",
  "ssh_key_file": "/path/to/your/private_key"
}
```

- **`repo_url`**: The SSH or HTTPS URL of the GitHub repository you want to clone and analyze.
- **`ssh_key_file`**: The full path to your private SSH key file used for authentication.

  - Ensure that the corresponding public key is added to your GitHub account under **Settings > SSH and GPG keys**.

**Example:**

```json
{
  "repo_url": "git@github.com:octocat/Hello-World.git",
  "ssh_key_file": "/home/user/.ssh/id_rsa"
}
```

## Usage

1. **Run the Script**

   Execute the script from the project directory:

   ```bash
   python commit_graph.py
   ```

2. **Script Output**

   - The script will clone the specified repository into the `repos` folder (if not already cloned).
   - It will analyze the commit history and generate a graph.
   - The graph image will be saved in the `graphs` folder, defaulting to `<repository_name>.png` if `output_file` is not specified in `config.json`.

3. **Viewing the Graph**

   - Navigate to the `graphs` folder to find the generated PNG image of the commit graph.
   - Open the image with your preferred image viewer.

## Project Structure

```
commit-graph-generator/
├── commit_graph.py
├── config.json
├── graphs/
└── repos/
```

- **`commit_graph.py`**: The main Python script that performs all operations.
- **`config.json`**: Configuration file containing repository URL and SSH key file path.
- **`graphs/`**: Directory where the generated graphs are saved.
- **`repos/`**: Directory where repositories are cloned.

## Notes

- **SSH Authentication**: The script uses SSH authentication with the specified SSH key file. Ensure your SSH key is correctly set up and associated with your GitHub account.

  - Test your SSH connection:

    ```bash
    ssh -i /path/to/your/private_key -T git@github.com
    ```

- **Dependencies**: Ensure all dependencies are installed and up to date.
- **Permissions**: The private SSH key file should have appropriate permissions (e.g., `chmod 600` on Unix-based systems).

## Customization

- **Adjusting the Time Granularity**: You can modify the script to change how commit dates are aggregated (e.g., by week or year) by adjusting the date processing logic.
- **Changing Graph Appearance**: Customize the graph by modifying the Matplotlib plotting parameters in `commit_graph.py`.
- **Specifying Output Filename**: To specify a custom output filename for the graph, add the `output_file` key in `config.json`:

  ```json
  {
    "repo_url": "git@github.com:username/repository.git",
    "ssh_key_file": "/path/to/your/private_key",
    "output_file": "custom_graph_name.png"
  }
  ```

## Troubleshooting

- **SSH Authentication Issues**:

  - If you encounter permission denied errors, verify your SSH key setup and its association with your GitHub account.
  - Ensure the SSH key file path in `config.json` is correct and points to your private key.

- **Repository Cloning Issues**:

  - Check for typos in the `repo_url` in `config.json`.
  - Ensure you have network access and the repository exists.

- **Dependencies Missing**:

  - If you receive import errors, ensure all required Python packages are installed.

    ```bash
    pip install -r requirements.txt
    ```

- **Graph Not Generated**:

  - Ensure that Matplotlib is installed.
  - Check for any errors in the script output that might indicate issues during plotting.
