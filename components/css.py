def inject_main_css():
    """Custom CSS themed to match the PrayanaAI travel aesthetic."""
    return '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    :root { color-scheme: light; }
    /* Core palette inspired by prayanaai.com */
    /* Primary teal: #00B7C2, Deep navy: #06324F, Warm accent: #FFB15E, Soft background: #F5FBFF */

    input, textarea, select { color: #163047 !important; background: #ffffff !important; }
    body, .stApp { 
        background: radial-gradient(circle at top left, #f5fbff 0, #e9f5ff 40%, #fefefe 100%);
        color: #163047;
    }
    .main { background: transparent; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #00b7c2, #ffb15e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        letter-spacing: -1px;
    }
    .sub-header {
        text-align: center;
        color: #60718a;
        font-size: 1.15rem;
        margin-bottom: 2.2rem;
        font-weight: 500;
    }
    .insight-box {
        background: rgba(255,255,255,0.98);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 14px;
        box-shadow: 0 18px 45px -20px rgba(6,50,79,0.45);
        margin: 1.6rem 0;
        border: 1.5px solid rgba(0,183,194,0.18);
    }
    .insight-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        color: #06324f;
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    .insight-item {
        font-size: 1.08rem;
        line-height: 1.7;
        padding: 0.95rem 1rem;
        margin: 0.4rem 0;
        border-radius: 6.5px;
        background: linear-gradient(135deg, #f3fcff, #fff7ec);
        border-left: 3.5px solid #00b7c2;
        color: #163047;
        transition: background 0.2s;
    }
    .insight-item:hover {
        background: #e3edfa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.6rem;
        background: rgba(255,255,255,0.95);
        padding: 0.5rem;
        border-radius: 13px;
        box-shadow: 0 10px 30px -18px rgba(6,50,79,0.65);
        border: 1.2px solid rgba(0,183,194,0.22);
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        padding: 0 1.6rem;
        font-size: 1.02rem;
        font-weight: 600;
        background: none;
        border-radius: 8px;
        color: #32516b;
        border: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #f0fbff;
        color: #00b7c2;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #00b7c2, #ffb15e); /* travel gradient */
        color: #fff !important;
        box-shadow: 0 12px 25px -14px rgba(6,50,79,0.9);
        font-weight:800;
    }
    .metric-card {
        background: rgba(255,255,255,0.96);
        padding: 1.3rem 1.5rem;
        border-radius: 14px;
        border: 1.3px solid #dfecfc;
        text-align: center;
        box-shadow: 0 2.5px 10px -3px #7891c510;
        min-height: 165px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00b7c2;
        margin-bottom: 0.6rem;
    }
    .metric-label {
        font-size: 1rem;
        color: #7a87a1;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    [data-testid="stSidebar"] {
        background: #fff;
        border-right: 1.3px solid #e0e6f1;
    }
    [data-testid="stSidebar"] .stSelectbox {
        background: #f7f8fa;
        border-radius: 9px;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #2364aa;
    }
    .stButton > button {
        background: linear-gradient(120deg, #00b7c2, #ffb15e);
        color: white;
        border: none;
        border-radius: 11px;
        padding: 0.68rem 2.1rem;
        font-weight: 600;
        font-size: 1.02rem;
        transition: box-shadow 0.18s, background 0.18s;
        box-shadow: 0 14px 30px -15px rgba(6,50,79,0.85);
    }
    .stButton > button:hover {
        background: linear-gradient(120deg, #0097a5, #ff9b35);
        box-shadow: 0 18px 38px -16px rgba(6,50,79,0.95);
    }
    .dataframe {
        background: rgba(255,255,255,0.98);
        border-radius: 8.5px;
        border: 1.3px solid rgba(0,183,194,0.18);
    }
    .stDateInput > div > div { background: #fff; border: 1.2px solid #dfecfc; border-radius: 8.5px; }
    .stSlider > div > div > div { background: linear-gradient(90deg, #00b7c2, #ffb15e); }
    h1, h2, h3 {
        color: #06324f;
    }
    h2 {
        font-weight: 700;
        font-size: 1.7rem;
        margin-top: 2rem;
        margin-bottom: 0.95rem;
    }
    h3 {
        font-weight: 600;
        font-size: 1.33rem;
        margin-bottom: 1rem;
    }
    .stInfo {
        background: #f3fcff;
        border-left: 4px solid #00b7c2;
        border-radius: 9px;
        color: #06324f;
    }
    .stSuccess {
        background: #f6fff7;
        border-left: 4px solid #41b555;
        border-radius: 9px;
        color: #238342;
    }
    .stWarning {
        background: #fff9ed;
        border-left: 4px solid #ffb15e;
        border-radius: 9px;
        color: #a67713;
    }
    hr { margin: 2rem 0; border: none; height: 1px; background: linear-gradient(to right, transparent, #c2e7ff, transparent); }
    .stSpinner > div { border-top-color: #00b7c2 !important; }
</style>
'''
