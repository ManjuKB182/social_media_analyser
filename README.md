# 🌍 Travel Trend Agent - Social Media Analyser

An AI-powered social media analytics tool that tracks trending travel destinations in India using Twitter data. Features include sentiment analysis, hourly trend tracking, state-wise aggregation, and an interactive Streamlit dashboard.

## ✨ Features

### 📊 Analytics
- **Real-time Twitter Trend Tracking**: Fetches and analyzes travel-related tweets
- **Indian Cities Focus**: Filters and analyzes only Indian destinations
- **Sentiment Analysis**: Evaluates the sentiment (Positive/Neutral/Negative) of travel discussions
- **Hourly Breakdown**: Tracks when destinations are trending throughout the day
- **State-wise Aggregation**: Groups cities by their respective states for regional insights

### 🤖 AI Agent Insights
- Automatically generates intelligent summaries of trending patterns
- Identifies top destinations, peak activity times, and regional trends
- Provides actionable insights from social media data

### 📈 Visualizations
1. **Bar Charts**: Country-level trending cities
2. **Pie Charts**: Engagement distribution by location
3. **Line Charts**: Hourly activity patterns
4. **Scatter Plots**: Sentiment vs. Engagement correlation
5. **State-wise Charts**: Regional trend analysis

### 🖥️ Interactive Dashboard
- Built with Streamlit for easy interaction
- Real-time data refresh
- Multiple view options (Country, State, Hourly)
- Responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Twitter API credentials (optional - works with mock data)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd /Users/manjukb/Desktop/Antigravity/social_media_analyser
```

2. **Activate the virtual environment**
```bash
source venv/bin/activate
```

3. **Install dependencies** (if not already installed)
```bash
pip install -r requirements.txt
```

4. **Configure API Keys** (Optional)
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Running the Application

#### Option 1: Streamlit Web App (Recommended)
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

#### Option 2: Command-line Script
```bash
python trends_of_day.py
```
This will generate PNG visualizations in the current directory.

## 📁 Project Structure

```
social_media_analyser/
├── app.py                  # Streamlit web application
├── trends_of_day.py        # Command-line script
├── fetchers.py             # API clients (Twitter, Instagram, News)
├── data_processor.py       # Data processing and state mapping
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── venv/                  # Virtual environment
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Twitter API
TWITTER_BEARER_TOKEN=your_token_here

# Instagram API (optional)
INSTAGRAM_ACCESS_TOKEN=your_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id_here

# News API (optional)
NEWS_API_KEY=your_key_here
```

### Supported Indian Locations
The tool tracks trends for major cities and tourist destinations including:
- **North**: Delhi, Jaipur, Agra, Amritsar, Shimla, Manali, Rishikesh, Ladakh
- **South**: Bangalore, Chennai, Hyderabad, Mysore, Ooty, Kerala
- **East**: Kolkata, Darjeeling
- **West**: Mumbai, Pune, Goa, Udaipur, Jaisalmer
- **Islands**: Andaman

## 📊 Dashboard Sections

### 1. Agent Analysis
AI-generated insights including:
- Top trending destination
- Most active state
- Peak activity time
- Overall diversity metrics

### 2. Country Level Trends
- Bar chart of top cities by engagement
- Detailed engagement metrics (Likes + Retweets)

### 3. State-wise Analysis
- Aggregated trends by state
- Pie chart showing state distribution
- Regional comparison

### 4. Hourly Breakdown
- Line chart showing activity over 24 hours
- Identifies peak engagement times
- Multi-location comparison

## 🎨 Visualizations Generated

When running `trends_of_day.py`, the following images are created:
- `trends_visualization.png` - Bar chart of trending locations
- `hourly_trends.png` - Line chart of hourly activity
- `engagement_pie_chart.png` - Pie chart of engagement distribution
- `sentiment_scatter.png` - Scatter plot of sentiment vs engagement

## 🧪 Testing

The application works with mock data by default, so you can test it without API credentials:

```bash
# Test the data processor
python -c "from data_processor import process_data; print('✓ Data processor OK')"

# Test the fetchers
python -c "from fetchers import TwitterFetcher; t = TwitterFetcher(); print('✓ Fetchers OK')"

# Run the app
streamlit run app.py
```

## 🔍 How It Works

1. **Data Collection**: Fetches tweets using Twitter API (or mock data)
2. **Filtering**: Filters for Indian cities and travel-related content
3. **Processing**: 
   - Maps cities to states
   - Calculates sentiment scores using TextBlob
   - Aggregates engagement metrics
   - Groups by hour for temporal analysis
4. **Analysis**: Generates AI insights based on patterns
5. **Visualization**: Creates interactive charts and dashboards

## 📝 Dependencies

- `streamlit` - Web dashboard framework
- `pandas` - Data manipulation
- `matplotlib` - Static visualizations
- `tweepy` - Twitter API client
- `textblob` - Sentiment analysis
- `python-dotenv` - Environment configuration
- `requests` - HTTP requests

## 🤝 Contributing

To extend the analyser:
1. Add new cities to `CITY_STATE_MAP` in `data_processor.py`
2. Add new data sources in `fetchers.py`
3. Customize visualizations in `app.py`
4. Modify the agent insights logic in `generate_agent_insights()`

## 📄 License

This project is part of the Antigravity Agent framework.

## 🆘 Troubleshooting

**App won't start?**
- Ensure virtual environment is activated
- Check all dependencies are installed: `pip install -r requirements.txt`

**No data showing?**
- The app uses mock data by default
- To use real data, add Twitter API credentials to `.env`

**Import errors?**
- Make sure you're running from the correct directory
- The app uses relative imports that require proper path setup

## 🎯 Future Enhancements

- [ ] Instagram integration with real API
- [ ] News API integration
- [ ] Historical trend tracking
- [ ] Export reports to PDF
- [ ] Email alerts for trending destinations
- [ ] Multi-language support
- [ ] Advanced ML-based predictions

---

**Built with ❤️ using Antigravity Agent**
