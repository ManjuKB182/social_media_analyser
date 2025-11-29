import os
from dotenv import load_dotenv
from fetchers import TwitterFetcher, InstagramFetcher, NewsFetcher
from collections import Counter

# Load environment variables
load_dotenv()

KEYWORDS = ['travel', 'hiking', 'mountain', 'sea', 'beach', 'hill', 'tourism', 'vacation', 'adventure', 'nature']

# List of major Indian cities and tourist destinations for filtering
INDIAN_LOCATIONS = [
    "Goa", "Jaipur", "Manali", "Kerala", "Rishikesh", "Mumbai", "Delhi", "Bangalore", 
    "Varanasi", "Agra", "Udaipur", "Shimla", "Ladakh", "Mysore", "Ooty", "Darjeeling",
    "Andaman", "Kolkata", "Chennai", "Hyderabad", "Pune", "Amritsar", "Jaisalmer"
]

from textblob import TextBlob

def analyze_trends():
    print("Initializing Social Media Trend Analyser (India Focus)...")
    
    twitter = TwitterFetcher()
    # instagram = InstagramFetcher() # Focusing on Twitter for now as requested
    # news = NewsFetcher()

    print("\n--- Fetching Twitter Trends for India ---")
    tweets = twitter.fetch_trends()
    print(f"Fetched {len(tweets)} tweets.")

    print("\n--- Analyzing Twitter Data ---")
    
    # Group by location
    location_data = {}
    
    for tweet in tweets:
        loc = tweet['location']
        if loc == "Unknown":
            continue
        
        # Filter for Indian locations
        # Simple check: is the location in our list? (Case insensitive partial match could be better but exact match for now)
        is_indian = False
        for indian_loc in INDIAN_LOCATIONS:
            if indian_loc.lower() in loc.lower():
                is_indian = True
                # Normalize location name to the one in our list for cleaner grouping
                loc = indian_loc 
                break
        
        if not is_indian:
            continue
            
        if loc not in location_data:
            location_data[loc] = {
                "tweets": [],
                "total_likes": 0,
                "total_retweets": 0,
                "sentiment_scores": [],
                "hourly_engagement": {} # Hour -> Engagement
            }
        
        # Sentiment Analysis
        blob = TextBlob(tweet['text'])
        sentiment = blob.sentiment.polarity
        
        # Hourly Analysis
        # Handle both datetime objects (real API) and strings (mock data)
        created_at = tweet['created_at']
        if isinstance(created_at, str):
            from datetime import datetime
            # Handle ISO format from mock data
            try:
                dt = datetime.fromisoformat(created_at)
            except ValueError:
                dt = datetime.now() # Fallback
        else:
            dt = created_at
            
        hour = dt.hour
        
        location_data[loc]["tweets"].append(tweet)
        location_data[loc]["total_likes"] += tweet['likes']
        location_data[loc]["total_retweets"] += tweet['retweets']
        location_data[loc]["sentiment_scores"].append(sentiment)
        
        engagement = tweet['likes'] + tweet['retweets']
        location_data[loc]["hourly_engagement"][hour] = location_data[loc]["hourly_engagement"].get(hour, 0) + engagement

    print("\n=== DETAILED TWITTER TREND REPORT ===")
    
    if not location_data:
        print("No location-specific trends found.")
        return

    # Sort locations by total engagement (likes + retweets)
    sorted_locs = sorted(
        location_data.items(), 
        key=lambda item: item[1]['total_likes'] + item[1]['total_retweets'], 
        reverse=True
    )

    for loc, data in sorted_locs:
        avg_sentiment = sum(data['sentiment_scores']) / len(data['sentiment_scores'])
        sentiment_label = "Neutral"
        if avg_sentiment > 0.1: sentiment_label = "Positive"
        elif avg_sentiment < -0.1: sentiment_label = "Negative"
        
        top_tweet = max(data['tweets'], key=lambda t: t['likes'])
        
        print(f"\n📍 LOCATION: {loc}")
        print(f"   - Mentions: {len(data['tweets'])}")
        print(f"   - Engagement: {data['total_likes']} Likes, {data['total_retweets']} Retweets")
        print(f"   - Sentiment: {sentiment_label} ({avg_sentiment:.2f})")
        print(f"   - Top Tweet: \"{top_tweet['text']}\"")
        
        # Print hourly breakdown
        print(f"   - Hourly Activity: {dict(sorted(data['hourly_engagement'].items()))}")

    visualize_trends(location_data)

import matplotlib.pyplot as plt

def visualize_trends(location_data):
    """
    Generates:
    1. Bar chart of trending locations by engagement (trends_visualization.png)
    2. Line chart of hourly trends (hourly_trends.png)
    """
    if not location_data:
        return

    # --- Chart 1: Bar Chart ---
    # Prepare data
    locations = []
    engagements = []
    colors = []

    # Sort by engagement for better visualization
    sorted_items = sorted(
        location_data.items(), 
        key=lambda item: item[1]['total_likes'] + item[1]['total_retweets'], 
        reverse=True
    )

    for loc, data in sorted_items:
        locations.append(loc)
        engagements.append(data['total_likes'] + data['total_retweets'])
        
        avg_sentiment = sum(data['sentiment_scores']) / len(data['sentiment_scores'])
        if avg_sentiment > 0.1:
            colors.append('green') # Positive
        elif avg_sentiment < -0.1:
            colors.append('red') # Negative
        else:
            colors.append('gray') # Neutral

    # Plotting Bar Chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(locations, engagements, color=colors)
    
    plt.xlabel('Locations')
    plt.ylabel('Total Engagement (Likes + Retweets)')
    plt.title('Trending Travel Destinations by Engagement & Sentiment')
    plt.xticks(rotation=45, ha='right')
    
    # Add legend manually
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Positive'),
        Patch(facecolor='gray', label='Neutral'),
        Patch(facecolor='red', label='Negative')
    ]
    plt.legend(handles=legend_elements, title="Sentiment")
    
    plt.tight_layout()
    output_file = 'trends_visualization.png'
    plt.savefig(output_file)
    print(f"\nVisualization saved to {output_file}")
    plt.close() # Close the figure to start fresh

    # --- Chart 2: Hourly Trends Line Chart ---
    plt.figure(figsize=(12, 6))
    
    # Plot a line for each location
    for loc, data in sorted_items[:5]: # Top 5 locations to avoid clutter
        hourly_data = data['hourly_engagement']
        hours = sorted(hourly_data.keys())
        hourly_engs = [hourly_data[h] for h in hours]
        
        plt.plot(hours, hourly_engs, marker='o', label=loc)
    
    plt.xlabel('Hour of Day (24h)')
    plt.ylabel('Engagement')
    plt.title('Hourly Trend Activity (Top 5 Locations)')
    plt.xticks(range(0, 24)) # Show all hours
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.tight_layout()
    hourly_output_file = 'hourly_trends.png'
    plt.savefig(hourly_output_file)
    print(f"Hourly visualization saved to {hourly_output_file}")
    plt.close()

    # --- Chart 3: Pie Chart (Engagement Distribution) ---
    plt.figure(figsize=(8, 8))
    plt.pie(engagements, labels=locations, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title('Engagement Distribution by Location')
    
    pie_output_file = 'engagement_pie_chart.png'
    plt.savefig(pie_output_file)
    print(f"Pie chart saved to {pie_output_file}")
    plt.close()

    # --- Chart 4: Scatter Plot (Sentiment vs Engagement) ---
    plt.figure(figsize=(10, 6))
    
    # Extract data for scatter plot
    sentiments = []
    total_engagements = []
    
    for loc, data in sorted_items:
        avg_sentiment = sum(data['sentiment_scores']) / len(data['sentiment_scores'])
        sentiments.append(avg_sentiment)
        total_engagements.append(data['total_likes'] + data['total_retweets'])
        
    plt.scatter(sentiments, total_engagements, color='blue', alpha=0.7, s=100)
    
    # Add labels to points
    for i, loc in enumerate(locations):
        plt.annotate(loc, (sentiments[i], total_engagements[i]), xytext=(5, 5), textcoords='offset points')
        
    plt.axvline(0, color='gray', linestyle='--', alpha=0.5) # Neutral line
    plt.xlabel('Average Sentiment (Polarity)')
    plt.ylabel('Total Engagement')
    plt.title('Sentiment vs. Engagement Analysis')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    scatter_output_file = 'sentiment_scatter.png'
    plt.savefig(scatter_output_file)
    print(f"Scatter plot saved to {scatter_output_file}")
    plt.close()

if __name__ == "__main__":
    analyze_trends()
