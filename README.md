# GitHub Repository Commit Graph Generator

This project is a Python script that clones a GitHub repository, analyzes its commit history, and generates a graph showing the number of commits over time. The script uses SSH authentication with a specified SSH key file, reads input from a `config.json` file, and saves the generated graph as a PNG image in a designated `graphs` folder. Repositories are cloned into a `repos` folder.

## Features

- Clones GitHub repositories using SSH authenti… ```bash
pip install -r requirements.txt
```

- **Graph Not Generated**:

- Ensure that Matplotlib is installed.
- Check for any errors in the script output that might indicate issues during plotting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## Acknowledgments

- Inspired by the need to visualize commit histories for GitHub repositories.
- Utilizes the powerful Matplotlib library for data visualization.