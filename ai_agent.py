import os
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class GeminiAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use gemini-2.0-flash-exp for better availability
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.chat = self.model.start_chat(history=[])
        else:
            self.model = None
            self.chat = None
            print("Warning: GEMINI_API_KEY not found in environment variables.")

    def generate_insights(self, df, topic):
        """
        Generates analytical insights based on the dataframe summary.
        """
        if not self.model:
            return "⚠️ Gemini API Key not configured. Please add GEMINI_API_KEY to your .env file."

        # Prepare data summary
        summary = self._prepare_data_summary(df, topic)
        
        prompt = f"""
        You are ShaNya, an expert Social Media Analyst AI specializing in Twitter data analysis.
        
        Your role:
        - Analyze tweets from Twitter API data for the topic '{topic}'
        - Understand sentiment, engagement patterns, and trending discussions
        - Identify key influencers, viral content, and emerging trends
        - Provide actionable insights based on real-time social media conversations
        
        Data Summary from Twitter:
        {summary}
        
        Provide 3-4 key insights focusing on:
        1. Top trending entities (locations/parties/sports) with engagement metrics
        2. Peak activity times and what's driving the conversations
        3. Notable patterns or anomalies in the data
        4. Actionable recommendations based on the trends
        
        Keep the tone professional yet engaging. Use emojis strategically.
        Format as bullet points starting with ★
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {str(e)}"

    def chat_with_data(self, user_input, df, topic):
        """
        Chat with the data context.
        """
        if not self.chat:
            return "⚠️ Gemini API Key not configured."

        # Update context if needed (simplified for now)
        summary = self._prepare_data_summary(df, topic)
        
        context_prompt = f"""
        You are ShaNya, an AI assistant specialized in analyzing Twitter data and social media trends.
        
        Context: You're currently analyzing Twitter data for '{topic}'.
        
        Available Twitter Data Summary:
        {summary}
        
        This data represents real tweets collected via Twitter API, including:
        - Tweet text content and engagement metrics (likes, retweets)
        - Temporal patterns (hourly activity)
        - Geographic or categorical distributions
        - Sentiment and discussion themes
        
        User Question: {user_input}
        
        Instructions:
        - Answer based on the Twitter data provided
        - Reference specific metrics and trends from the tweets
        - If the answer requires data not available, politely explain what's missing
        - Provide context about what the Twitter data reveals
        - Keep answers concise, insightful, and actionable
        - Use a friendly, professional tone
        """
        
        try:
            response = self.chat.send_message(context_prompt)
            return response.text
        except Exception as e:
            return f"Error processing chat: {str(e)}"

    def metric_health_summary(self, df, topic):
        """
        Returns a dict: { 'total_records': 'Good', 'engagement': 'Low', 'timerange': 'Peak hours covered', ... }
        Use LLM for summary lines/comments, or fallback on rule-based msg if no LLM. Designed for metrics_box integration.
        """
        if df.empty:
            return { 'total_records': 'No data', 'engagement': 'No engagement', 'timerange': 'No active range' }
        # Heuristic/LLM hybrid (skeleton):
        avg_engagement = df['Engagement'].mean() if len(df) else 0
        total_engagement = df['Engagement'].sum()
        min_hour, max_hour = df['Hour'].min(), df['Hour'].max()
        health = {}
        # Basic thresholds (more advanced: LLM)
        health['total_records'] = '🟢 High volume' if len(df) > 1000 else '🟠 Needs more data'
        if total_engagement > avg_engagement * len(df):
            health['engagement'] = '🟢 Above avg engagement'
        else:
            health['engagement'] = '🔴 Below avg; check content'
        if (min_hour == 0 and max_hour == 23) or (max_hour - min_hour) > 10:
            health['timerange'] = '🟢 Good hourly coverage'
        else:
            health['timerange'] = f'🟠 Limited: {min_hour}:00-{max_hour}:00'
        # Advanced (Gemini)
        if self.model:
            try:
                prompt = f"For social analytics on {topic}, comment on the following quick stats: Total records = {len(df)}, Engagement = {total_engagement}, Hour range = {min_hour}-{max_hour}. Give concise (5-10 words) status for each: Total records, Engagement, Time range."
                response = self.model.generate_content(prompt)
                summary_lines = response.text.strip().split('\n')
                for line in summary_lines:
                    if 'record' in line:
                        health['total_records'] = line
                    elif 'engagement' in line:
                        health['engagement'] = line
                    elif 'time' in line or 'hour' in line:
                        health['timerange'] = line
            except Exception as e:
                pass
        return health

    def _prepare_data_summary(self, df, topic):
        """
        Creates a string summary of the dataframe for the LLM.
        """
        if df.empty:
            return "No data available."
            
        total_records = len(df)
        total_engagement = df['Engagement'].sum()
        
        summary = f"Topic: {topic}\n"
        summary += f"Total Records: {total_records}\n"
        summary += f"Total Engagement: {total_engagement}\n"
        
        # Top entities
        if 'Location' in df.columns:
            top_locs = df.groupby('Location')['Engagement'].sum().nlargest(3).to_dict()
            summary += f"Top Locations: {top_locs}\n"
            
        if 'Party' in df.columns:
            top_parties = df.groupby('Party')['Engagement'].sum().nlargest(3).to_dict()
            summary += f"Top Parties: {top_parties}\n"
            
        if 'Sport' in df.columns:
            top_sports = df.groupby('Sport')['Engagement'].sum().nlargest(3).to_dict()
            summary += f"Top Sports: {top_sports}\n"
            
        # Hourly peak
        hourly_peak = df.groupby('Hour')['Engagement'].sum().idxmax()
        summary += f"Peak Activity Hour: {hourly_peak}:00\n"
        
        return summary
