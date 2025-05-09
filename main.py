from scraper import scrape_all
from reporter import generate_report, load_config as load_reporter_config
from gdocs_exporter import export_to_google_docs, load_config as load_gdocs_config
from datetime import datetime

if __name__ == "__main__":
    print(f"Starting Market Insights Radar process on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")

    # 1. Load Configurations
    reporter_config = load_reporter_config()
    gdocs_config = load_gdocs_config()

    # 2. Scrape Data
    print("Scraping websites...")
    scraped_data = scrape_all()

    if scraped_data:
        print(f"Scraping complete. Collected data from {len(scraped_data)} sources.")
        generate_report(scraped_data, "")
      #  generate_report(scraped_data, "")
         # 3. Generate Report using Gemini
#         api_key = reporter_config.get('gemini_api_key')
#         if api_key:
#             print("Generating report with Gemini...")
#             report_content = generate_report(scraped_data, api_key)
#             if report_content:
#                 print("Report generated successfully.")
#
#                 # 4. Export to Google Docs
#                 credentials_file = gdocs_config.get('google_docs', {}).get('credentials_file')
#                 document_name_format = gdocs_config.get('google_docs', {}).get('document_name')
#
#                 if credentials_file:
#                     print("Exporting report to Google Docs...")
#                     document_link = export_to_google_docs(report_content, credentials_file, document_name_format)
#                     if document_link:
#                         print(f"Report exported to Google Docs.")
#                     else:
#                         print("Failed to export report to Google Docs.")
#                 else:
#                     print("Google Docs credentials not found. Report not exported.")
#             else:
#                 print("Report generation failed.")
#         else:
#             print("Gemini API key not found. Cannot generate report.")
    else:
        print("No data scraped. Skipping report generation and export.")

    print("Market Insights Radar process finished.")