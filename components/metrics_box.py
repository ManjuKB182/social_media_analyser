import streamlit as st

def render_metrics(df, insights_summary=None):
    if df is not None and not df.empty:
        col1, col2, col3 = st.columns(3)
        # Compute health (example): green if > avg, red otherwise
        avg_engagement = df['Engagement'].mean() if len(df) > 0 else 0
        total_engagement = df['Engagement'].sum()
        min_hour, max_hour = df['Hour'].min(), df['Hour'].max()
        colors = {True: '#27ae60', False: '#e74c3c'}
        actual_vs_avg = total_engagement > (avg_engagement * len(df))
        with col1:
            st.markdown(f"""
                <div class="metric-card" style="border-left:6px solid {colors[len(df) > 1000]};">
                    <div class="metric-value">{len(df):,}</div>
                    <div class="metric-label">📊 Total Records</div>
                    <div class="metric-summary">{insights_summary.get('total_records') if insights_summary else ''}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card" style="border-left:6px solid {colors[actual_vs_avg]};">
                    <div class="metric-value">{total_engagement:,}</div>
                    <div class="metric-label">💬 Total Engagement</div>
                    <div class="metric-summary">{insights_summary.get('engagement') if insights_summary else ''}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card" style="border-left:6px solid #FFD93D;">
                    <div class="metric-value">{min_hour}:00 - {max_hour}:00</div>
                    <div class="metric-label">⏰ Time Range</div>
                    <div class="metric-summary">{insights_summary.get('timerange') if insights_summary else ''}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
