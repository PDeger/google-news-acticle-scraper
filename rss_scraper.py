import feedparser
import urllib.parse
import pandas as pd
from datetime import datetime, timedelta
import time
from tqdm import tqdm
'''
Old query
 "General": "(Politik OR Bundestag OR Bundesregierung OR Gesetz OR Partei OR Ausland OR Krise OR Reform)",
    "Wirtschaft": "(Wirtschaft OR Unternehmen OR Aktien OR Inflation OR Dax OR Finanzen OR Markt OR Rezession OR Zinsen OR Banken)",
    "Technologie": "(Technologie OR KI OR Software OR Smartphone OR Innovation OR Gadget OR Digital OR Cyber OR Hardware)",
    "Gesundheit": "(Gesundheit OR Medizin OR Klinik OR Krankenhaus OR Patient OR RKI OR Pharmazie OR Impfung OR Aerzte)"
'''
CATEGORIES = {
    "General": "(Politik OR Bundestag OR Bundesregierung OR Gesetz OR Partei OR Scholz OR AfD OR Berlin OR Rente OR Polizei)",
    "Wirtschaft": "(Wirtschaft OR Unternehmen OR Aktien OR Inflation OR Dax OR Finanzen OR Markt OR Konzern OR Auto OR Preise)",
    "Technologie": "(Technologie OR KI OR Software OR Smartphone OR Digital OR Innovation OR Apple OR Google OR WhatsApp OR Gaming)",
    "Gesundheit": "(Gesundheit OR Medizin OR Klinik OR Patient OR RKI OR Ärzte OR Risiko OR Forschung OR Zellen OR Erkrankung)"
}
def clean_title_and_source(raw_title):
    """Seperates the titles from the source and the end of the strings"""
    if not raw_title:
        return "No Title", "Unknown"
    
    #google seperates the titles almost always with a '-'
    if ' - ' in raw_title:
        parts = raw_title.rsplit(' - ', 1)
        title = parts[0].strip()
        source = parts[1].strip()
        return title, source
    
    return raw_title.strip(), "Unknown"

def run_news_scraper():
    all_articles = []
    
    #define the timespan, it is defined by the current time minus end_date 
    #syntax: year, month, day, hour, second
    end_date = datetime(2026, 6, 7, 0, 0, 0)
    #datetime.now()

    start_date = end_date - timedelta(days=194)
    total_days = (end_date - start_date).days
    
    print(f"Starting Google news RSS scraper for {len(CATEGORIES)} categories...")
    print(f"Timespan: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}, ({total_days} days)")
    
    #day bay day loop
    for day_offset in tqdm(range(total_days), desc="Scrape progress"):
        current_date = start_date + timedelta(days=day_offset)
        next_date = current_date + timedelta(days=1)
        
        date_query = f"after:{current_date.strftime('%Y-%m-%d')} before:{next_date.strftime('%Y-%m-%d')}"
        
        for cat_name, keywords in CATEGORIES.items():
            full_query = f"{keywords} {date_query}"
            encoded_query = urllib.parse.quote(full_query)

            #the actual rss search query 
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=de&gl=DE&ceid=DE:de"
            
            try:
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries:
                    # Nutze die neue Funktion zur Trennung von Titel und Quelle
                    cleaned_title, source = clean_title_and_source(entry.title)
                    
                    all_articles.append({
                        "titel": cleaned_title,
                        "source": source,
                        "original_url": entry.link,
                        "published_raw": entry.published,
                        "category": cat_name,
                        "article_date": current_date.strftime('%Y-%m-%d')
                    })
            except Exception as e:
                #just continiue in case of a network timeout
                continue
                
        #pause for a moment to prevent a service denial from google 
        time.sleep(0.4)

    if all_articles:
        df_raw = pd.DataFrame(all_articles)
        total_raw = len(df_raw)
        
        #remove douplicates based on unique urls
        df_clean = df_raw.drop_duplicates(subset=['original_url'])
        total_clean = len(df_clean)
        
        filename = "google_news_6_month_rss_record.csv"
        #safe location in the directory this script sits in 
        path = r'./' + filename
        df_clean.to_csv(path, index=False, encoding="utf-8")

        print("\n=== DOWNLOAD COMPLETED ===")
        print(f"Raw entries: {total_raw}")
        print(f"Unique articles total: {total_clean}")
        print(f"Found duplicates: {total_raw - total_clean}")
        print(f"File saved as: {filename}")
        
        print("\nArticle distribution per category:")
        print(df_clean['category'].value_counts())

        sources_count = len(df_clean["source"].unique())
        print(f"\nUnique sources total: {sources_count}")
        
        print("\nTop 10 most frequend sources:")
        print(df_clean['source'].value_counts().head(10))
        
    else:
        print("No data found.")

if __name__ == "__main__":
    start_zeit = time.time()
    run_news_scraper()
    print(f"Task duration: {round((time.time() - start_zeit) / 60, 2)} minutes.")