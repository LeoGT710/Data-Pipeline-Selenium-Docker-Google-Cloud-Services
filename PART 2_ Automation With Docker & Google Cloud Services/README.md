```markdown
# Selenium Web Scraping Docker Setup

This project containerizes a Selenium-based web scraping application using a standalone Chrome Docker image.
The container includes Python, necessary libraries, and dependencies for running the scraping task in a secure,
isolated environment.

## Table of Contents
- [Base Image](#base-image)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Custom Python Environment](#custom-python-environment)
- [Environment Setup](#environment-setup)
- [Running the Container](#running-the-container)

## Base Image

The project uses the official Selenium standalone Chrome image:

```dockerfile
FROM selenium/standalone-chrome:4.20.0-20240425
```

This ensures compatibility between Selenium and the Chrome browser.

## Features
- **Selenium with Chrome**: The container is pre-configured with a Chrome browser, ready to be used with Selenium.
- **Python Virtual Environment**: The container uses a Python virtual environment for installing and managing dependencies.
- **Customizable**: Easily add your own scraping scripts and dependencies.

## Installation

1. **Clone this repository** to your local machine.
2. **Build the Docker image** using the `Dockerfile` provided.

```bash
docker build -t selenium-scraping:latest .
```

3. Ensure all necessary files (like `Key_1.json`, `cookies.txt`, and `requirements.txt`) are included in the `/app/` directory before building.

## Usage

1. **Run the Docker container** after building the image:

```bash
docker run -it --rm selenium-scraping:latest
```

This command starts the container and runs the `scraping_docker.py` script.

## File Structure

```bash
/app
 ├── scraping_docker.py     # Python script to be executed inside the container
 ├── requirements.txt       # Python package dependencies
 ├── Key_1.json             # Google Cloud service account credentials
 ├── cookies.txt            # Cookies file for web scraping session
 ├── Temp_saved_file/       # Directory for saving temporary files
```

## Custom Python Environment

The container creates a virtual environment for Python, ensuring that all dependencies are isolated and managed within the container. The `requirements.txt` file is used to install necessary packages.

### Create and Activate Virtual Environment

```bash
# Create virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment and install dependencies
RUN /app/venv/bin/pip install -r /app/requirements.txt
```

## Environment Setup

### Installed Packages

The container installs various system-level dependencies for running Chrome and handling web scraping efficiently. This includes libraries such as:

- `libnspr4`
- `libnss3`
- `libgdk-pixbuf2.0-0`
- `libxcomposite1`, etc.

These libraries are critical for running Chrome in headless mode inside the container.

### Python Dependencies

The required Python packages are listed in the `requirements.txt` file and installed into the virtual environment.

## Running the Container

Once the container is up and running, it will automatically execute the `scraping_docker.py` script using:

```dockerfile
CMD ["python3", "scraping_docker.py"]
```

You can modify the Python script or pass additional parameters by changing the `CMD` line in the `Dockerfile` or overriding it when running the container.
```

## Credits
- **Selenium**: For automating the Chrome browser.
- **Docker**: For containerizing the application.
- **Python**: For managing the scraping tasks and data processing.
```
