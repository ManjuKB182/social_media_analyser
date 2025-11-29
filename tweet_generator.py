import random
from datetime import datetime, timedelta

class TweetGenerator:
    """Generates large volumes of realistic mock tweet data"""
    
    # Cinema: movies by industry with preferred discussion hubs
    CINEMA_MOVIES = {
        # Hollywood
        "Dune 2":       {"industry": "Hollywood", "locations": ["Mumbai", "Delhi", "Bangalore"]},
        "Oppenheimer":  {"industry": "Hollywood", "locations": ["Mumbai", "Delhi", "Hyderabad"]},
        "Avengers 5":   {"industry": "Hollywood", "locations": ["Mumbai", "Kolkata", "Chennai"]},
        # Bollywood
        "Pathaan":      {"industry": "Bollywood", "locations": ["Mumbai", "Delhi", "Agra"]},
        "Jawan":        {"industry": "Bollywood", "locations": ["Mumbai", "Pune", "Bangalore"]},
        "Gadar 3":      {"industry": "Bollywood", "locations": ["Delhi", "Varanasi", "Jaipur"]},
        # Sandalwood (Kannada)
        "KGF 3":        {"industry": "Sandalwood", "locations": ["Bangalore", "Mysore", "Davangere"]},
        "Kantara 2":    {"industry": "Sandalwood", "locations": ["Mangalore", "Udupi", "Shimla"]},
        "Sapta Sagarada 3": {"industry": "Sandalwood", "locations": ["Bangalore", "Tumakuru", "Chikmagalur"]},
        # Tollywood (Telugu)
        "RRR 2":        {"industry": "Tollywood", "locations": ["Hyderabad", "Chennai", "Bangalore"]},
        "Pushpa 2":     {"industry": "Tollywood", "locations": ["Hyderabad", "Chennai", "Goa"]},
        # Mollywood (Malayalam)
        "Drishyam 3":   {"industry": "Mollywood", "locations": ["Kerala", "Bangalore", "Mumbai"]},
        "Premalu":      {"industry": "Mollywood", "locations": ["Kerala", "Hyderabad", "Chennai"]},
    }
    
    # Travel templates
    TRAVEL_TEMPLATES = {
        "Goa": [
            "Beach vibes in {loc}! #travel #beach",
            "Sunset at {loc} is breathtaking! #goa",
            "Party night in {loc}! Best nightlife ever #travel",
            "Water sports in {loc} were amazing! #adventure",
            "Seafood in {loc} is incredible! #foodie",
            "Relaxing on {loc} beaches #vacation",
            "Best time in {loc}! Highly recommend #travel",
            "{loc} never disappoints! #beachlife"
        ],
        "Manali": [
            "Snowfall in {loc} is magical! #mountains",
            "Paragliding in {loc} - what a thrill! #adventure",
            "Rohtang Pass views from {loc} are stunning! #travel",
            "Cozy cafes in {loc} ❤️ #mountainlife",
            "Trekking around {loc} - best experience! #hiking",
            "{loc} in winter is paradise! #snow",
            "Adventure sports in {loc} are top-notch! #adventure"
        ],
        "Jaipur": [
            "Royal palaces of {loc} are mesmerizing! #heritage",
            "Hawa Mahal in {loc} is architectural marvel! #travel",
            "Shopping in {loc} markets is a must! #pinkcity",
            "Amber Fort near {loc} at sunrise - magical! #rajasthan",
            "{loc} heritage walk was amazing! #culture",
            "Traditional food in {loc} is delicious! #foodie"
        ],
        "Kerala": [
            "{loc} backwaters are so peaceful! #travel",
            "Houseboat experience in {loc} is amazing! #kerala",
            "Tea gardens in {loc} are beautiful! #nature",
            "{loc} cuisine is incredible! #foodtravel",
            "Ayurveda retreat in {loc} was transformative! #wellness",
            "{loc} - God's own country indeed! #travel"
        ],
        "Rishikesh": [
            "River rafting in {loc} - adrenaline rush! #adventure",
            "Yoga retreat in {loc} was life-changing! #wellness",
            "Ganga Aarti in {loc} is mesmerizing! #spiritual",
            "Trekking around {loc} was an adventure! #hiking",
            "{loc} is perfect for spiritual seekers! #yoga",
            "Bungee jumping in {loc}! #adventure"
        ],
        "Mumbai": [
            "{loc} - the city that never sleeps! #mumbai",
            "Marine Drive in {loc} at night is stunning! #travel",
            "Street food in {loc} is unbeatable! #foodie",
            "Gateway of India in {loc} - iconic! #mumbai",
            "{loc} local train experience! #travel",
            "Bollywood vibes in {loc}! #entertainment"
        ],
        "Varanasi": [
            "{loc} ghats at sunrise - spiritual bliss! #travel",
            "Boat ride on Ganges in {loc} was peaceful! #spiritual",
            "Ancient temples of {loc} are magnificent! #heritage",
            "{loc} is a spiritual experience! #travel",
            "Evening aarti in {loc} is unforgettable! #spiritual"
        ],
        "Bangalore": [
            "{loc} weather is perfect! #nammabengaluru",
            "Cubbon Park in {loc} is so peaceful! #nature",
            "Cafe hopping in {loc} is amazing! #coffeecity",
            "{loc} nightlife is vibrant! #travel",
            "Tech hub {loc} has great food scene! #foodie"
        ],
        "Ladakh": [
            "{loc} landscapes are otherworldly! #adventure",
            "Pangong Lake in {loc} is stunning! #travel",
            "Bike trip to {loc} - dream come true! #roadtrip",
            "{loc} monasteries are peaceful! #spiritual",
            "Stargazing in {loc} is magical! #nature"
        ],
        "Agra": [
            "Taj Mahal in {loc} at sunrise - no words! #travel",
            "{loc} Fort is equally impressive! #history",
            "Petha from {loc} is delicious! #foodtravel",
            "{loc} - city of love! #tajmahal"
        ],
        "Udaipur": [
            "Lake Pichola in {loc} at sunset is breathtaking! #travel",
            "City Palace in {loc} is stunning! #rajasthan",
            "Boat ride in {loc} was romantic! #lakecity",
            "{loc} - Venice of the East! #travel"
        ],
        "Shimla": [
            "{loc} in winter is magical! #himachal",
            "Mall Road in {loc} is bustling! #hillstation",
            "Toy train to {loc} was nostalgic! #travel",
            "{loc} snowfall is beautiful! #winter"
        ],
        "Mysore": [
            "{loc} Palace illumination is spectacular! #heritage",
            "Chamundi Hills near {loc} - amazing views! #karnataka",
            "{loc} silk sarees are famous! #shopping"
        ],
        # Additional Karnataka cities for richer Karnataka dashboards
        "Mangaluru": [
            "Beaches in {loc} are underrated! #karnataka",
            "Seafood in {loc} is next level! #foodie",
            "Monsoon drives around {loc} are beautiful! #travel"
        ],
        "Udupi": [
            "Temple town {loc} is so peaceful! #spiritual",
            "Udupi cuisine in {loc} is a must-try! #foodtravel"
        ],
        "Hubli": [
            "{loc} is buzzing with new developments! #karnataka",
            "Markets in {loc} are always lively! #travel"
        ],
        "Belagavi": [
            "Historic forts around {loc} are worth visiting! #heritage",
            "Weather in {loc} is pleasant this season! #karnataka"
        ],
        "Davangere": [
            "{loc} benne dosa is legendary! #foodie",
            "Streets of {loc} are full of life! #travel"
        ],
        "Tumakuru": [
            "Road trips to {loc} from Bangalore are fun! #weekend",
            "Hill views near {loc} are refreshing! #nature"
        ],
        "Chikmagalur": [
            "Coffee estates in {loc} are stunning! #coffee",
            "Sunrise treks around {loc} are unforgettable! #trekking"
        ],
        "Coorg": [
            "{loc} is perfect for a weekend getaway! #coorg",
            "Waterfalls near {loc} look amazing in monsoon! #nature"
        ],
        "Gokarna": [
            "Beaches in {loc} are perfect for a quiet escape! #beach",
            "Trekking between beaches in {loc} is awesome! #trekking"
        ],
        "Hampi": [
            "Ruins of {loc} feel like open-air museum! #heritage",
            "Sunset at {loc} boulders is magical! #travel"
        ],
        "Ooty": [
            "{loc} botanical gardens are beautiful! #tamilnadu",
            "Toy train in {loc} is charming! #hillstation",
            "{loc} tea estates are picturesque! #nature"
        ],
        "Darjeeling": [
            "{loc} tea gardens are stunning! #westbengal",
            "Tiger Hill sunrise from {loc} is worth it! #travel",
            "{loc} toy train ride is iconic! #heritage"
        ]
    }
    
    # Politics templates
    POLITICS_TEMPLATES = {
        "BJP": [
            "BJP announces new development projects for Karnataka #politics",
            "BJP holds massive rally in Bangalore #karnataka",
            "BJP criticizes opposition on governance #politics",
            "BJP promises infrastructure development #karnataka",
            "BJP celebrates victory in local elections #politics",
            "BJP announces new schemes for farmers #karnataka",
            "BJP leader addresses rally in Mysore #politics"
        ],
        "Congress": [
            "Congress criticizes government policies #karnataka",
            "Congress promises 5 guarantees for voters #politics",
            "Congress holds massive rally in Hubli #karnataka",
            "Congress announces free electricity scheme #politics",
            "Congress leader addresses farmers' concerns #karnataka",
            "Congress promises job creation for youth #politics"
        ],
        "JDS": [
            "JDS focuses on rural development #karnataka",
            "JDS announces farmer loan waiver #politics",
            "JDS criticizes major parties #karnataka",
            "JDS promises better crop prices #politics",
            "JDS holds rally in Mandya #karnataka"
        ],
        "AAP": [
            "AAP announces free water and electricity #karnataka",
            "AAP criticizes traditional parties #politics",
            "AAP holds first major rally in Bangalore #karnataka",
            "AAP promises corruption-free governance #politics"
        ]
    }
    
    # Sports templates
    SPORTS_TEMPLATES = {
        "Cricket": [
            "What a match! India vs Australia cricket is intense! #cricket",
            "Virat Kohli century! Incredible innings #cricket #india",
            "IPL auction is heating up! Big bids today #cricket #ipl",
            "Test cricket at its finest! Great bowling #cricket",
            "T20 World Cup excitement building! #cricket #worldcup",
            "Rohit Sharma's captaincy is brilliant #cricket #india",
            "Cricket fever! Stadium is packed today #cricket",
            "Historic cricket victory for India! #cricket #celebration"
        ],
        "Football": [
            "ISL match was thrilling! Great goals #football #isl",
            "Indian football team showing improvement #football #india",
            "Sunil Chhetri legend! Another goal #football #captain",
            "Football fever in Kolkata! Mohun Bagan vs East Bengal #football",
            "Premier League watch party! #football #epl",
            "FIFA World Cup discussions heating up #football #worldcup",
            "Indian Super League finals approaching! #football #isl"
        ],
        "Kabaddi": [
            "Pro Kabaddi League is amazing! #kabaddi #pkl",
            "Kabaddi raid was spectacular! #kabaddi #india",
            "Traditional sport making comeback! #kabaddi",
            "PKL auction results are out! #kabaddi #prokabaddi",
            "India dominates in Kabaddi World Cup! #kabaddi #worldcup",
            "Kabaddi is India's pride! #kabaddi #traditional",
            "Incredible kabaddi match tonight! #kabaddi #pkl"
        ],
        "Hockey": [
            "Indian hockey team wins! Proud moment #hockey #india",
            "Hockey World Cup excitement! #hockey #worldcup",
            "Olympic hockey dreams alive! #hockey #olympics",
            "Field hockey is back in spotlight #hockey #india",
            "Hockey India League starting soon! #hockey #hil",
            "Women's hockey team inspiring! #hockey #india",
            "Historic hockey victory! #hockey #celebration"
        ],
        "Volleyball": [
            "Volleyball championship underway! #volleyball #india",
            "Pro Volleyball League is exciting! #volleyball #pvl",
            "Indian volleyball team improving! #volleyball",
            "Beach volleyball tournament! #volleyball #sports",
            "Volleyball spike was incredible! #volleyball",
            "Indoor volleyball finals today! #volleyball #championship"
        ],
        "Chess": [
            "Viswanathan Anand brilliance! #chess #india",
            "Chess Olympiad excitement! #chess #olympiad",
            "Praggnanandhaa's amazing game! #chess #prodigy",
            "India dominating in chess! #chess #grandmaster",
            "Chess World Championship discussions #chess",
            "Online chess tournament trending! #chess #online",
            "Chess is mental sport at its best! #chess #strategy"
        ]
    }
    
    POLITICIAN_TEMPLATES = {
        "Siddaramaiah": [
            "Siddaramaiah promises free electricity #congress",
            "Siddaramaiah criticizes BJP policies #karnataka",
            "Siddaramaiah addresses rally in Mysore #politics",
            "Siddaramaiah speaks on healthcare #karnataka"
        ],
        "DK Shivakumar": [
            "DK Shivakumar meets farmers #congress",
            "DK Shivakumar promises infrastructure #karnataka",
            "DK Shivakumar addresses rally #politics",
            "DK Shivakumar inaugurates new office #karnataka"
        ],
        "BS Yediyurappa": [
            "BS Yediyurappa comments on coalition politics #bjp",
            "BS Yediyurappa meets party workers #karnataka",
            "BS Yediyurappa speaks on development #politics",
            "BS Yediyurappa inaugurates hospital #karnataka"
        ],
        "Basavaraj Bommai": [
            "Basavaraj Bommai inaugurates metro line #bjp",
            "Basavaraj Bommai announces IT park #karnataka",
            "Basavaraj Bommai meets startup founders #politics",
            "Basavaraj Bommai addresses farmers #karnataka"
        ],
        "HD Kumaraswamy": [
            "HD Kumaraswamy meets farmers #jds",
            "HD Kumaraswamy criticizes policies #karnataka",
            "HD Kumaraswamy promises irrigation projects #politics",
            "HD Kumaraswamy speaks on rural development #karnataka"
        ],
        "HD Deve Gowda": [
            "HD Deve Gowda criticizes major parties #jds",
            "HD Deve Gowda speaks on farmer issues #karnataka",
            "HD Deve Gowda addresses party workers #politics",
            "HD Deve Gowda on regional politics #karnataka"
        ]
    }
    
    @staticmethod
    def generate_travel_tweets(count=5000, from_date=None, end_date=None):
        """Generate travel tweets"""
        tweets = []
        locations = list(TweetGenerator.TRAVEL_TEMPLATES.keys())
        now = datetime.now()
        
        # Use provided dates or default to today
        if from_date is None:
            from_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            from_date = datetime.combine(from_date, datetime.min.time())
        
        if end_date is None:
            end_date = now
        else:
            end_date = datetime.combine(end_date, datetime.max.time())
        
        # Guarantee at least N tweets per hour in range
        total_hours = int(((end_date - from_date).total_seconds()) // 3600) + 1
        min_per_hour = max(1, count // max(1, total_hours))
        for h in range(total_hours):
            this_hour = from_date + timedelta(hours=h)
            for _ in range(min_per_hour):
                loc = random.choice(locations)
                template = random.choice(TweetGenerator.TRAVEL_TEMPLATES[loc])
                text = template.format(loc=loc)
                # Random minute/second within hour
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                created_at = this_hour.replace(minute=minute, second=second)
                base_likes = random.randint(50, 1000)
                likes = int(base_likes * random.uniform(0.8, 1.5))
                retweets = int(likes * random.uniform(0.1, 0.3))
                # Mock basic user metadata for demographics
                user_id = f"u{random.randint(1, 500000)}"
                sex = random.choices(["M", "F", "Other"], weights=[4, 4, 1])[0]
                age_group = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[3, 4, 2, 1])[0]
                tweets.append({
                    "text": text,
                    "location": loc,
                    "likes": likes,
                    "retweets": retweets,
                    "created_at": created_at.isoformat(),
                    # user-level fields
                    "user_id": user_id,
                    "user_name": f"Traveler {user_id}",
                    "user_sex": sex,
                    "user_age_group": age_group,
                    "user_location_raw": f"{loc}, India",
                })
        # Fill remaining tweets randomly
        while len(tweets) < count:
            loc = random.choice(locations)
            template = random.choice(TweetGenerator.TRAVEL_TEMPLATES[loc])
            text = template.format(loc=loc)
            rand_seconds = random.uniform(0, (end_date - from_date).total_seconds())
            created_at = from_date + timedelta(seconds=rand_seconds)
            base_likes = random.randint(50, 1000)
            likes = int(base_likes * random.uniform(0.8, 1.5))
            retweets = int(likes * random.uniform(0.1, 0.3))
            user_id = f"u{random.randint(1, 500000)}"
            sex = random.choices(["M", "F", "Other"], weights=[4, 4, 1])[0]
            age_group = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[3, 4, 2, 1])[0]
            tweets.append({
                "text": text,
                "location": loc,
                "likes": likes,
                "retweets": retweets,
                "created_at": created_at.isoformat(),
                "user_id": user_id,
                "user_name": f"Traveler {user_id}",
                "user_sex": sex,
                "user_age_group": age_group,
                "user_location_raw": f"{loc}, India",
            })
        return tweets
    
    @staticmethod
    def generate_politics_tweets(count=5000, from_date=None, end_date=None):
        """Generate politics tweets"""
        tweets = []
        parties = list(TweetGenerator.POLITICS_TEMPLATES.keys())
        politicians = list(TweetGenerator.POLITICIAN_TEMPLATES.keys())
        # Reuse travel locations for India-wide geography
        travel_locs = list(TweetGenerator.TRAVEL_TEMPLATES.keys())
        now = datetime.now()
        
        # Use provided dates or default to today
        if from_date is None:
            from_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            from_date = datetime.combine(from_date, datetime.min.time())
        
        if end_date is None:
            end_date = now
        else:
            end_date = datetime.combine(end_date, datetime.max.time())
        
        total_hours = int(((end_date - from_date).total_seconds()) // 3600) + 1
        min_per_hour = max(1, count // max(1, total_hours))
        for h in range(total_hours):
            this_hour = from_date + timedelta(hours=h)
            for _ in range(min_per_hour):
                loc = random.choice(travel_locs)
                if random.random() < 0.6:
                    party = random.choice(parties)
                    text = random.choice(TweetGenerator.POLITICS_TEMPLATES[party])
                else:
                    politician = random.choice(politicians)
                    text = random.choice(TweetGenerator.POLITICIAN_TEMPLATES[politician])
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                created_at = this_hour.replace(minute=minute, second=second)
                base_likes = random.randint(100, 1500)
                likes = int(base_likes * random.uniform(0.8, 1.5))
                retweets = int(likes * random.uniform(0.1, 0.35))
                user_id = f"u{random.randint(1, 500000)}"
                sex = random.choices(["M", "F", "Other"], weights=[5, 3, 1])[0]
                age_group = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[2, 4, 3, 2])[0]
                tweets.append({
                    "text": text,
                    "location": loc,
                    "likes": likes,
                    "retweets": retweets,
                    "created_at": created_at.isoformat(),
                    "user_id": user_id,
                    "user_name": f"Voter {user_id}",
                    "user_sex": sex,
                    "user_age_group": age_group,
                    "user_location_raw": f"{loc}, India",
                })
        while len(tweets) < count:
            loc = random.choice(travel_locs)
            if random.random() < 0.6:
                party = random.choice(parties)
                text = random.choice(TweetGenerator.POLITICS_TEMPLATES[party])
            else:
                politician = random.choice(politicians)
                text = random.choice(TweetGenerator.POLITICIAN_TEMPLATES[politician])
            rand_seconds = random.uniform(0, (end_date - from_date).total_seconds())
            created_at = from_date + timedelta(seconds=rand_seconds)
            base_likes = random.randint(100, 1500)
            likes = int(base_likes * random.uniform(0.8, 1.5))
            retweets = int(likes * random.uniform(0.1, 0.35))
            user_id = f"u{random.randint(1, 500000)}"
            sex = random.choices(["M", "F", "Other"], weights=[5, 3, 1])[0]
            age_group = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[2, 4, 3, 2])[0]
            tweets.append({
                "text": text,
                "location": loc,
                "likes": likes,
                "retweets": retweets,
                "created_at": created_at.isoformat(),
                "user_id": user_id,
                "user_name": f"Voter {user_id}",
                "user_sex": sex,
                "user_age_group": age_group,
                "user_location_raw": f"{loc}, India",
            })
        return tweets
    
    @staticmethod
    def generate_sports_tweets(count=5000, from_date=None, end_date=None):
        """Generate sports tweets"""
        tweets = []
        sports = list(TweetGenerator.SPORTS_TEMPLATES.keys())
        travel_locs = list(TweetGenerator.TRAVEL_TEMPLATES.keys())
        now = datetime.now()
        
        # Use provided dates or default to today
        if from_date is None:
            from_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            from_date = datetime.combine(from_date, datetime.min.time())
        
        if end_date is None:
            end_date = now
        else:
            end_date = datetime.combine(end_date, datetime.max.time())
        
        total_hours = int(((end_date - from_date).total_seconds()) // 3600) + 1
        min_per_hour = max(1, count // max(1, total_hours))
        for h in range(total_hours):
            this_hour = from_date + timedelta(hours=h)
            for _ in range(min_per_hour):
                sport = random.choice(sports)
                text = random.choice(TweetGenerator.SPORTS_TEMPLATES[sport])
                loc = random.choice(travel_locs)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                created_at = this_hour.replace(minute=minute, second=second)
                base_likes = random.randint(100, 2000)
                likes = int(base_likes * random.uniform(0.8, 1.5))
                retweets = int(likes * random.uniform(0.15, 0.4))
                user_id = f"u{random.randint(1, 500000)}"
                sex = random.choices(["M", "F", "Other"], weights=[4, 3, 1])[0]
                age_group = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[3, 4, 2, 1])[0]
                tweets.append({
                    "text": text,
                    "location": loc,
                    "likes": likes,
                    "retweets": retweets,
                    "created_at": created_at.isoformat(),
                    "user_id": user_id,
                    "user_name": f"Fan {user_id}",
                    "user_sex": sex,
                    "user_age_group": age_group,
                    "user_location_raw": f"{loc}, India",
                })
        while len(tweets) < count:
            sport = random.choice(sports)
            text = random.choice(TweetGenerator.SPORTS_TEMPLATES[sport])
            loc = random.choice(travel_locs)
            rand_seconds = random.uniform(0, (end_date - from_date).total_seconds())
            created_at = from_date + timedelta(seconds=rand_seconds)
            base_likes = random.randint(100, 2000)
            likes = int(base_likes * random.uniform(0.8, 1.5))
            retweets = int(likes * random.uniform(0.15, 0.4))
            user_id = f"u{random.randint(1, 500000)}"
            sex = random.choices(["M", "F", "Other"], weights=[4, 3, 1])[0]
            age_group = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[3, 4, 2, 1])[0]
            tweets.append({
                "text": text,
                "location": loc,
                "likes": likes,
                "retweets": retweets,
                "created_at": created_at.isoformat(),
                "user_id": user_id,
                "user_name": f"Fan {user_id}",
                "user_sex": sex,
                "user_age_group": age_group,
                "user_location_raw": f"{loc}, India",
            })
        return tweets

    @staticmethod
    def generate_cinema_tweets(count=5000, from_date=None, end_date=None):
        """Generate cinema/movie discussion tweets."""
        tweets = []
        movies = list(TweetGenerator.CINEMA_MOVIES.keys())
        now = datetime.now()

        # Use provided dates or default to today
        if from_date is None:
            from_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            from_date = datetime.combine(from_date, datetime.min.time())

        if end_date is None:
            end_date = now
        else:
            end_date = datetime.combine(end_date, datetime.max.time())

        total_hours = int(((end_date - from_date).total_seconds()) // 3600) + 1
        min_per_hour = max(1, count // max(1, total_hours))

        def _make_tweet(movie_name, loc, this_hour):
            meta = TweetGenerator.CINEMA_MOVIES[movie_name]
            industry = meta["industry"]
            # simple natural-language templates
            templates = [
                "Watching {movie} in {loc} tonight! #{industry}",
                "{movie} buzz in {loc} is unreal right now. #{industry}",
                "Debating {movie} with friends in {loc} – what a film! #{industry}",
                "{movie} shows almost full in {loc}. Hype is real. #{industry}",
                "Tickets for {movie} sold out in {loc}! #{industry}",
            ]
            text = random.choice(templates).format(movie=movie_name, loc=loc, industry=industry.lower())
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            created_at = this_hour.replace(minute=minute, second=second)
            base_likes = random.randint(50, 1200)
            likes = int(base_likes * random.uniform(0.8, 1.6))
            retweets = int(likes * random.uniform(0.1, 0.35))
            user_id = f"u{random.randint(1, 500000)}"
            sex = random.choices(["M", "F", "Other"], weights=[4, 4, 1])[0]
            age_group = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[3, 4, 2, 1])[0]
            return {
                "text": text,
                "location": loc,
                "likes": likes,
                "retweets": retweets,
                "created_at": created_at.isoformat(),
                "user_id": user_id,
                "user_name": f"MovieFan {user_id}",
                "user_sex": sex,
                "user_age_group": age_group,
                "user_location_raw": f"{loc}, India",
                "movie": movie_name,
                "industry": industry,
            }

        # Ensure dense hourly coverage
        for h in range(total_hours):
            this_hour = from_date + timedelta(hours=h)
            for _ in range(min_per_hour):
                movie_name = random.choice(movies)
                loc = random.choice(TweetGenerator.CINEMA_MOVIES[movie_name]["locations"])
                tweets.append(_make_tweet(movie_name, loc, this_hour))

        # Fill remaining tweets randomly across window
        while len(tweets) < count:
            movie_name = random.choice(movies)
            loc = random.choice(TweetGenerator.CINEMA_MOVIES[movie_name]["locations"])
            rand_seconds = random.uniform(0, (end_date - from_date).total_seconds())
            created_at = from_date + timedelta(seconds=rand_seconds)
            tweets.append(_make_tweet(movie_name, loc, created_at))

        return tweets
