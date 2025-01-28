import sqlite3
import requests
from bs4 import BeautifulSoup

def debug_print(message, verbose=True):
    if verbose:
        print(f"[DEBUG] {message}")

def test_connection(url):
    try:
        debug_print("Testing network connection...")
        response = requests.get("https://www.google.com", timeout=10)
        debug_print("Network connection OK")
        
        debug_print(f"Testing connection to {url}...")
        test_res = requests.get(url, timeout=10)
        test_res.raise_for_status()
        debug_print("Website connection OK")
        return True
    except Exception as e:
        print(f"\nCONNECTION FAILED: {str(e)}")
        print("Possible issues:")
        print("- No internet connection")
        print("- Invalid URL")
        print("- Website blocking requests")
        print("- SSL certificate issues (try http:// instead of https://)")
        return False

def run_scraper():
    print("""\
╔════════════════════════════╗
║    Web Scraper Assistant   ║
╚════════════════════════════╝""")
    
    url = input("Enter website URL: ").strip()
    
    if not test_connection(url):
        input("\nPress Enter to exit...")
        return

    try:
        print("\nStep 1: Verify page structure")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Page title: {soup.title.string if soup.title else 'None found'}")

        print("\nStep 2: Define scraping targets")
        fields = {}
        while True:
            field = input("Enter field name (or press Enter to finish): ").strip()
            if not field:
                break
            selector = input(f"CSS selector for {field}: ").strip()
            elements = soup.select(selector)
            print(f"Found {len(elements)} matches")
            fields[field] = selector

        if not fields:
            print("No fields defined!")
            input("\nPress Enter to exit...")
            return

        print("\nStep 3: Database setup")
        db_name = input("Database filename (default: data.db): ").strip() or "data.db"
        
        print("\nStep 4: Verification")
        print("Testing scraping...")
        test_data = {"url": url}
        for field, selector in fields.items():
            element = soup.select_one(selector)
            test_data[field] = element.get_text(strip=True) if element else "NULL"
            print(f"{field}: {test_data[field]}")

        confirm = input("\nDoes this look correct? (y/n): ").lower()
        if confirm != 'y':
            print("Aborting...")
            input("\nPress Enter to exit...")
            return

        print("\nStep 5: Saving data...")
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        # Create table
        columns = ["url TEXT"] + [f"{field} TEXT" for field in fields.keys()]
        c.execute(f"CREATE TABLE IF NOT EXISTS scraped_data ({', '.join(columns)})")
        
        # Insert data
        c.execute(f"INSERT INTO scraped_data VALUES ({', '.join(['?']*len(test_data))})",
                tuple(test_data.values()))
        
        conn.commit()
        conn.close()

        print("\nSUCCESS! Data saved to database")
        print(f"Database location: {db_name}")
        print("You can view the data using DB Browser for SQLite")

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("Common solutions:")
        print("1. Try different CSS selectors")
        print("2. Check website permissions (robots.txt)")
        print("3. Use http:// instead of https://")
        print("4. Try a different database name")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    run_scraper()