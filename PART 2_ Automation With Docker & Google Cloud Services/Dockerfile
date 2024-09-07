# Use the official Selenium standalone Chrome image
FROM selenium/standalone-chrome:4.20.0-20240425

# Set working directory in the container
WORKDIR /app

# Create a directory for temporary files
RUN mkdir -p /app/Temp_saved_file

# Copy the Python script and other necessary files into the container
COPY scraping_docker.py /app/
COPY requirements.txt /app/
COPY Key_1.json /app/
COPY cookies.txt /app/


# List the contents of /app to verify files are copied
RUN ls -l /app/

# Install Python and other necessary tools
USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment and install Python packages
RUN /app/venv/bin/pip install -r /app/requirements.txt

# Switch back to the default Selenium user
USER seluser

# Set the environment variable to use the virtual environment's Python
ENV PATH="/app/venv/bin:$PATH"

# Run the Python script
CMD ["python3", "scraping_docker.py"]
