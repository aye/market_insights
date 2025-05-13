import google.generativeai as genai
import yaml
from datetime import datetime
import database_manager # Import the new database manager

def load_config(filepath="config.yaml"):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def generate_report(scraped_data, api_key):
    # genai.configure(api_key=api_key) # Assuming you'll re-enable Gemini later
    # model = genai.GenerativeModel('gemini-pro')

    config = load_config()
    db_config = config.get('database', {})
    db_enabled = db_config.get('enabled', False)
    db_filename = db_config.get('filename', 'market_news.db')

    if not scraped_data:
        return "No market insights data was scraped this week."

    articles_for_report = []
    new_articles_count = 0
    existing_articles_count = 0

    for item in scraped_data:
        headline = item.get('headline')
        copy_text = item.get('copy') # Renamed to avoid conflict with 'copy' module
        link = item.get('link')
        name = item.get('name')

        if not link: # Skip items without a link as it's used as a unique identifier
            print(f"Skipping item, no link: {headline[:50]}...")
            continue

        if db_enabled:
            # Check if article is already in DB
            if database_manager.is_news_article_present(db_filename, link):
                print(f"Duplicate found (already in DB): {headline[:50]}... ({link})")
                existing_articles_count += 1
                # Decide if you want to skip it or include it with a note for Gemini
                # For now, we'll skip duplicates from the report to Gemini
                continue
            else:
                # If not present, add it to the DB
                added = database_manager.add_news_article(db_filename, name, headline, link, copy_text)
                if added:
                    new_articles_count += 1
                articles_for_report.append(item) # Add to report list only if new or DB disabled
        else:
            articles_for_report.append(item) # If DB is not enabled, process all items

    if db_enabled:
        print(f"Database check complete: {new_articles_count} new articles added, {existing_articles_count} existing articles found.")

    if not articles_for_report:
        return "No new market insights data to report this week (all items were duplicates or skipped)."


    prompt = """
"You will be provided with a collection of news items. Each item includes a 'Source', 'Headline', 'Copy' (which typically contains a publication date/time and sometimes a brief description or sub-headline), and a 'Link URL'.

Please perform an analysis of this news and generate a comprehensive report in English. The report should be structured and sorted by 'News Source'.

For each unique news source, please provide:

News Source Name: [Name of the source]
General Overview & Key Themes for this Source:
Provide a brief (2-4 sentence) summary in English of the main topics, recurring themes, types of announcements (e.g., events, research, partnerships, student life, program updates, awards), or general focus observed in the news items from this specific source. Translate any German content from headlines or copy to inform this overview.
Detailed News Items (Chronologically if possible, otherwise as listed): For each news item from this source, list the following:
a. Headline (Translated to English): Provide an English translation of the original headline.
b. Summary of Content (Translated to English): Briefly summarize the essence of the news item in English, drawing from the 'Copy' field (especially any descriptive text beyond just the timestamp) and the headline. If the 'Copy' field is just a timestamp, use the headline to infer the content.
c. Publication Information: State the date and time as provided in the 'Copy' field.
d. Link URL: Provide the full Link URL.
Ensure the entire report is in English. Pay attention to accurate translation of headlines and any descriptive text within the 'Copy' field. The final output should be well-organized and easy to read."
Here is the data:

"""
    for item in articles_for_report: # Use the filtered list
        headline = item.get('headline')
        copy_text = item.get('copy')
        link = item.get('link')
        name = item.get('name')

        if name:
            prompt += f"Source: {name}\n"
        if headline:
            prompt += f"Headline: {headline}\n"
        if copy_text: # Use the renamed variable
            prompt += f"Copy: {copy_text}\n"
        if link:
            prompt += f"Link URL: {link}\n"
        prompt += "\n"

    prompt += "\n\nDo not include any introductory or concluding remarks. Respond ONLY with the market insights radar report in the specified format."

    print("--- PROMPT FOR GEMINI ---")
    print(prompt)
    print("--- END OF PROMPT ---")


    # try:
    # response = model.generate_content(prompt)
    # return response.text
    # except Exception as e:
    # print(f"Error generating report with Gemini: {e}")
    # return None
    print("Mocking Gemini response for now. Returning the generated prompt.")
    return f"Report based on {len(articles_for_report)} articles would be generated here. \nDB Status: Enabled={db_enabled}, New={new_articles_count}, Existing={existing_articles_count}"


if __name__ == '__main__':
    mock_scraped_data = [
        {'name': 'Tech News', 'headline': 'Old Tech Stock Surge', 'copy': 'Shares of major tech companies saw significant gains... 2023-01-01', 'link': 'http://example.com/news/old-tech-surge'},
        {'name': 'AI Weekly', 'headline': 'AI Adoption Still Rising', 'copy': 'Increased investment in AI startups... 2023-01-05', 'link': 'http://example.com/news/ai-trends-old'},
        {'name': 'Product Hunt', 'headline': 'New Product Launched Last Year', 'copy': 'A company released an innovative product... 2023-01-10', 'link': 'http://example.com/news/product-launch-old'},
        {'name': 'Tech News', 'headline': 'Fresh Tech Innovations', 'copy': 'Latest breakthroughs announced today. 2024-05-10', 'link': 'http://example.com/news/fresh-tech'},
        {'name': 'AI Weekly', 'headline': 'New AI Model Released', 'copy': 'A new AI model promises revolution. 2024-05-09', 'link': 'http://example.com/news/new-ai-model'}
    ]
    config = load_config()
    db_conf = config.get('database', {})
    if db_conf.get('enabled', False):
        database_manager.create_news_table_if_not_exists(db_conf.get('filename')) # Ensure table exists

    api_key = config.get('gemini_api_key') # This will be None if not set
    report = generate_report(mock_scraped_data, api_key)
    if report:
        print("\n--- Generated Report ---")
        print(report)
    else:
        print("Report generation failed.")