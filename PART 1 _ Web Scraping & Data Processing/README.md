```markdown
# Web Scraping and Data Processing with Selenium and Google Cloud

## Overview

This project is a Python-based web scraping solution utilizing Selenium for automating browser interactions,
downloading data,and cleaning it for loading to Google Big Query data warehouse. It integrates with Google
Cloud services for logging and data storage, and it sends email notifications to provide status updates.

### Prerequisites
- Python 3.8+
- Google Cloud SDK installed and configured
- Chrome Browser installed
- ChromeDriver (automatically managed via WebDriver Manager)

### Python Libraries

Install the required Python libraries using:

```bash
pip install selenium webdriver-manager google-cloud-logging google-cloud-bigquery pandas openpyxl smtplib email
```
### Setup

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) and authenticate using a service account.
2. Add the Google Cloud service account key file (`Key_1.json`) to your working directory.
3. Ensure all necessary files (input reports) are available in the `/app/` directory.

## Project Structure

```bash
/app
 ├── accounting_sale_detail.xlsx    # Data file for sale details
 ├── Key_1.json                     # Google Cloud service account credentials
 ├── cash_in_cash_out_report.xlsx   # Cash-in cash-out report
 ├── list_shift_report.xlsx         # Shift report
 ├── Transaction_report_<date>.csv  # Momo transaction report
 ├── Transaction_Store_<date>.csv   # Grab transaction report
 ├── merchant_order_report_*.xlsx   # Merchant order report
```

## Features

- **Web Scraping with Selenium**: Automates logging into a website and downloading specific reports.
- **Headless Chrome**: Chrome runs in headless mode for efficient execution on cloud or local environments.
- **Data Processing**: Cleans and processes the downloaded Excel files by renaming columns and reformatting data.
- **Google Cloud Logging**: Logs errors and events to Google Cloud Logging for centralized monitoring.
- **Google BigQuery**: Processed data can be uploaded to BigQuery for storage and analysis.
- **Email Notifications**: Sends status emails using SMTP.

## Configuration

### Environment Variables

Set the following environment variables in your environment:

```bash
export TZ=Asia/Ho_Chi_Minh
export GOOGLE_APPLICATION_CREDENTIALS="/app/Key_1.json"
```

### Chrome Options

The script uses headless Chrome. Adjust the options if needed:

```python
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("user-agent=your-custom-user-agent")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
```

## Usage

### Running the Script

To start the web scraping and data processing, run the `main()` function, it will trigger `ipos_sales()`,`momo()`,`ipos_thuchi()`,`ipos_ketca()`, `grab()`,`spf()`,`send_email(log_messages)`:

```python
main()
```

This function will:
- Open the website and log in automatically.
- Download a report as an Excel file.
- Clean the downloaded data and process it into a pandas DataFrame.
- Log results and remove the file after processing.
- Load the data to Google Big Query warehouse
- send_email(log_messages) will log output to email when automating by Docker

## Credits

- **Selenium**: Web automation and scraping library.
- **Google Cloud SDK**: For logging and BigQuery integration.
- **Pandas**: For data processing and cleaning.
- **Smtplib**: For sending email notifications.
```
