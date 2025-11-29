import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
try:
    from wordcloud import WordCloud
except ImportError:
    WordCloud = None

# --- NEW: Topic Velocity Scoreboard ---
def render_velocity_scoreboard(trend_list, title='Topic Velocity Scoreboard'):
    if not trend_list:
        return
    st.markdown(f"## 🚀 {title}")
    
    # Configurable Thresholds (Expander)
    with st.expander("⚙️ Configure Velocity Formula & Thresholds"):
        col1, col2, col3 = st.columns(3)
        alpha = col1.slider("Alpha (Engagement Weight)", 0.1, 5.0, 1.0, 0.1)
        beta = col2.slider("Beta (Likes Weight)", 0.1, 5.0, 1.0, 0.1)
        gamma = col3.slider("Gamma (Retweets Weight)", 0.1, 5.0, 2.0, 0.1)
        st.caption("Velocity = α*Engagement + β*Likes + γ*Retweets")
    
    def action_color(score):
        if score >= 8:
            return 'background-color:#2ecc40;color:white;font-weight:bold;'  # Go/green
        elif score >= 5:
            return 'background-color:#ffd93d;color:black;font-weight:bold;'  # Monitor/yellow
        else:
            return 'background-color:#ff4b2b;color:white;font-weight:bold;'  # No-go/red

    tbl = pd.DataFrame(trend_list)
    # Ensure required columns exist (graceful fallback)
    required_cols = ['Rank','Topic','Velocity Score','Action','Prediction','Top Influencer','Mentions','Type']
    for c in required_cols:
        if c not in tbl.columns:
            tbl[c] = '-' # Fill missing with dash

    display_tbl = tbl[required_cols]
    
    # Style via apply
    def style_row(row):
        styles = [''] * len(row) # Default no style
        action_idx = row.index.get_loc('Action')
        
        if row['Action'] == 'GO NOW!':
            styles[action_idx] = action_color(9)
        elif row['Action'] == 'Monitor':
            styles[action_idx] = action_color(6)
        else:
            styles[action_idx] = action_color(3)
        return styles

    st.dataframe(
        display_tbl.style.apply(style_row, axis=1), 
        use_container_width=True, 
        hide_index=True
    )

    # Detail Popups (Click simulation via selectbox or expander for row details)
    selected_topic = st.selectbox("🔍 View Details for Topic:", ["Select a topic..."] + list(tbl['Topic'].unique()))
    if selected_topic != "Select a topic...":
        row = tbl[tbl['Topic'] == selected_topic].iloc[0]
        with st.container():
            st.markdown(f"### 📌 Deep Dive: {selected_topic}")
            c1, c2 = st.columns([1,2])
            with c1:
                st.metric("Velocity Score", f"{row['Velocity Score']}/10", delta=row['Prediction'])
                st.write(f"**Action:** {row['Action']}")
                st.write(f"**Type:** {row['Type']}")
            with c2:
                st.info(f"💡 **Top Influencer:** {row['Top Influencer']}\n\n**Strategy:** Capitalize on this trend immediately if score > 8. Check competitor angles.")
                # Placeholder for a mini trend chart if we had time-series data passed here
                st.caption("Trend history (Last 24h): 📈 ↗️ ➡️ (Simulated)")

    st.markdown("<span style='font-size:0.95em;color:#666;'>TOP 5 topics, scored by trend velocity. Green = GO NOW, Yellow = Monitor, Red = Skip. Click rows for details.</span>", unsafe_allow_html=True)

# --- NEW: Geo/Time Audience Heatmap ---
def render_geo_time_heatmap(df, geo_field, title="Peak Audience Time Heatmap"):
    if df.empty or geo_field not in df.columns or 'Hour' not in df.columns or 'Engagement' not in df.columns:
        return
    st.markdown(f"### ⏰ {title}")
    heat_df = df.groupby([geo_field,'Hour'])['Engagement'].sum().reset_index()
    pivot = heat_df.pivot(index=geo_field, columns='Hour', values='Engagement').fillna(0)
    plt.figure(figsize=(12, min(0.5+0.6*len(pivot),8)))
    sns.set(font_scale=0.9)
    ax = sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.2, annot=True, fmt=".0f", cbar=True, annot_kws={"size":8})
    ax.set_xlabel('Hour of Day (24h)', fontsize=11, fontweight='bold')
    ax.set_ylabel(geo_field, fontsize=12, fontweight='bold')
    ax.set_title('Audience Engagement by Hour & Geo', fontsize=13, pad=8)
    plt.yticks(rotation=0)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()
    st.caption("Hotter colors = peak activity. Use this to time uploads for initial algorithmic boost.")

def render_video_health_table(df, video_field='Title', ctr_field='CTR', duration_field='Avg. View Duration', cr_field='Comment/Reply Ratio', n_recent=5, title='Recent Video Health Check'):
    # Only plot if all fields exist
    needed = [video_field, ctr_field, duration_field, cr_field]
    if any(c not in df.columns for c in needed):
        st.info('Not enough data for Recent Video Health Check')
        return
    tbl = df[[video_field, ctr_field, duration_field, cr_field]].sort_values(by=duration_field, ascending=False).head(n_recent).copy()
    avg_ctr = df[ctr_field].mean()
    avg_dur = df[duration_field].mean()
    avg_cr = df[cr_field].mean()
    def status_row(row):
        status = []
        colors = []
        for val, avg in zip([row[ctr_field], row[duration_field], row[cr_field]], [avg_ctr, avg_dur, avg_cr]):
            if val >= avg * 1.05:
                status.append('👍')
                colors.append('background-color:#27ae60; color:white;')
            elif val >= avg * 0.95:
                status.append('⚠️')
                colors.append('background-color:#ffd93d; color:black;')
            else:
                status.append('🔻')
                colors.append('background-color:#e74c3c; color:white;')
        tbl_status = max(set(status), key=status.count)
        overall_col = colors[status.index(tbl_status)]
        return [None, None, None, None, tbl_status, overall_col]
    tbl['Status'] = ''
    styled = tbl.style.apply(lambda row: ['' for _ in range(4)] + [status_row(row)[4]], axis=1)
    tbl.columns = ['Title','CTR (%)','Avg. View Duration (s)','Comment/Reply Ratio','Status']
    st.markdown(f"### 📊 {title}")
    st.dataframe(tbl, use_container_width=True, hide_index=True)
    st.caption('Color status: Green = above avg, Yellow = near avg, Red = below avg (vs channel average). Use this for thumbnail/title or format optimization.')

def render_dropoff_funnel(df, time_col='Timestamp', remain_col='Viewers_Remaining', n_annotate=3, title='Viewer Drop-Off Funnel'):
    if any(c not in df.columns for c in [time_col, remain_col]) or len(df) < 4:
        st.info('Not enough data for drop-off funnel.')
        return
    st.markdown(f"### 🔻 {title}")
    # Calculate drop points
    df = df.sort_values(by=time_col).reset_index(drop=True)
    drops = df[remain_col].shift(1) - df[remain_col]
    top_drops = drops.abs().nlargest(n_annotate + 1).iloc[1:]  # skip first (na)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df[time_col], df[remain_col], marker='o', color="#FF416C", lw=2)
    for ann_idx in top_drops.index:
        ax.annotate(f"Drop here\n{df[time_col][ann_idx]}: {int(df[remain_col][ann_idx])}%",
            xy=(df[time_col][ann_idx], df[remain_col][ann_idx]),
            xytext=(0, -26), textcoords='offset points', ha='center', fontsize=10,
            arrowprops=dict(arrowstyle='->', color='#2d3436'), color='#e74c3c')
    ax.set_xlabel('Progress (Time or %)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Viewers Remaining (%)', fontsize=11, fontweight='bold')
    ax.set_title('Viewer Retention/Drop-off Funnel', fontsize=13)
    ax.grid(True, linestyle='--', alpha=0.25)
    sns.despine()
    st.pyplot(fig)
    st.caption("The top 3 drop-offs are shown. Focus revision here to retain more viewers!")

def render_loyalty_conversion_health(df, date_col='Date', subs_col='Subscribers', unsubs_col='Unsubscribes', conv_col='External_Conversions', title='Loyalty & Conversion Health'):
    needed = [date_col, subs_col, unsubs_col, conv_col]
    if any(c not in df.columns for c in needed):
        st.info('Not enough data for Loyalty & Conversion Health. (Requires Date, Subscribers, Unsubscribes, External_Conversions)')
        return
    st.markdown(f'### 🤝 {title}')
    health = df[[date_col, subs_col, unsubs_col, conv_col]].sort_values(date_col).copy()
    health['Net Growth'] = health[subs_col] - health[unsubs_col]
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.bar(health[date_col], health['Net Growth'], color=['#27ae60' if x>=0 else '#e74c3c' for x in health['Net Growth']], alpha=0.72, label='Net Growth')
    ax1.set_ylabel('Net Subscriber Growth', color='#2d3436', fontsize=11)
    ax1.set_xlabel('Date', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#2d3436')
    ax2 = ax1.twinx()
    ax2.plot(health[date_col], health[conv_col], color='#2986cc', lw=2, marker='o', label='External Conversions')
    ax2.set_ylabel('External Conversions', color='#2986cc', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#2986cc')
    fig.tight_layout()
    plt.title('Subs Growth vs. Conversions Over Time', fontsize=13)
    sns.despine()
    st.pyplot(fig)
    st.caption('Green = subscriber growth, Red = net loss. Blue = conversions. Use this to identify best-performers and churn risks.')

def render_sentiment_meter(df, entity_col='Entity', pos_col='Positive', neu_col='Neutral', neg_col='Negative', n_entities=5, title='7-Day Sentiment Meter'):
    needed = [entity_col, pos_col, neu_col, neg_col]
    if any(c not in df.columns for c in needed) or df.empty:
        st.info('Not enough sentiment data available.')
        return
    st.markdown(f'### 📶 {title}')
    top = df.sort_values(pos_col, ascending=False).head(n_entities)
    for i, row in top.iterrows():
        labels = ['Positive','Neutral','Negative']
        values = [row[pos_col], row[neu_col], row[neg_col]]
        colors = ['#27ae60','#ffd93d','#e74c3c']
        fig, ax = plt.subplots(figsize=(6, 1.2))
        ax.barh([row[entity_col]], [row[pos_col]], color=colors[0], label='Positive')
        ax.barh([row[entity_col]], [row[neu_col]], left=[row[pos_col]], color=colors[1], label='Neutral')
        ax.barh([row[entity_col]], [row[neg_col]], left=[row[pos_col]+row[neu_col]], color=colors[2], label='Negative')
        ax.set_xlim(0, max(sum(values), 1))
        ax.set_title(f"{row[entity_col]}: Sentiment Split", fontsize=10, pad=2)
        ax.set_axisbelow(True)
        ax.get_yaxis().set_visible(False)
        ax.legend(labels, loc='upper right', frameon=False, bbox_to_anchor=(1.2, 1.05),fontsize=9)
        for i, v in enumerate(values):
            ax.text(row[pos_col] if i==0 else row[pos_col]+row[neu_col] if i==1 else sum(values), 0.05, f'{int(v)}', color='#2d3436', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
    st.caption('Sentiment score is color-coded: green = positive, yellow = neutral, red = negative. Use for tone setting or contrarian takes.')

def render_topic_cluster_cloud(df, comment_col='Comment', keyword_col=None, max_words=40, title='Comment Topic Cluster Word Cloud'):
    st.markdown(f'### 💬 {title}')
    # Try keyword first, else fall back to comment text tokenization
    words = []
    if keyword_col and keyword_col in df.columns:
        for kw_list in df[keyword_col].dropna():
            if isinstance(kw_list, str):
                words.extend(kw_list.split(','))
            else:
                words.extend(list(kw_list))
    elif comment_col in df.columns:
        txt = ' '.join(df[comment_col].astype(str))
        words = [w.lower() for w in txt.split() if len(w) > 3 and w.isalpha()]
    if not words:
        st.info('Not enough comment/topic data for clustering.')
        return
    word_counts = Counter(words).most_common(max_words)
    words_dict = dict(word_counts)
    if WordCloud is not None and words_dict:
        wc = WordCloud(width=900, height=300, background_color='white', colormap='cool').generate_from_frequencies(words_dict)
        fig, ax = plt.subplots(figsize=(9, 3.5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    elif words_dict:
        # fallback: bar chart
        labels, vals = zip(*word_counts[:15])
        fig, ax = plt.subplots(figsize=(8,2.2))
        ax.barh(labels, vals, color='#27ae60')
        ax.set_title('Top Comment Keywords (freq)', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
    st.caption('Comment topics sized by frequency. Use large ones for new community/Q&A ideas.')

def render_competitor_opinion_map(df, competitor_col='Competitor', topic_col='Topic', opinion_col='Opinion', title='Competitor Opinion Map'):
    st.markdown(f'### 🧐 {title}')
    needed = [competitor_col, topic_col, opinion_col]
    if any(c not in df.columns for c in needed) or df.empty:
        st.info('Not enough competitor/opinion data.')
        return
    opinion_tbl = df.pivot(index=competitor_col, columns=topic_col, values=opinion_col).fillna('-')
    st.dataframe(opinion_tbl, use_container_width=True)
    st.caption("Table shows each competitor's stance on key topics/events. Use to differentiate your unique take!")

def travel_tabs(df):
    """
    Simple Travel dashboard:
    - India level state-wise trend (excluding Karnataka)
    - Top 10 cities in India
    - Category-wise (Hill, Mountains, Beach, Trekking, Religious Places)
    - Interaction split by Sex and Age groups
    - Karnataka-only city-wise hourly trend
    """
    # Split India vs Karnataka: India tabs exclude Karnataka, Karnataka tab is dedicated
    if "State" in df.columns:
        df_india = df[df["State"] != "Karnataka"].copy()
    else:
        df_india = df.copy()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🇮🇳 State Trends", "🏙️ Top 10 Cities", "🏷️ Categories", "👥 Demographics", "🕒 Karnataka Cities / Hour"]
    )

    # --- Tab 1: India level state-wise trend ---
    with tab1:
        st.markdown("### India State-wise Travel Trend")
        if "State" not in df_india.columns:
            st.info("No State information available in travel data.")
        else:
            state_df = (
                df_india.groupby("State")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            if state_df.empty:
                st.info("No engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.barh(state_df["State"], state_df["Engagement"], color="#FF416C")
                ax.set_xlabel("Total Engagement")
                ax.set_ylabel("State")
                ax.set_title("Travel Engagement by State (India)")
                plt.gca().invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig)

    # --- Tab 2: Top 10 cities in India ---
    with tab2:
        st.markdown("### Top 10 Cities in India — Travel Trend")
        if "Location" not in df_india.columns:
            st.info("Location column not available in travel data.")
        else:
            city_df = (
                df_india.groupby("Location")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            if city_df.empty:
                st.info("No city-level engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(city_df["Location"], city_df["Engagement"], color="#FF8D29")
                ax.set_xlabel("City / Destination")
                ax.set_ylabel("Engagement")
                ax.set_title("Top 10 Cities in India by Travel Engagement")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(city_df, width='stretch')

    # --- Tab 3: Category-wise trends ---
    with tab3:
        st.markdown("### Category-wise Travel Trends")
        if "Category" not in df_india.columns:
            st.info("No Category information available. Ensure TRAVEL_CATEGORY_MAP is set.")
        else:
            # Focus on requested categories; group others
            focus_cats = ["Hill", "Mountains", "Beach", "Trekking", "Religious"]
            # Keep only the configured categories; drop Others
            tmp = df_india[df_india["Category"].isin(focus_cats)].copy()
            tmp["CategoryView"] = tmp["Category"]
            cat_df = (
                tmp.groupby("CategoryView")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(cat_df["CategoryView"], cat_df["Engagement"], color="#27ae60")
            ax.set_xlabel("Category")
            ax.set_ylabel("Engagement")
            ax.set_title("Engagement by Travel Category")
            plt.tight_layout()
            st.pyplot(fig)
            st.dataframe(cat_df, width='stretch')

    # --- Tab 4: Interactions split by Sex & Age group ---
    with tab4:
        st.markdown("### Interaction Split by Sex & Age Groups")
        if "Sex" not in df_india.columns or "AgeGroup" not in df_india.columns:
            st.info("Sex / AgeGroup columns not found in data.")
        else:
            col1, col2 = st.columns(2)
            # Sex split
            with col1:
                sex_df = (
                    df_india.groupby("Sex")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if sex_df.empty:
                    st.info("No engagement by Sex available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.pie(
                        sex_df["Engagement"],
                        labels=sex_df["Sex"],
                        autopct="%1.1f%%",
                        startangle=90,
                    )
                    ax.set_title("Engagement by Sex")
                    st.pyplot(fig)
            # Age group split
            with col2:
                age_df = (
                    df_india.groupby("AgeGroup")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if age_df.empty:
                    st.info("No engagement by AgeGroup available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.bar(age_df["AgeGroup"], age_df["Engagement"], color="#2986cc")
                    ax.set_xlabel("Age Group")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Engagement by Age Group")
                    plt.tight_layout()
                    st.pyplot(fig)

    # --- Tab 5: Karnataka only — city-wise hourly trend ---
    with tab5:
        st.markdown("### Karnataka — City-wise Hourly Travel Trend")
        if "State" not in df.columns or "Location" not in df.columns:
            st.info("State/Location columns not available in travel data.")
        else:
            df_ka = df[df["State"] == "Karnataka"].copy()
            if df_ka.empty:
                st.info("No Karnataka-specific travel data available.")
            else:
                hourly_city = df_ka.pivot_table(
                    index="Hour", columns="Location", values="Engagement", aggfunc="sum", fill_value=0
                )
                if hourly_city.empty:
                    st.info("No hourly city-wise data for Karnataka.")
                else:
                    # Limit to top 10 cities by total engagement
                    top_cities = (
                        df_ka.groupby("Location")["Engagement"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(10)
                        .index
                    )
                    fig, ax = plt.subplots(figsize=(12, 5))
                    for city in hourly_city.columns:
                        if city in top_cities:
                            ax.plot(hourly_city.index, hourly_city[city], marker="o", linewidth=2, label=city)
                    ax.set_xlabel("Hour of Day")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Karnataka: City-wise Hourly Travel Engagement (Top 10 Cities)")
                    ax.grid(True, linestyle="--", alpha=0.2)
                    ax.legend()
        plt.tight_layout()
        st.pyplot(fig)


def politics_tabs(df):
    """
    Simple Politics dashboard:
    - India level state-wise trend
    - Top 10 cities in India
    - Party-wise trend (INC/BJP/JDS/AAP/Others + top 3 others)
    - Interaction split by Sex and Age groups
    - Karnataka-only politician hourly trend
    """
    # Split India vs Karnataka: India tabs exclude Karnataka, Karnataka tab is dedicated
    if "State" in df.columns:
        df_india = df[df["State"] != "Karnataka"].copy()
    else:
        df_india = df.copy()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🇮🇳 State Trends", "🏙️ Top 10 Cities", "🏛️ Parties", "👥 Demographics", "🕒 Karnataka Politicians / Hour"]
    )

    # --- Tab 1: India level state-wise trend ---
    with tab1:
        st.markdown("### India State-wise Political Trend")
        if "State" not in df_india.columns:
            st.info("No State information available in politics data.")
        else:
            state_df = (
                df_india.groupby("State")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            if state_df.empty:
                st.info("No engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.barh(state_df["State"], state_df["Engagement"], color="#FF416C")
                ax.set_xlabel("Total Engagement")
                ax.set_ylabel("State")
                ax.set_title("Political Engagement by State (India)")
                plt.gca().invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(state_df, width='stretch')

    # --- Tab 2: Top 10 cities in India ---
    with tab2:
        st.markdown("### Top 10 Cities in India — Political Trend")
        if "Location" not in df_india.columns:
            st.info("Location column not available in politics data.")
        else:
            city_df = (
                df_india.groupby("Location")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            if city_df.empty:
                st.info("No city-level engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(city_df["Location"], city_df["Engagement"], color="#FF8D29")
                ax.set_xlabel("City / Location")
                ax.set_ylabel("Engagement")
                ax.set_title("Top 10 Cities in India by Political Engagement")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(city_df, width='stretch')

    # --- Tab 3: Party-wise trends with Others + top 3 others ---
    with tab3:
        st.markdown("### Party-wise Political Trends")
        if "Party" not in df_india.columns:
            st.info("No Party information available.")
        else:
            # Aggregate by party
            party_df = (
                df_india.groupby("Party")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            if party_df.empty:
                st.info("No party-level data available.")
            else:
                display_rows = []
                main_parties = ["Congress", "BJP", "JDS", "AAP"]
                for p in main_parties:
                    val = party_df.loc[party_df["Party"] == p, "Engagement"]
                    if not val.empty:
                        label = "INC" if p == "Congress" else p
                        display_rows.append((label, int(val.iloc[0])))

                if not display_rows:
                    st.info("No engagement for main parties yet.")
                else:
                    labels, vals = zip(*display_rows)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(labels, vals, color=["#FF416C", "#FFD93D", "#FF8D29", "#FF4B2B", "#636e72"][: len(labels)])
                    ax.set_xlabel("Party")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Engagement by Party")
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.dataframe(
                        pd.DataFrame({"Party": labels, "Engagement": vals}),
                        width='stretch',
                    )

    # --- Tab 4: Interactions split by Sex & Age group ---
    with tab4:
        st.markdown("### Interaction Split by Sex & Age Groups")
        if "Sex" not in df_india.columns or "AgeGroup" not in df_india.columns:
            st.info("Sex / AgeGroup columns not found in data.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                sex_df = (
                    df_india.groupby("Sex")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if sex_df.empty:
                    st.info("No engagement by Sex available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.pie(
                        sex_df["Engagement"],
                        labels=sex_df["Sex"],
                        autopct="%1.1f%%",
                        startangle=90,
                    )
                    ax.set_title("Engagement by Sex")
                st.pyplot(fig)
            with col2:
                age_df = (
                    df_india.groupby("AgeGroup")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if age_df.empty:
                    st.info("No engagement by AgeGroup available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.bar(age_df["AgeGroup"], age_df["Engagement"], color="#2986cc")
                    ax.set_xlabel("Age Group")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Engagement by Age Group")
                    plt.tight_layout()
                    st.pyplot(fig)

    # --- Tab 5: Karnataka-only politician hourly trends ---
    with tab5:
        st.markdown("### Karnataka — Politician Trends by Hour of Day")
        if "State" not in df.columns or "Politician" not in df.columns:
            st.info("State/Politician columns not available in politics data.")
        else:
            df_ka = df[df["State"] == "Karnataka"].copy()
            if df_ka.empty:
                st.info("No Karnataka-specific political data available.")
            else:
                # Focus on named politicians, exclude generic 'Other'
                df_pol = df_ka[df_ka["Politician"] != "Other"]
                if df_pol.empty:
                    st.info("No specific politician engagement data for Karnataka.")
                else:
                    # Pick top 10 politicians by total engagement (if available)
                    top_pols = (
                        df_pol.groupby("Politician")["Engagement"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(10)
                        .index
                    )
                    hourly_pol = df_pol[df_pol["Politician"].isin(top_pols)].pivot_table(
                        index="Hour", columns="Politician", values="Engagement", aggfunc="sum", fill_value=0
                    )
                    fig, ax = plt.subplots(figsize=(12, 5))
                    for pol in hourly_pol.columns:
                        ax.plot(hourly_pol.index, hourly_pol[pol], marker="o", linewidth=2, label=pol)
                    ax.set_xlabel("Hour of Day")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Karnataka: Politician Engagement by Hour of Day (Top 10)")
                    ax.grid(True, linestyle="--", alpha=0.2)
                    ax.legend()
                    plt.tight_layout()
                    st.pyplot(fig)

def sports_tabs(df):
    """
    Simple Sports dashboard:
    - India level state-wise trend (excluding Karnataka)
    - Top 10 cities in India
    - Sport-wise trend (Cricket/Football/Hockey/Kabaddi/Chess/Others + top 3 others)
    - Interaction split by Sex and Age groups
    - Karnataka-only city-wise hourly trend per sport
    """
    # Split India vs Karnataka: India tabs exclude Karnataka, Karnataka tab is dedicated
    if "State" in df.columns:
        df_india = df[df["State"] != "Karnataka"].copy()
    else:
        df_india = df.copy()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🇮🇳 State Trends", "🏙️ Top 10 Cities", "🏆 Sports", "👥 Demographics", "🕒 Karnataka Cities / Sport / Hour"]
    )

    # --- Tab 1: India level state-wise trend ---
    with tab1:
        st.markdown("### India State-wise Sports Trend")
        if "State" not in df_india.columns:
            st.info("No State information available in sports data.")
        else:
            state_df = (
                df_india.groupby("State")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            if state_df.empty:
                st.info("No engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.barh(state_df["State"], state_df["Engagement"], color="#FF416C")
                ax.set_xlabel("Total Engagement")
                ax.set_ylabel("State")
                ax.set_title("Sports Engagement by State (India)")
                plt.gca().invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(state_df, width='stretch')

    # --- Tab 2: Top 10 cities in India ---
    with tab2:
        st.markdown("### Top 10 Cities in India — Sports Trend")
        if "Location" not in df_india.columns:
            st.info("Location column not available in sports data.")
        else:
            city_df = (
                df_india.groupby("Location")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            if city_df.empty:
                st.info("No city-level engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(city_df["Location"], city_df["Engagement"], color="#FF8D29")
                ax.set_xlabel("City / Location")
                ax.set_ylabel("Engagement")
                ax.set_title("Top 10 Cities in India by Sports Engagement")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(city_df, width='stretch')

    # --- Tab 3: Sport-wise trends with Others + top 3 others ---
    with tab3:
        st.markdown("### Sport-wise Trends")
        if "Sport" not in df_india.columns:
            st.info("No Sport information available.")
        else:
            sport_df = (
                df_india.groupby("Sport")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            if sport_df.empty:
                st.info("No sport-level data available.")
            else:
                main_sports = ["Cricket", "Football", "Hockey", "Kabaddi", "Chess"]
                display_rows = []
                for sname in main_sports:
                    val = sport_df.loc[sport_df["Sport"] == sname, "Engagement"]
                    if not val.empty:
                        display_rows.append((sname, int(val.iloc[0])))

                if not display_rows:
                    st.info("No engagement for main sports yet.")
                else:
                    labels, vals = zip(*display_rows)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(
                        labels,
                        vals,
                        color=["#FF416C", "#FFD93D", "#FF8D29", "#FF4B2B", "#F7B733", "#636e72"][: len(labels)],
                    )
                    ax.set_xlabel("Sport")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Engagement by Sport")
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.dataframe(
                        pd.DataFrame({"Sport": labels, "Engagement": vals}),
                        width='stretch',
                    )

    # --- Tab 4: Interactions split by Sex & Age group ---
    with tab4:
        st.markdown("### Interaction Split by Sex & Age Groups")
        if "Sex" not in df_india.columns or "AgeGroup" not in df_india.columns:
            st.info("Sex / AgeGroup columns not found in data.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                sex_df = (
                    df_india.groupby("Sex")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if sex_df.empty:
                    st.info("No engagement by Sex available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.pie(
                        sex_df["Engagement"],
                        labels=sex_df["Sex"],
                        autopct="%1.1f%%",
                        startangle=90,
                    )
                    ax.set_title("Engagement by Sex")
                    st.pyplot(fig)
            with col2:
                age_df = (
                    df_india.groupby("AgeGroup")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if age_df.empty:
                    st.info("No engagement by AgeGroup available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.bar(age_df["AgeGroup"], age_df["Engagement"], color="#2986cc")
                    ax.set_xlabel("Age Group")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Engagement by Age Group")
                    plt.tight_layout()
                    st.pyplot(fig)

    # --- Tab 5: Karnataka-only city-wise hourly per sport ---
    with tab5:
        st.markdown("### Karnataka — City-wise Hourly Sports Trends")
        if "State" not in df.columns or "Location" not in df.columns or "Sport" not in df.columns:
            st.info("State/Location/Sport columns not available in sports data.")
        else:
            df_ka = df[df["State"] == "Karnataka"].copy()
            if df_ka.empty:
                st.info("No Karnataka-specific sports data available.")
            else:
                sports_available = sorted(df_ka["Sport"].dropna().unique())
                if not sports_available:
                    st.info("No sport categories found for Karnataka.")
                else:
                    selected_sport = st.selectbox("Select Sport", sports_available, key="sport_hourly_ka")
                    df_sport = df_ka[df_ka["Sport"] == selected_sport]
                    if df_sport.empty:
                        st.info(f"No data for {selected_sport} in Karnataka.")
                    else:
                        hourly_city = df_sport.pivot_table(
                            index="Hour", columns="Location", values="Engagement", aggfunc="sum", fill_value=0
                        )
                        if hourly_city.empty:
                            st.info(f"No hourly city-wise data for {selected_sport} in Karnataka.")
                        else:
                            # Top 10 cities by engagement for this sport
                            top_cities = (
                                df_sport.groupby("Location")["Engagement"]
                                .sum()
                                .sort_values(ascending=False)
                                .head(10)
                                .index
                            )
                            fig, ax = plt.subplots(figsize=(12, 5))
                            for city in hourly_city.columns:
                                if city in top_cities:
                                    ax.plot(hourly_city.index, hourly_city[city], marker="o", linewidth=2, label=city)
                            ax.set_xlabel("Hour of Day")
                            ax.set_ylabel("Engagement")
                            ax.set_title(f"Karnataka: City-wise Hourly Engagement for {selected_sport}")
                            ax.grid(True, linestyle="--", alpha=0.2)
                            ax.legend()
                            plt.tight_layout()
                            st.pyplot(fig)

def cinema_tabs(df):
    """
    Cinema dashboard:
    - India level state-wise movie discussion trend (excluding Karnataka)
    - Top 10 movies under discussion
    - Industry-wise trends (Hollywood, Bollywood, Sandalwood, Tollywood, Mollywood)
    - Interaction split by Sex and Age groups
    - Karnataka-only movie vs hour-of-day trends
    """
    # Split India vs Karnataka: India tabs exclude Karnataka, Karnataka tab is dedicated
    if "State" in df.columns:
        df_india = df[df["State"] != "Karnataka"].copy()
    else:
        df_india = df.copy()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🇮🇳 State Trends", "🎬 Top 10 Movies", "🏷️ Industries", "👥 Demographics", "🕒 Karnataka Movies / Hour"]
    )

    # --- Tab 1: India level state-wise movie trend ---
    with tab1:
        st.markdown("### India State-wise Cinema Discussion Trend")
        if "State" not in df_india.columns:
            st.info("No State information available in cinema data.")
        else:
            state_df = (
                df_india.groupby("State")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            if state_df.empty:
                st.info("No engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.barh(state_df["State"], state_df["Engagement"], color="#FF416C")
                ax.set_xlabel("Total Engagement")
                ax.set_ylabel("State")
                ax.set_title("Cinema Engagement by State (India)")
                plt.gca().invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(state_df, width='stretch')

    # --- Tab 2: Top 10 movies under discussion ---
    with tab2:
        st.markdown("### Top 10 Movies Under Discussion")
        if "Movie" not in df.columns:
            st.info("No Movie information available in cinema data.")
        else:
            movies_df = (
                df.groupby("Movie")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            if movies_df.empty:
                st.info("No movie-level engagement data available.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(movies_df["Movie"], movies_df["Engagement"], color="#FF8D29")
                ax.set_xlabel("Movie")
                ax.set_ylabel("Engagement")
                ax.set_title("Top 10 Movies by Engagement")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(movies_df, width='stretch')

    # --- Tab 3: Industry-wise trends ---
    with tab3:
        st.markdown("### Industry-wise Cinema Trends")
        if "Industry" not in df_india.columns:
            st.info("No Industry information available in cinema data.")
        else:
            ind_df = (
                df_india.groupby("Industry")["Engagement"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            # Keep only configured industries; drop Others if present
            focus_inds = ["Hollywood", "Bollywood", "Sandalwood", "Tollywood", "Mollywood"]
            ind_df = ind_df[ind_df["Industry"].isin(focus_inds)]
            if ind_df.empty:
                st.info("No engagement for configured cinema industries yet.")
            else:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(ind_df["Industry"], ind_df["Engagement"], color="#27ae60")
                ax.set_xlabel("Industry")
                ax.set_ylabel("Engagement")
                ax.set_title("Engagement by Cinema Industry")
                plt.tight_layout()
                st.pyplot(fig)
                st.dataframe(ind_df, width='stretch')

    # --- Tab 4: Interactions split by Sex & Age group ---
    with tab4:
        st.markdown("### Interaction Split by Sex & Age Groups")
        if "Sex" not in df_india.columns or "AgeGroup" not in df_india.columns:
            st.info("Sex / AgeGroup columns not found in data.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                sex_df = (
                    df_india.groupby("Sex")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if sex_df.empty:
                    st.info("No engagement by Sex available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.pie(
                        sex_df["Engagement"],
                        labels=sex_df["Sex"],
                        autopct="%1.1f%%",
                        startangle=90,
                    )
                    ax.set_title("Engagement by Sex")
                    st.pyplot(fig)
            with col2:
                age_df = (
                    df_india.groupby("AgeGroup")["Engagement"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                if age_df.empty:
                    st.info("No engagement by AgeGroup available.")
                else:
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.bar(age_df["AgeGroup"], age_df["Engagement"], color="#2986cc")
                    ax.set_xlabel("Age Group")
                    ax.set_ylabel("Engagement")
                    ax.set_title("Engagement by Age Group")
                    plt.tight_layout()
                    st.pyplot(fig)

    # --- Tab 5: Karnataka-only movie vs hour-of-day ---
    with tab5:
        st.markdown("### Karnataka — Movie Discussion by Hour of Day")
        if "State" not in df.columns or "Movie" not in df.columns:
            st.info("State/Movie columns not available in cinema data.")
        else:
            df_ka = df[df["State"] == "Karnataka"].copy()
            if df_ka.empty:
                st.info("No Karnataka-specific cinema data available.")
            else:
                if df_ka["Movie"].nunique() == 0:
                    st.info("No movie information for Karnataka.")
                else:
                    # Top movies by engagement in Karnataka
                    top_movies = (
                        df_ka.groupby("Movie")["Engagement"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(10)
                        .index
                    )
                    hourly_movie = df_ka[df_ka["Movie"].isin(top_movies)].pivot_table(
                        index="Hour", columns="Movie", values="Engagement", aggfunc="sum", fill_value=0
                    )
                    if hourly_movie.empty:
                        st.info("No hourly movie-wise data for Karnataka.")
                    else:
                        fig, ax = plt.subplots(figsize=(12, 5))
                        for mv in hourly_movie.columns:
                            ax.plot(hourly_movie.index, hourly_movie[mv], marker="o", linewidth=2, label=mv)
                        ax.set_xlabel("Hour of Day")
                        ax.set_ylabel("Engagement (Tweets)")
                        ax.set_title("Karnataka: Movie Discussions by Hour of Day (Top 10 Movies)")
                        ax.grid(True, linestyle="--", alpha=0.2)
                        ax.legend()
                        plt.tight_layout()
                        st.pyplot(fig)

def render_demographics_persona(df, age_field='Age', gender_field='Gender', location_field='Location', state_field='State', device_field='Device', interest_fields=('LikesTravel','LikesFootball')):
    st.markdown("### 👥 Audience Persona Snapshot")
    # Guard: Check for columns first
    loc_col_exist = location_field in df.columns
    state_col_exist = state_field in df.columns
    age_col_exist = age_field in df.columns
    gender_col_exist = gender_field in df.columns
    if not loc_col_exist and not state_col_exist:
        st.info('No Location/State breakdown available for demographic persona.')
        return
    # Pie chart (Age) for India vs Karnataka
    for group, val in [("India", "India"), ("Karnataka", "Karnataka")]:
        if group=="India" and not loc_col_exist:
            continue
        if group=="Karnataka" and not state_col_exist:
            continue
        sub = df[df[location_field]==val] if group=="India" else df[df[state_field]==val]
        if age_col_exist and not sub.empty and age_field in sub.columns:
            st.markdown(f"#### Age Distribution — {group}")
            ages = sub[age_field].value_counts().sort_index()
            fig, ax = plt.subplots()
            ax.pie(ages.values, labels=ages.index, autopct='%1.1f%%',startangle=90)
            ax.set_title(f"{group} Audience by Age", fontsize=10)
            st.pyplot(fig)
    # Pie chart (Gender)
    for group, val in [("India", "India"), ("Karnataka", "Karnataka")]:
        if group=="India" and not loc_col_exist:
            continue
        if group=="Karnataka" and not state_col_exist:
            continue
        sub = df[df[location_field]==val] if group=="India" else df[df[state_field]==val]
        if gender_col_exist and not sub.empty and gender_field in sub.columns:
            st.markdown(f"#### Gender Distribution — {group}")
            genders = sub[gender_field].value_counts().sort_index()
            fig, ax = plt.subplots()
            ax.pie(genders.values, labels=genders.index, autopct='%1.1f%%',startangle=90)
            ax.set_title(f"{group} Audience by Gender", fontsize=10)
            st.pyplot(fig)
    # Bar chart: Top 5 locations
    if loc_col_exist:
        loc_ct = df[location_field].value_counts().head(5)
        st.markdown('#### Top 5 Locations (India)')
        fig, ax = plt.subplots()
        colors = ['#FFD93D' if k=="Karnataka" else '#636e72' for k in loc_ct.index]
        ax.bar(loc_ct.index, loc_ct.values, color=colors)
        ax.set_ylabel('Count')
        ax.set_title('Top Locations — Highlight: Karnataka')
        st.pyplot(fig)
    # Bar chart: Devices if available
    if device_field in df.columns:
        dev_ct = df[device_field].value_counts().head(5)
        st.markdown('#### Top 5 Devices (India)')
        fig, ax = plt.subplots()
        ax.bar(dev_ct.index, dev_ct.values, color='#636e72')
        ax.set_ylabel('Count')
        ax.set_title('Top 5 Devices Used (India)')
        st.pyplot(fig)
    # Interest overlap (stubbed logic)
    if all(f in df.columns for f in interest_fields):
        st.markdown('#### Interest Overlap: Football + Travel')
        both = df[df[interest_fields[0]] & df[interest_fields[1]]]
        only_one = df[df[interest_fields[0]] ^ df[interest_fields[1]]]
        fig, ax = plt.subplots()
        ax.bar(['Both', 'Only One'], [len(both), len(only_one)], color=['#27ae60','#FFD93D'])
        ax.set_ylabel('User Count')
        ax.set_title('Audience with Overlapping Interests')
        st.pyplot(fig)
    st.caption("Persona charts focus on India/Karnataka audience. All demos use latest best-practice Streamlit visual style.")

def render_quarterly_audit_report(df, topic_col='Topic', roi_col='ROI', hours_col='Hours_Production', views_col='Views', evergreen_col='Evergreen', fail_col='Failure_Reason', title='Quarterly Content Audit Report'):
    st.markdown(f'### 📈 {title}')
    needed = [topic_col, roi_col, hours_col, views_col, evergreen_col, fail_col]
    if any(c not in df.columns for c in needed) or df.empty:
        st.info('Not enough quarterly audit data.')
        return
    df_sorted = df.sort_values(roi_col, ascending=False).copy()
    st.dataframe(df_sorted, use_container_width=True)
    evergreen = df[df[evergreen_col]==True]
    fails = df[df[fail_col]!=''].sort_values(roi_col).head(5)
    if not evergreen.empty:
        st.markdown('#### Evergreen Winners')
        st.dataframe(evergreen[[topic_col,views_col,hours_col]], use_container_width=True)
    if not fails.empty:
        st.markdown('#### Failure Analysis')
        st.dataframe(fails[[topic_col,fail_col]], use_container_width=True)
    st.caption('Review winners (ROI>avg, evergreen) and failures for quarterly strategy reset.')
