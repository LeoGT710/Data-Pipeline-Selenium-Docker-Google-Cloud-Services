# Comprehensive Data Pipeline Implementation Overview

This project automates data extraction, processing, and analysis using Python, Selenium, Docker, and Google Cloud Services. It streamlines data collection from various sources, transforms and loads data into Google BigQuery, and generates interactive dashboards for business insights.

## Structure

- **PART 1 _ Web Scraping & Data Processing**: Utilizes Selenium to extract data from diverse websites.
- **PART 2 _ Docker**: Builds robust Docker images for encapsulating the web scraping and data processing environments, ensuring consistency and portability.
- **PART 3 _ Automation**: Deploys Docker images to Google Cloud Artifact Registry and automates data updates using Google Cloud Scheduler for continuous, hands-free execution.
- **PART 4 _ Data Analysis**: Transforms raw data into actionable insights by creating dynamic, interactive dashboards in Looker and Google Sheets, driving business decision-making.

## Technical Details

- **Programming Languages**: Python
- **Libraries**: Selenium, pandas, Google Cloud Client Library
- **Services**: Docker, Google Cloud Run, Cloud Scheduler, BigQuery, Looker

## Scripts

- **`ipos_sales()`**: Extracts sales data from IPoS website.
- **`ipos_thuchi()`**: Extracts cash-in/cash-out data from IPoS website.
- **`ipos_ketca()`**: Extracts shift report data from IPoS website.

## Usage

1. Set up Google Cloud Services and install required libraries.
2. Configure Selenium WebDriver options.
3. Run scripts to extract, process, and analyze data.
4. Clean and build Docker images after developing web scraping tasks.
5. Deploy Docker images to Google Cloud Services.
6. Schedule tasks using Cloud Scheduler.

## Benefits

- Automates data collection and processing.
- Enhances data accessibility and analysis.
- Supports data-driven decision-making.

## Future Development

- Expand data sources and scraping capabilities.
- Enhance data transformation and loading processes.
- Develop additional dashboards and reports.

