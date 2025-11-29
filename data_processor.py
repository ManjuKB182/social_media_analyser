import pandas as pd
from datetime import datetime

# Mapping of major Indian cities/tourist spots to States
CITY_STATE_MAP = {
    "Goa": "Goa",
    "Jaipur": "Rajasthan",
    "Manali": "Himachal Pradesh",
    "Kerala": "Kerala",
    "Rishikesh": "Uttarakhand",
    "Mumbai": "Maharashtra",
    "Delhi": "Delhi",
    # Karnataka cities (expanded)
    "Bangalore": "Karnataka",
    "Mysore": "Karnataka",
    "Mangaluru": "Karnataka",
    "Mangalore": "Karnataka",
    "Udupi": "Karnataka",
    "Hubli": "Karnataka",
    "Hubballi": "Karnataka",
    "Belagavi": "Karnataka",
    "Belgaum": "Karnataka",
    "Davangere": "Karnataka",
    "Tumakuru": "Karnataka",
    "Tumkur": "Karnataka",
    "Chikmagalur": "Karnataka",
    "Chikkamagaluru": "Karnataka",
    "Coorg": "Karnataka",
    "Kodagu": "Karnataka",
    "Gokarna": "Karnataka",
    "Hampi": "Karnataka",
    # Other Indian cities
    "Varanasi": "Uttar Pradesh",
    "Agra": "Uttar Pradesh",
    "Udaipur": "Rajasthan",
    "Shimla": "Himachal Pradesh",
    "Ladakh": "Ladakh",
    "Ooty": "Tamil Nadu",
    "Darjeeling": "West Bengal",
    "Andaman": "Andaman and Nicobar Islands",
    "Kolkata": "West Bengal",
    "Chennai": "Tamil Nadu",
    "Hyderabad": "Telangana",
    "Pune": "Maharashtra",
    "Amritsar": "Punjab",
    "Jaisalmer": "Rajasthan",
    "Lucknow": "Uttar Pradesh",
    "Patna": "Bihar",
    "Bhopal": "Madhya Pradesh",
    "Ahmedabad": "Gujarat",
}

# Karnataka Political Parties
KARNATAKA_PARTIES = ["BJP", "Congress", "JDS", "AAP"]

# Karnataka Politicians
KARNATAKA_POLITICIANS = [
    "Siddaramaiah",
    "DK Shivakumar",
    "BS Yediyurappa",
    "Basavaraj Bommai",
    "HD Kumaraswamy",
    "HD Deve Gowda",
]

# National-level Politicians (India-wide context)
NATIONAL_POLITICIANS = [
    "Narendra Modi",
    "Amit Shah",
    "Rahul Gandhi",
    "Priyanka Gandhi",
    "Arvind Kejriwal",
    "Yogi Adityanath",
]

ALL_POLITICIANS = KARNATAKA_POLITICIANS + NATIONAL_POLITICIANS

# Sports Categories
SPORTS_CATEGORIES = ["Cricket", "Football", "Kabaddi", "Hockey", "Volleyball", "Chess"]

# Sports persons (for mock data analytics)
SPORTS_PERSONS = [
    "Virat Kohli",
    "Rohit Sharma",
    "MS Dhoni",
    "Hardik Pandya",
    "Sunil Chhetri",
    "PV Sindhu",
    "Neeraj Chopra",
    "Saina Nehwal",
]

# Cinema industries
CINEMA_INDUSTRIES = ["Hollywood", "Bollywood", "Sandalwood", "Tollywood", "Mollywood"]

# Travel high-level content categories
TRAVEL_CATEGORY_MAP = {
    # Beach destinations
    "Goa": "Beach",
    "Andaman": "Beach",
    "Kerala": "Beach",
    "Mumbai": "Beach",
    # Hill stations
    "Shimla": "Hill",
    "Ooty": "Hill",
    "Darjeeling": "Hill",
    # Mountains / adventure
    "Manali": "Mountains",
    "Ladakh": "Mountains",
    "Rishikesh": "Trekking",
    # Religious / spiritual places
    "Varanasi": "Religious",
    "Amritsar": "Religious",
}

def process_data(tweets, topic="travel"):
    """
    Process raw tweet data into a structured DataFrame.
    """
    data = []
    for tweet in tweets:
        # Parse created_at
        created_at = tweet['created_at']
        if isinstance(created_at, str):
            try:
                dt = datetime.fromisoformat(created_at)
            except ValueError:
                dt = datetime.now()
        else:
            dt = created_at

        # Common user-level metadata (may be None for some sources)
        sex = tweet.get("user_sex", "Unknown")
        age_group = tweet.get("user_age_group", "Unknown")
        user_location_raw = tweet.get("user_location_raw", tweet.get("location", "Unknown"))

        if topic == "travel":
            loc = tweet['location']
            state = "Unknown"
            normalized_loc = loc
            
            for city, mapped_state in CITY_STATE_MAP.items():
                if city.lower() in loc.lower():
                    normalized_loc = city
                    state = mapped_state
                    break
            
            category = TRAVEL_CATEGORY_MAP.get(normalized_loc, "Other")

            data.append({
                "Location": normalized_loc,
                "State": state,
                "Category": category,
                "Text": tweet['text'],
                "Likes": tweet['likes'],
                "Retweets": tweet['retweets'],
                "Engagement": tweet['likes'] + tweet['retweets'],
                "Hour": dt.hour,
                "Sentiment": 0.0,
                "Sex": sex,
                "AgeGroup": age_group,
                "UserLocationRaw": user_location_raw,
            })
        
        elif topic == "politics":
            # For politics, extract party and politician mentions
            party = "Other"
            politician = "Other"

            text_lower = tweet['text'].lower()
            for p in KARNATAKA_PARTIES:
                if p.lower() in text_lower:
                    party = p
                    break

            for pol in ALL_POLITICIANS:
                if pol.lower() in text_lower:
                    politician = pol
                    break

            # Best-effort State/Location from raw location text
            loc_raw = tweet.get("location", "Unknown")
            state = "Unknown"
            city_name = loc_raw
            for city, mapped_state in CITY_STATE_MAP.items():
                if city.lower() in loc_raw.lower():
                    city_name = city
                    state = mapped_state
                    break
            
            data.append({
                "Party": party,
                "Politician": politician,
                "Location": city_name,
                "State": state,
                "Text": tweet['text'],
                "Likes": tweet['likes'],
                "Retweets": tweet['retweets'],
                "Engagement": tweet['likes'] + tweet['retweets'],
                "Hour": dt.hour,
                "Sentiment": 0.0,
                "Sex": sex,
                "AgeGroup": age_group,
                "UserLocationRaw": user_location_raw,
            })
        
        elif topic == "sports":
            # For sports, extract sport category & (mock) sports person
            sport = "Other"
            sports_person = "Other"
            
            text_lower = tweet['text'].lower()
            for s in SPORTS_CATEGORIES:
                if s.lower() in text_lower:
                    sport = s
                    break

            for sp in SPORTS_PERSONS:
                if sp.lower() in text_lower:
                    sports_person = sp
                    break

            # Best-effort State/Location from raw location text
            loc_raw = tweet.get("location", "Unknown")
            state = "Unknown"
            city_name = loc_raw
            for city, mapped_state in CITY_STATE_MAP.items():
                if city.lower() in loc_raw.lower():
                    city_name = city
                    state = mapped_state
                    break
            
            data.append({
                "Sport": sport,
                "SportsPerson": sports_person,
                "Location": city_name,
                "State": state,
                "Text": tweet['text'],
                "Likes": tweet['likes'],
                "Retweets": tweet['retweets'],
                "Engagement": tweet['likes'] + tweet['retweets'],
                "Hour": dt.hour,
                "Sentiment": 0.0,
                "Sex": sex,
                "AgeGroup": age_group,
                "UserLocationRaw": user_location_raw,
            })

        elif topic == "cinema":
            # Movie + industry analytics
            movie = tweet.get("movie", "Unknown")
            industry = tweet.get("industry", "Other")
            if industry not in CINEMA_INDUSTRIES:
                industry = "Other"

            loc_raw = tweet.get("location", "Unknown")
            state = "Unknown"
            city_name = loc_raw
            for city, mapped_state in CITY_STATE_MAP.items():
                if city.lower() in loc_raw.lower():
                    city_name = city
                    state = mapped_state
                    break

            data.append({
                "Movie": movie,
                "Industry": industry,
                "Location": city_name,
                "State": state,
                "Text": tweet['text'],
                "Likes": tweet['likes'],
                "Retweets": tweet['retweets'],
                "Engagement": tweet['likes'] + tweet['retweets'],
                "Hour": dt.hour,
                "Sentiment": 0.0,
                "Sex": sex,
                "AgeGroup": age_group,
                "UserLocationRaw": user_location_raw,
            })
    
    df = pd.DataFrame(data)
    return df

def generate_agent_insights(df, topic="travel"):
    """
    Generate a textual summary based on the data.
    """
    if df.empty:
        return "No data available for analysis."
    
    insights = []
    
    if topic == "travel":
        # Top Location
        top_loc = df.groupby("Location")["Engagement"].sum().idxmax()
        top_eng = df.groupby("Location")["Engagement"].sum().max()
        insights.append(f"🔥 Top Trending Destination: {top_loc} is leading with {top_eng:,} total engagement.")
        
        # Top State
        top_state = df.groupby("State")["Engagement"].sum().idxmax()
        if top_state != "Unknown":
            insights.append(f"🗺️ Most Active State: {top_state} is seeing the most travel chatter.")
        
        # Peak Hour
        peak_hour = df.groupby("Hour")["Engagement"].sum().idxmax()
        insights.append(f"⏰ Peak Activity Time: The most buzz happened around {peak_hour}:00 hours.")
        
        # General Observation
        unique_locs = df["Location"].nunique()
        total_tweets = len(df)
        insights.append(f"📊 Diversity: We are tracking trends across {unique_locs} different locations with {total_tweets:,} tweets analyzed today.")
    
    elif topic == "politics":
        # Top Party
        top_party = df.groupby("Party")["Engagement"].sum().idxmax()
        top_party_eng = df.groupby("Party")["Engagement"].sum().max()
        insights.append(f"🏛️ Most Discussed Party: {top_party} with {top_party_eng:,} total engagement.")
        
        # Top Politician
        top_pol = df.groupby("Politician")["Engagement"].sum().idxmax()
        if top_pol != "Other":
            top_pol_eng = df[df["Politician"] == top_pol]["Engagement"].sum()
            insights.append(f"👤 Most Mentioned Politician: {top_pol} is dominating the conversation with {top_pol_eng:,} engagement.")
        
        # Peak Hour
        peak_hour = df.groupby("Hour")["Engagement"].sum().idxmax()
        insights.append(f"⏰ Peak Political Activity: Most discussions happened around {peak_hour}:00 hours.")
        
        # Party diversity
        unique_parties = df[df["Party"] != "Other"]["Party"].nunique()
        total_tweets = len(df)
        insights.append(f"📊 Political Landscape: Tracking {unique_parties} major parties in Karnataka with {total_tweets:,} tweets analyzed today.")
    
    elif topic == "sports":
        # Top Sport
        top_sport = df.groupby("Sport")["Engagement"].sum().idxmax()
        top_sport_eng = df.groupby("Sport")["Engagement"].sum().max()
        insights.append(f"🏆 Most Discussed Sport: {top_sport} with {top_sport_eng:,} total engagement.")
        
        # Peak Hour
        peak_hour = df.groupby("Hour")["Engagement"].sum().idxmax()
        insights.append(f"⏰ Peak Sports Activity: Most discussions happened around {peak_hour}:00 hours.")
        
        # Sport diversity
        unique_sports = df[df["Sport"] != "Other"]["Sport"].nunique()
        total_tweets = len(df)
        insights.append(f"📊 Sports Coverage: Tracking {unique_sports} major sports with {total_tweets:,} tweets analyzed today.")
        
        # Engagement comparison
        top_3_sports = df.groupby("Sport")["Engagement"].sum().nlargest(3)
        if len(top_3_sports) >= 3:
            insights.append(f"🥇 Top 3 Sports: {', '.join(top_3_sports.index.tolist())}")
    
    return "\n\n".join(insights)
