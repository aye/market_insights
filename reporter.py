import google.generativeai as genai
import yaml
from datetime import datetime

def load_config(filepath="config.yaml"):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def generate_report(scraped_data, api_key):
#    genai.configure(api_key=api_key)
#    model = genai.GenerativeModel('gemini-pro')

    if not scraped_data:
        return "No market insights data was scraped this week."

    prompt = """You are a market research analyst. Analyze the following news headlines and associated information about to the name of the Source. Generate a concise market insights radar report in English. The report MUST:

Be structured into two main sections:
Key Focuses and Developments of the source (This section should summarize the main activities and initiatives of the subject based on the provided data.)
Key Takeaways for Market Observers: (This section should provide insights for someone monitoring the higher education market, based on sources activities.)
Use bullet points within each section to list specific details. Not more then 3 points per section.
Focus on trends, developments, and implications.
Be concise and professional.
Here is the data:

"""
    for item in scraped_data:
        headline = item.get('headline')
        copy = item.get('copy')
        link = item.get('link')
        name = item.get('name')

        if name:
            prompt += f"Source: {name}\n"
        if headline:
            prompt += f"Headline: {headline}\n"
        if copy:
            prompt += f"Copy: {copy}\n"
        if link:
            prompt += f"Link URL: {link}\n"
        prompt += "\n"

    prompt += "\n\nDo not include any introductory or concluding remarks. Respond ONLY with the market insights radar report in the specified format."

    print(prompt)

#    try:
#        response = model.generate_content(prompt)
#        return response.text
#    except Exception as e:
#        print(f"Error generating report with Gemini: {e}")
#        return None

if __name__ == '__main__':
    # Mock scraped data for testing with the new structure
    mock_scraped_data = [
        {'headline': 'Tech Stock Surge', 'copy': 'Shares of major tech companies saw significant gains...', 'link': 'example.com/tech-surge'},
        {'headline': 'AI Adoption Rising', 'copy': 'Increased investment in AI startups...', 'link': 'example.com/ai-trends'},
        {'headline': 'New Product Launched', 'copy': 'A company released an innovative product...', 'link': None}
    ]
    config = load_config()
    api_key = config.get('gemini_api_key')
    if api_key:
        report = generate_report(mock_scraped_data, api_key)
        if report:
            print(report)
        else:
            print("Report generation failed.")
    else:
        print("Gemini API key not found in config.")