import requests
from bs4 import BeautifulSoup
import yaml

def load_config(filepath="config.yaml"):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def scrape_website(source, max_items_to_scrape):
    url = source['url']
    schema = source.get('schema', {})
    name = source.get('name', 'Unknown Source')
    print(f"Scraping: {name} from {url}")
    scraped_items = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Determine the number of items to extract.
        # We'll naively assume the length of the first found element list.
        # A more robust approach might be needed depending on the site structure.
        num_items = None
        first_selector = next(iter(schema.values()), None)
        if first_selector and first_selector['selector']:
            first_elements = soup.select(first_selector['selector'])
            num_items = len(first_elements) if first_elements else 0

        if num_items is None:
            print(f"Warning: Could not determine the number of items on {url}. Skipping.")
            return []

        for i in range(min(num_items, max_items_to_scrape)):
            item_data = {}
            for field, config in schema.items():
                selector = config.get('selector')
                attribute = config.get('attribute')
                extract_href_flag = config.get('extract_href', False)
                add_domain = config.get('add_domain')

                if selector:
                    elements = soup.select(selector)
                    if elements and i < len(elements):
                        element = elements[i]
                        if attribute:
                            item_data[field] = add_domain + element.get(attribute)
                        else:
                            item_data[field] = element.get_text(separator=" ", strip=True)
                            if extract_href_flag:
                                item_data[f"{field}_href"] = element.get('href')
                    else:
                        item_data[field] = None
                        if extract_href_flag:
                            item_data[f"{field}_href"] = None
                else:
                    item_data[field] = None

            item_data["name"]=name
            scraped_items.append(item_data)

        return scraped_items
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return []

def scrape_all(config_file="config.yaml"):
    config = load_config(config_file)
    all_scraped_data = []
    max_items_to_scrape = 100
    if 'max_items_to_scrape' in config:
        max_items_to_scrape = config['max_items_to_scrape']

    if 'sources' in config:
        for source in config['sources']:
            data = scrape_website(source, max_items_to_scrape)
            if data:
                all_scraped_data.extend(data) # Extend the list as scrape_website now returns a list
    return all_scraped_data

if __name__ == '__main__':
    scraped_data = scrape_all()
    for item in scraped_data:
        print("\n--- Item ---")
        for key, value in item.items():
            print(f"  {key}: {value}")