import sqlite3
import yaml
from datetime import datetime

def load_db_config(filepath="config.yaml"):
    """Loads database configuration from the YAML file."""
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('database', {})

def get_db_connection(db_name="market_news.db"):
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row # Access columns by name
    return conn

def create_news_table_if_not_exists(db_name="market_news.db"):
    """Creates the 'news_articles' table if it doesn't already exist."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            headline TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL, -- Assuming link is unique for a news item
            copy TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized and 'news_articles' table ensured.")

def add_news_article(db_name, source, headline, link, copy):
    """Adds a new news article to the database. Returns True if added, False if it already exists (based on link)."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO news_articles (source, headline, link, copy, scraped_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (source, headline, link, copy, datetime.now()))
        conn.commit()
        print(f"Added to DB: {headline[:50]}... ({link})")
        return True
    except sqlite3.IntegrityError:
        # This error occurs if the link (due to UNIQUE constraint) already exists
        print(f"Already in DB (link exists): {headline[:50]}... ({link})")
        return False
    finally:
        conn.close()

def is_news_article_present(db_name, link):
    """Checks if a news article with the given link already exists in the database."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM news_articles WHERE link = ?", (link,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

if __name__ == '__main__':
    # Example Usage (for testing this module directly)
    db_config = load_db_config()
    if db_config.get('enabled', False):
        db_filename = db_config.get('filename', 'market_news.db')
        create_news_table_if_not_exists(db_filename)

        # Test adding a new article
        added1 = add_news_article(db_filename,
                                 "Test Source",
                                 "Test Headline: New Innovations in Tech",
                                 "http://example.com/news/tech-innovations",
                                 "Some copy about tech innovations. Published 2024-01-15")
        print(f"Article 1 added: {added1}")

        # Test adding the same article again (should be blocked by UNIQUE constraint on link)
        added2 = add_news_article(db_filename,
                                 "Test Source",
                                 "Test Headline: New Innovations in Tech", # Even if other fields change, link is key
                                 "http://example.com/news/tech-innovations",
                                 "Updated copy.")
        print(f"Article 2 added: {added2}")

        # Test checking presence
        present = is_news_article_present(db_filename, "http://example.com/news/tech-innovations")
        print(f"Article 'http://example.com/news/tech-innovations' present: {present}")

        present_fake = is_news_article_present(db_filename, "http://example.com/news/fake")
        print(f"Article 'http://example.com/news/fake' present: {present_fake}")
    else:
        print("Database feature is disabled in config.yaml")