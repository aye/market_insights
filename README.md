### Install Libraries:
```
pip install requests beautifulsoup4 PyYAML google-generativeai google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
Configure your config.yaml:

Add the URLs and CSS selectors for the websites you want to scrape.
Enter your Gemini API key. You can obtain one from the Google AI Studio.
Provide the path to your Google Cloud service account credentials JSON file.
Optionally, customize the document_name format for your Google Docs.

Here is an example:

```
sources:
  - name: "Publikation A"
    url: "https://www.example.com/index"
    schema:
      headline:
        selector: ".teaser__title"
        extract_href: False
      copy:
        selector: ".teaser__summary"
        extract_href: False
      link:
        selector: ".teaser__link"
        attribute: "href" 
gemini_api_key: "YOUR_GEMINI_API_KEY"
google_docs:
  credentials_file: "path/to/your/credentials.json"
  document_name: "Weekly Market Insights Radar - {date}" # {date} will be replaced
```

### Set Up Google Cloud and Google Docs API:
 
* Create a Google Cloud Project.
* Enable the Google Docs API.
* Create a service account and download the JSON key file. Make sure this file's path is correctly specified in config.yaml.
* Share a Google Docs document (if you want to update an existing one, though the current code creates a new one each week) with the service account's email address.


### Run the Tool:
You can run the tool manually by executing the main.py script:
```
python main.py
```
Schedule Weekly Execution. Linux/macOS (Cron): Open your crontab (crontab -e) and add a line like:
```

Code snippet

0 6 * * FRI python /path/to/your/market_radar/main.py
```

This will run the script every Friday at 6:00 AM. Adjust the path and time as needed.
Windows (Task Scheduler): Search for "Task Scheduler" in the Start Menu and create a basic task to run the main.py script weekly.

