from scraper import scrape_all
from reporter import generate_report, load_config as load_reporter_config
from gdocs_exporter import export_to_google_docs, load_config as load_gdocs_config
from datetime import datetime
import database_manager # Import the database manager
import yaml # For loading the main config to check db settings

def load_main_config(filepath="config.yaml"):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    print(f"Starting Market Insights Radar process on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")

    # 1. Load Configurations
    main_config = load_main_config() # Load the main config
    reporter_config = main_config # reporter.py now loads its own, but main_config is useful here
    gdocs_config = main_config # gdocs_exporter.py also loads its own

    # 1a. Initialize Database (if enabled)
    db_config = main_config.get('database', {})
    if db_config.get('enabled', False):
        db_filename = db_config.get('filename', 'market_news.db')
        print(f"Database feature is enabled. Ensuring table exists in '{db_filename}'...")
        database_manager.create_news_table_if_not_exists(db_filename)
    else:
        print("Database feature is disabled in config.yaml.")

    # 2. Scrape Data
    print("Scraping websites...")
    scraped_data = scrape_all() # scrape_all already uses config.yaml for max_items

    if scraped_data:
        print(f"Scraping complete. Collected data from {len(scraped_data)} sources.")

        # 3. Generate Report (reporter.py now handles DB interaction)
        api_key = reporter_config.get('gemini_api_key')
        # The generate_report function in reporter.py will now handle
        # checking the database and filtering articles before calling Gemini.
        print("Generating report...")
        report_content = generate_report(scraped_data, api_key if api_key else "") # Pass empty string if no API key for now

        if report_content:
            print("Report content prepared.") # "Report generated successfully." might be misleading if it's just the prompt

            # 4. Export to Google Docs (if you re-enable this part)
            # This part is currently commented out in your provided main.py
            # If you uncomment it, ensure it uses the potentially filtered 'report_content'
            # credentials_file = gdocs_config.get('google_docs', {}).get('credentials_file')
            # document_name_format = gdocs_config.get('google_docs', {}).get('document_name')
            #
            # if credentials_file and api_key: # Also ensure API key was present for actual Gemini call
            #     print("Exporting report to Google Docs...")
            #     document_link = export_to_google_docs(report_content, credentials_file, document_name_format)
            #     if document_link:
            #         print(f"Report exported to Google Docs.")
            #     else:
            #         print("Failed to export report to Google Docs.")
            # elif not api_key:
            #     print("Gemini API key not found. Report not generated, so not exported.")
            # else:
            #     print("Google Docs credentials not found. Report not exported.")
        else:
            print("Report generation/preparation failed or no new articles to report.")
    else:
        print("No data scraped. Skipping report generation and export.")

    print("Market Insights Radar process finished.")