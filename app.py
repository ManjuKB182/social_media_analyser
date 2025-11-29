import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import random
from pathlib import Path
from fetchers import TwitterFetcher
from data_processor import process_data
from ai_agent import GeminiAgent  # Re-enable GeminiAgent
from dotenv import load_dotenv
from components.css import inject_main_css
from components.metrics_box import render_metrics
from components.tabs import travel_tabs, politics_tabs, sports_tabs, cinema_tabs

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

# Function definitions FIRST
# ---
def load_data(topic_name, from_date, end_date, time_range):
    twitter = TwitterFetcher()
    if topic_name == "Travel":
        raw_tweets = twitter.fetch_trends(query="travel India", from_date=from_date, end_date=end_date)
        df = process_data(raw_tweets, topic="travel")
    elif topic_name == "Cinema":
        # Cinema-specific tweets with movie/industry info
        raw_tweets = twitter.fetch_trends(query="cinema India", topic="cinema", from_date=from_date, end_date=end_date)
        df = process_data(raw_tweets, topic="cinema")
    elif topic_name == "Politics":
        raw_tweets = twitter.fetch_politics_trends(from_date=from_date, end_date=end_date)
        df = process_data(raw_tweets, topic="politics")
    else:  # Sports
        raw_tweets = twitter.fetch_sports_trends(from_date=from_date, end_date=end_date)
        df = process_data(raw_tweets, topic="sports")
    if not df.empty:
        df = df[(df["Hour"] >= time_range[0]) & (df["Hour"] <= time_range[1])]
    return df

def render_simple_insights(df, topic_label: str):
    """Show 3 concise, data-driven insights for the current dashboard."""
    if df is None or df.empty:
        return

    insights = []

    # Top state
    if "State" in df.columns and not df["State"].dropna().empty:
        top_state_series = df.groupby("State")["Engagement"].sum().sort_values(ascending=False)
        top_state = top_state_series.index[0]
        top_state_val = int(top_state_series.iloc[0])
        insights.append(f"Top state by engagement is **{top_state}** with **{top_state_val:,}** interactions.")

    # Top city/location
    if "Location" in df.columns and not df["Location"].dropna().empty:
        top_city_series = df.groupby("Location")["Engagement"].sum().sort_values(ascending=False)
        top_city = top_city_series.index[0]
        top_city_val = int(top_city_series.iloc[0])
        insights.append(f"Most active city is **{top_city}** with **{top_city_val:,}** engagement.")

    # Demographic split
    if "Sex" in df.columns and not df["Sex"].dropna().empty:
        sex_series = df.groupby("Sex")["Engagement"].sum().sort_values(ascending=False)
        top_sex = sex_series.index[0]
        top_sex_val = int(sex_series.iloc[0])
        insights.append(f"Highest-engaging segment by sex is **{top_sex}** with **{top_sex_val:,}** interactions.")
    elif "AgeGroup" in df.columns and not df["AgeGroup"].dropna().empty:
        age_series = df.groupby("AgeGroup")["Engagement"].sum().sort_values(ascending=False)
        top_age = age_series.index[0]
        insights.append(f"Most responsive age group is **{top_age}**.")

    # Trim to 3 insights max
    insights = insights[:3]
    if not insights:
        return

    st.markdown(
        f'<div class="insight-box" style="margin-top:0.5rem;margin-bottom:0.75rem;">'
        f'<div class="insight-title">📌 Key Insights for {topic_label} Dashboard</div>',
        unsafe_allow_html=True,
    )
    for i_text in insights:
        st.markdown(f"- {i_text}")
    st.markdown("</div>", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="Social Trend Agent", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")
st.markdown(inject_main_css(), unsafe_allow_html=True)

# Header UI
st.markdown('<h1 class="main-header">🔍 Social Trend Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Real-Time Analysis of Social Media Trends</p>', unsafe_allow_html=True)

# Sidebar UI
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 4rem;">🤖</div>
            <h2 style="margin-top: 1rem; color: #FF416C;">Configuration</h2>
        </div>
    """, unsafe_allow_html=True)
    topic = st.selectbox(
        "📊 Select Analysis Topic",
        ["Travel", "Politics", "Sports", "Cinema"],
        help="Choose the topic you want to analyze"
    )
    st.markdown("---")
    st.markdown("### 📅 Date & Time Filters")
    col1, col2 = st.columns(2)
    with col1:
        from_date = st.date_input("From Date", value=pd.Timestamp.now().date(), help="Start date for analysis")
    with col2:
        end_date = st.date_input("To Date", value=pd.Timestamp.now().date(), help="End date for analysis")
    st.markdown("#### ⏰ Time Range")
    time_range = st.slider(
        "Select Hour Range",
        min_value=0,
        max_value=23,
        value=(0, 23),
        help="Filter data by hour of day (0-23)"
    )
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    fetch_latest = st.button("🔃 Fetch Latest Now", use_container_width=True)
    st.markdown("---")
    st.markdown("### 📈 About")
    st.info(f"Analyzing **{topic}** trends with AI-powered sentiment analysis.")
    filter_info = f"""
    **Active Filters:**
    - Date: {from_date} to {end_date}
    - Time: {time_range[0]}:00 - {time_range[1]}:00
    """
    st.success(filter_info)
    st.markdown("---")
    st.markdown("### 🎯 Features")
    st.markdown("""
    - 🔍 Real-time tracking
    - 💭 Sentiment analysis
    - ⏰ Hourly breakdown
    - 📊 Interactive charts
    """)

# Load agent
agent = GeminiAgent()

# Data & LLM loading/processing
llm_summary = None  # For LLM dashboard insights

if fetch_latest:
    # Real-time/on-demand fetch for selected topic (last 1 hour)
    twitter = TwitterFetcher()
    trending_queries = []
    if topic == "Travel":
        trending_queries = [{"topic": "travel", "query": "travel India"}]
    elif topic == "Cinema":
        trending_queries = [{"topic": "cinema", "query": "cinema India"}]
    elif topic == "Politics":
        trending_queries = [{"topic": "politics", "query": "Karnataka politics"}]
    else:
        trending_queries = [{"topic": "sports", "query": "India sports"}]
    raw_tweets = twitter.fetch_realtime_trends(trending_queries, time_window_hrs=1, max_results_per_query=40)
    # Map UI topic to processing topic
    proc_topic = "travel" if topic == "Travel" else "cinema" if topic == "Cinema" else "politics" if topic == "Politics" else "sports"
    df = process_data(raw_tweets, topic=proc_topic)
    if not df.empty:
        df = df[(df["Hour"] >= time_range[0]) & (df["Hour"] <= time_range[1])]
    # Immediately analyze with LLM
    llm_summary = agent.generate_insights(df, topic)
else:
    df = load_data(topic, from_date, end_date, time_range)

# Normalize sample size to always have ~100,000 rows for analysis window
TARGET_SAMPLE_SIZE = 100_000
if df is not None and not df.empty:
    n = len(df)
    if n > TARGET_SAMPLE_SIZE:
        df = df.sample(n=TARGET_SAMPLE_SIZE, random_state=42)
    elif n < TARGET_SAMPLE_SIZE:
        # Upsample with replacement so dashboards stay stable even when real API returns fewer rows
        df = df.sample(n=TARGET_SAMPLE_SIZE, replace=True, random_state=42)

# Insights & Dashboard rendering
metrics_summary = None
if llm_summary and not df.empty:
    # Compute metric summary silently (used only in compact metrics box, no separate LLM panel)
    metrics_summary = agent.metric_health_summary(df, topic)

# In dashboard section for each topic (simple tab-based dashboards):
if not df.empty:
    # Simple, non-LLM 3-point insight summary for the current dashboard
    render_simple_insights(df, topic)

    if topic == "Travel":
        travel_tabs(df)
    elif topic == "Cinema":
        cinema_tabs(df)
    elif topic == "Politics":
        politics_tabs(df)
    else:
        sports_tabs(df)
    render_metrics(df, insights_summary=metrics_summary)
st.markdown("---")
st.markdown('<p style="text-align: center; color: #636e72; font-size: 0.9rem;">Powered by <strong style="background: linear-gradient(90deg, #FF416C 0%, #FFD93D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Antigravity Agent</strong> • Data Source: Twitter (Mock/Real)</p>', unsafe_allow_html=True)
