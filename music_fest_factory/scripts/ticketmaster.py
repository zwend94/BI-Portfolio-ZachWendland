import os
import pandas as pd
import requests
from datetime import datetime, timedelta

#Change the working directory
os.chdir('C:/Users/lyyud/Documents/spotify_project')

#Ticketmaster API key
API_KEY = 'h7aGjAVcQbASRNQSAuweAHxmAVItAlQC'

#Ticketmaster API endpoint
ENDPOINT = 'https://app.ticketmaster.com/discovery/v2/events.json'

#Load artist names from top_arist_by_genre.csv
file_path = 'C:/Users/lyyud/Documents/spotify_project/top_artists_by_genre.csv'
artist_data = pd.read_csv(file_path)
artists = artist_data["Artist Name"].tolist()

#Define date range
today = datetime.now()
trailing_12_months = (today - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
next_12_months = (today + timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')

#List to store event data
all_events = []

#Function to get event data for an artist
def fetch_events_for_artist(artist_name, start_date, end_date):
    params = {
        'apikey': API_KEY,
        'keyword': artist_name,
        'classificationName': 'music',
        'startDateTime': start_date,
        'endDateTime': end_date,
        'size': 150  
    }
    response = requests.get(ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {artist_name}: {response.status_code}")
        return None
#Get data for each artist
for artist in artists:
    print(f"Fetching events for artist: {artist}")
    
    #Get T12M
    historical_data = fetch_events_for_artist(artist, trailing_12_months, today.strftime('%Y-%m-%dT%H:%M:%SZ'))
    if historical_data and '_embedded' in historical_data:
        events = historical_data['_embedded']['events']
        for event in events:
            event_name = event.get('name', 'N/A')
            event_id = event.get('id', 'N/A')
            event_url = event.get('url', 'N/A')
            event_date = event.get('dates', {}).get('start', {}).get('localDate', 'N/A')
            sales = event.get('sales', {})
            venue_info = event.get('_embedded', {}).get('venues', [{}])[0]
            venue_name = venue_info.get('name', 'N/A')
            venue_capacity = venue_info.get('capacity', 'N/A')
            dma = venue_info.get('dma', 'N/A')
            market = venue_info.get('market', 'N/A')
            general_info = venue_info.get('generalInfo', {}).get('generalRule', 'N/A')
            tickets_sold = venue_info.get('upcomingEvents', {}).get('ticketmaster', 'N/A')  # Placeholder for tickets sold
            attendance = sales.get('attendance', 'N/A')  # Placeholder for attendance
            promoter_info = event.get('promoter', {})
            promoter_name = promoter_info.get('name', 'N/A')
            price_ranges = event.get('priceRanges', [{}])[0]
            min_price = price_ranges.get('min', 'N/A')
            max_price = price_ranges.get('max', 'N/A')
            avg_price = (min_price + max_price) / 2 if isinstance(min_price, (int, float)) and isinstance(max_price, (int, float)) else 'N/A'
            classifications = event.get('classifications', [{}])[0]
            primary_genre = classifications.get('genre', {}).get('name', 'N/A')
            sub_genre = classifications.get('subGenre', {}).get('name', 'N/A')

            all_events.append({
                'artist_name': artist,
                'event_name': event_name,
                'event_id': event_id,
                'event_url': event_url,
                'event_date': event_date,
                'sales_data': sales,
                'venue_name': venue_name,
                'venue_capacity': venue_capacity,
                'dma': dma,
                'market': market,
                'general_info': general_info,
                'tickets_sold': tickets_sold,
                'attendance': attendance,
                'promoter_name': promoter_name,
                'min_price': min_price,
                'max_price': max_price,
                'average_price': avg_price,
                'primary_genre': primary_genre,
                'sub_genre': sub_genre,
                'timeframe': 'Trailing 12 Months'
            })
    
    # Fetch next 12 months
    future_data = fetch_events_for_artist(artist, today.strftime('%Y-%m-%dT%H:%M:%SZ'), next_12_months)
    if future_data and '_embedded' in future_data:
        events = future_data['_embedded']['events']
        for event in events:
            event_name = event.get('name', 'N/A')
            event_id = event.get('id', 'N/A')
            event_url = event.get('url', 'N/A')
            event_date = event.get('dates', {}).get('start', {}).get('localDate', 'N/A')
            sales = event.get('sales', {})
            venue_info = event.get('_embedded', {}).get('venues', [{}])[0]
            venue_name = venue_info.get('name', 'N/A')
            venue_capacity = venue_info.get('capacity', 'N/A')
            dma = venue_info.get('dma', 'N/A')
            market = venue_info.get('market', 'N/A')
            general_info = venue_info.get('generalInfo', {}).get('generalRule', 'N/A')
            tickets_sold = venue_info.get('upcomingEvents', {}).get('ticketmaster', 'N/A') 
            attendance = sales.get('attendance', 'N/A') 
            promoter_info = event.get('promoter', {})
            promoter_name = promoter_info.get('name', 'N/A')
            price_ranges = event.get('priceRanges', [{}])[0]
            min_price = price_ranges.get('min', 'N/A')
            max_price = price_ranges.get('max', 'N/A')
            avg_price = (min_price + max_price) / 2 if isinstance(min_price, (int, float)) and isinstance(max_price, (int, float)) else 'N/A'
            classifications = event.get('classifications', [{}])[0]
            primary_genre = classifications.get('genre', {}).get('name', 'N/A')
            sub_genre = classifications.get('subGenre', {}).get('name', 'N/A')

            all_events.append({
                'artist_name': artist,
                'event_name': event_name,
                'event_id': event_id,
                'event_url': event_url,
                'event_date': event_date,
                'sales_data': sales,
                'venue_name': venue_name,
                'venue_capacity': venue_capacity,
                'dma': dma,
                'market': market,
                'general_info': general_info,
                'tickets_sold': tickets_sold,
                'attendance': attendance,
                'promoter_name': promoter_name,
                'min_price': min_price,
                'max_price': max_price,
                'average_price': avg_price,
                'primary_genre': primary_genre,
                'sub_genre': sub_genre,
                'timeframe': 'Next 12 Months'
            })

# Create a DataFrame from the event data
events_df = pd.DataFrame(all_events)

# Save the results to a CSV file
output_file = 'ticketmaster_events_detailed_2.csv'
events_df.to_csv(output_file, index=False)

print(f"Event data saved to {output_file}")
