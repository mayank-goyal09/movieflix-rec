import requests
import streamlit as st
import random
from typing import Optional, Dict, Any, List, Tuple

# =============================
# CONFIG
# =============================
API_BASE = "https://movieflix-rec.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP = "https://image.tmdb.org/t/p/original"

st.set_page_config(
    page_title="🎬 MovieFlix | Your Movie Universe",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# NETFLIX-STYLE CSS
# =============================
st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --netflix-red: #E50914;
        --netflix-red-hover: #F40612;
        --dark-bg: #141414;
        --card-bg: #181818;
        --card-hover: #252525;
        --text-primary: #FFFFFF;
        --text-secondary: #B3B3B3;
        --text-muted: #757575;
        --accent-gold: #E5A00D;
        --gradient-red: linear-gradient(135deg, #E50914 0%, #B20710 100%);
        --gradient-dark: linear-gradient(180deg, transparent 0%, rgba(20,20,20,0.8) 50%, #141414 100%);
        --shadow-glow: 0 0 40px rgba(229, 9, 20, 0.3);
        --shadow-card: 0 8px 32px rgba(0,0,0,0.6);
    }
    
    /* ===== GLOBAL STYLES ===== */
    .stApp {
        background: var(--dark-bg) !important;
    }
    
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
        padding-left: 4% !important;
        padding-right: 4% !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ===== CUSTOM SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--dark-bg);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--netflix-red);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--netflix-red-hover);
    }
    
    /* ===== NAVBAR ===== */
    .netflix-navbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        padding: 15px 4%;
        background: linear-gradient(180deg, rgba(20,20,20,0.95) 0%, transparent 100%);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    .netflix-logo {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 2.8rem !important;
        color: var(--netflix-red) !important;
        letter-spacing: 4px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 0 !important;
        animation: logoGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes logoGlow {
        from { text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
        to { text-shadow: 2px 2px 20px rgba(229, 9, 20, 0.5), 2px 2px 4px rgba(0,0,0,0.5); }
    }
    
    /* ===== HERO SECTION ===== */
    .hero-container {
        position: relative;
        width: 100%;
        height: 70vh;
        min-height: 500px;
        margin-bottom: 30px;
        border-radius: 0 0 20px 20px;
        overflow: hidden;
    }
    
    .hero-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.5);
    }
    
    .hero-gradient {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, rgba(20,20,20,0.9) 0%, rgba(20,20,20,0.4) 50%, transparent 100%),
                    linear-gradient(180deg, transparent 60%, #141414 100%);
    }
    
    .hero-content {
        position: absolute;
        bottom: 15%;
        left: 4%;
        max-width: 45%;
        z-index: 10;
    }
    
    .hero-title {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 4rem !important;
        color: white !important;
        line-height: 1 !important;
        margin-bottom: 15px !important;
        text-shadow: 2px 4px 10px rgba(0,0,0,0.8);
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-info {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;
    }
    
    .hero-rating {
        background: var(--accent-gold);
        color: black !important;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    .hero-year, .hero-genre {
        color: var(--text-secondary) !important;
        font-size: 1rem;
    }
    
    .hero-overview {
        color: var(--text-secondary) !important;
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        margin-bottom: 25px !important;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin: 40px 0 20px 0 !important;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .section-title::before {
        content: '';
        width: 4px;
        height: 28px;
        background: var(--netflix-red);
        border-radius: 2px;
    }
    
    /* ===== MOVIE CAROUSEL ===== */
    .movie-carousel {
        display: flex;
        gap: 12px;
        overflow-x: auto;
        scroll-behavior: smooth;
        padding: 15px 0;
        -webkit-overflow-scrolling: touch;
        scroll-snap-type: x mandatory;
    }
    
    .movie-carousel::-webkit-scrollbar {
        height: 6px;
    }
    
    .movie-card {
        flex: 0 0 180px;
        border-radius: 8px;
        overflow: hidden;
        background: var(--card-bg);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        scroll-snap-align: start;
        position: relative;
    }
    
    .movie-card:hover {
        transform: scale(1.08) translateY(-10px);
        z-index: 100;
        box-shadow: var(--shadow-card), var(--shadow-glow);
    }
    
    .movie-poster {
        width: 100%;
        aspect-ratio: 2/3;
        object-fit: cover;
        transition: filter 0.3s ease;
    }
    
    .movie-card:hover .movie-poster {
        filter: brightness(0.7);
    }
    
    .movie-info {
        padding: 12px;
        background: linear-gradient(180deg, transparent 0%, var(--card-bg) 30%);
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
    }
    
    .movie-card:hover .movie-info {
        opacity: 1;
        transform: translateY(0);
    }
    
    .movie-title-card {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: white !important;
        margin: 0 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .movie-meta {
        font-size: 0.75rem;
        color: var(--text-muted) !important;
        margin-top: 4px;
    }
    
    /* ===== PLAY BUTTON OVERLAY ===== */
    .play-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0);
        width: 50px;
        height: 50px;
        background: rgba(229, 9, 20, 0.9);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .movie-card:hover .play-overlay {
        transform: translate(-50%, -50%) scale(1);
    }
    
    .play-icon {
        font-size: 20px;
        margin-left: 3px;
    }
    
    /* ===== SEARCH BAR ===== */
    .stTextInput > div > div > input {
        background: rgba(45,45,45,0.9) !important;
        border: 2px solid transparent !important;
        border-radius: 30px !important;
        padding: 15px 25px !important;
        color: white !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--netflix-red) !important;
        box-shadow: 0 0 20px rgba(229, 9, 20, 0.3) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: var(--gradient-red) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* Secondary Button */
    .secondary-btn > button {
        background: rgba(109, 109, 110, 0.7) !important;
    }
    
    .secondary-btn > button:hover {
        background: rgba(109, 109, 110, 0.9) !important;
        box-shadow: none !important;
    }
    
    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background: rgba(45,45,45,0.9) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div > div {
        color: white !important;
    }
    
    /* ===== DETAIL PAGE ===== */
    .detail-container {
        margin-top: -50px;
    }
    
    .detail-backdrop-container {
        position: relative;
        width: 100%;
        height: 60vh;
        overflow: hidden;
    }
    
    .detail-backdrop {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.4);
    }
    
    .detail-backdrop-gradient {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, transparent 0%, #141414 95%);
    }
    
    .detail-content {
        position: relative;
        margin-top: -200px;
        z-index: 10;
        display: flex;
        gap: 40px;
        padding: 0 4%;
    }
    
    .detail-poster-container {
        flex: 0 0 280px;
    }
    
    .detail-poster {
        width: 100%;
        border-radius: 12px;
        box-shadow: var(--shadow-card);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .detail-info {
        flex: 1;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    .detail-title {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 3.5rem !important;
        color: white !important;
        margin-bottom: 15px !important;
        line-height: 1.1 !important;
    }
    
    .detail-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 25px;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--text-secondary) !important;
        font-size: 1rem;
    }
    
    .meta-icon {
        font-size: 1.2rem;
    }
    
    .genre-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 25px;
    }
    
    .genre-tag {
        background: rgba(229, 9, 20, 0.2);
        border: 1px solid var(--netflix-red);
        color: var(--netflix-red) !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .genre-tag:hover {
        background: var(--netflix-red);
        color: white !important;
    }
    
    .detail-overview {
        font-size: 1.1rem !important;
        color: var(--text-secondary) !important;
        line-height: 1.7 !important;
        margin-bottom: 30px !important;
    }
    
    /* ===== LOADING ANIMATION ===== */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(229, 9, 20, 0.2);
        border-top-color: var(--netflix-red);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* ===== NO POSTER PLACEHOLDER ===== */
    .no-poster {
        width: 100%;
        aspect-ratio: 2/3;
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--text-muted) !important;
        font-size: 2rem;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-container {
            height: 50vh;
            min-height: 350px;
        }
        .hero-content {
            max-width: 90%;
        }
        .hero-title {
            font-size: 2.5rem !important;
        }
        .movie-card {
            flex: 0 0 140px;
        }
        .detail-content {
            flex-direction: column;
            align-items: center;
        }
        .detail-poster-container {
            flex: 0 0 auto;
            max-width: 250px;
        }
        .detail-title {
            font-size: 2.5rem !important;
            text-align: center;
        }
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent) !important;
        margin: 30px 0 !important;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* ===== CATEGORY PILLS ===== */
    .category-pills {
        display: flex;
        gap: 12px;
        overflow-x: auto;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    
    .category-pill {
        background: rgba(45,45,45,0.8);
        color: white !important;
        padding: 10px 24px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .category-pill:hover, .category-pill.active {
        background: var(--netflix-red);
        border-color: var(--netflix-red);
        transform: scale(1.05);
    }
    
    /* ===== INFO CARDS ===== */
    .info-card {
        background: rgba(30,30,30,0.8);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 40px 0;
        color: var(--text-muted) !important;
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 60px;
    }
    
    .footer a {
        color: var(--netflix-red) !important;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "category" not in st.session_state:
    st.session_state.category = "trending"

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=60)
def api_get_json(path: str, params: Optional[dict] = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def create_movie_carousel(movies, section_id):
    """Create a horizontal scrollable movie carousel"""
    if not movies:
        return
    
    carousel_html = f'<div class="movie-carousel" id="{section_id}">'
    
    for i, movie in enumerate(movies):
        tmdb_id = movie.get("tmdb_id")
        title = movie.get("title", "Untitled")
        poster = movie.get("poster_url")
        year = (movie.get("release_date") or "")[:4]
        
        poster_html = f'<img class="movie-poster" src="{poster}" alt="{title}">' if poster else '<div class="no-poster">🎬</div>'
        
        carousel_html += f'''
        <div class="movie-card" onclick="window.location.href='?view=details&id={tmdb_id}'">
            {poster_html}
            <div class="play-overlay">
                <span class="play-icon">▶</span>
            </div>
            <div class="movie-info">
                <p class="movie-title-card">{title}</p>
                <p class="movie-meta">{year}</p>
            </div>
        </div>
        '''
    
    carousel_html += '</div>'
    st.markdown(carousel_html, unsafe_allow_html=True)
    
    # Render button row for navigation
    cols = st.columns(len(movies[:12]))
    for i, movie in enumerate(movies[:12]):
        with cols[i]:
            if st.button("▶", key=f"{section_id}_btn_{i}_{movie.get('tmdb_id')}"):
                goto_details(movie.get("tmdb_id"))


def render_movie_grid(movies, key_prefix, cols_per_row=6):
    """Render movies in a grid with clickable cards"""
    if not movies:
        st.info("No movies to display.")
        return
    
    for row_start in range(0, len(movies), cols_per_row):
        row_movies = movies[row_start:row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        
        for i, movie in enumerate(row_movies):
            with cols[i]:
                tmdb_id = movie.get("tmdb_id")
                title = movie.get("title", "Untitled")
                poster = movie.get("poster_url")
                year = (movie.get("release_date") or "")[:4]
                
                # Card HTML
                card_html = f'''
                <div style="
                    background: #181818;
                    border-radius: 8px;
                    overflow: hidden;
                    transition: all 0.3s ease;
                    cursor: pointer;
                ">
                '''
                
                if poster:
                    card_html += f'<img src="{poster}" style="width:100%; aspect-ratio:2/3; object-fit:cover;">'
                else:
                    card_html += '<div style="width:100%; aspect-ratio:2/3; background:#2a2a2a; display:flex; align-items:center; justify-content:center; font-size:2rem;">🎬</div>'
                
                card_html += f'''
                    <div style="padding:10px;">
                        <p style="font-size:0.85rem; font-weight:600; color:white; margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{title}</p>
                        <p style="font-size:0.75rem; color:#757575; margin:4px 0 0 0;">{year}</p>
                    </div>
                </div>
                '''
                st.markdown(card_html, unsafe_allow_html=True)
                
                if st.button("Watch", key=f"{key_prefix}_{row_start}_{i}_{tmdb_id}", use_container_width=True):
                    goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    """Convert TF-IDF items to card format"""
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
                "release_date": tmdb.get("release_date", "")
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """Parse TMDB search results to card format"""
    keyword_l = keyword.strip().lower()
    
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []
    
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items
    
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))
    
    cards = [{
        "tmdb_id": x["tmdb_id"],
        "title": x["title"],
        "poster_url": x["poster_url"],
        "release_date": x.get("release_date", "")
    } for x in final_list[:limit]]
    
    return suggestions, cards


# =============================
# NAVBAR
# =============================
st.markdown("""
<div class="netflix-navbar">
    <h1 class="netflix-logo">MOVIEFLIX</h1>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    
    # Search Bar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        typed = st.text_input(
            "",
            placeholder="🔍 Search movies, shows, genres...",
            label_visibility="collapsed"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # If searching
    if typed.strip():
        if len(typed.strip()) < 2:
            st.info("Type at least 2 characters to search...")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
            
            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)
                
                if suggestions:
                    st.markdown(f'<div class="section-title">🔍 Search Results for "{typed}"</div>', unsafe_allow_html=True)
                    
                    # Dropdown for quick select
                    labels = ["-- Quick Select --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("", labels, index=0, label_visibility="collapsed")
                    
                    if selected != "-- Quick Select --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                    
                    render_movie_grid(cards, key_prefix="search_results", cols_per_row=6)
                else:
                    st.info("No results found. Try another search term.")
        st.stop()
    
    # Category Pills
    categories = ["trending", "popular", "top_rated", "now_playing", "upcoming"]
    category_labels = {
        "trending": "🔥 Trending",
        "popular": "⭐ Popular",
        "top_rated": "🏆 Top Rated",
        "now_playing": "🎬 Now Playing",
        "upcoming": "📅 Coming Soon"
    }
    
    # Category selector
    cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        with cols[i]:
            if st.button(category_labels[cat], key=f"cat_{cat}", use_container_width=True):
                st.session_state.category = cat
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hero Section - Featured Movie
    hero_data, err = api_get_json("/home", params={"category": "popular", "limit": 5})
    
    if hero_data and len(hero_data) > 0:
        featured = random.choice(hero_data[:3])
        featured_id = featured.get("tmdb_id")
        
        # Fetch detailed info for hero
        detail_data, _ = api_get_json(f"/movie/id/{featured_id}")
        
        if detail_data:
            backdrop = detail_data.get("backdrop_url") or featured.get("poster_url")
            title = detail_data.get("title", "Featured Movie")
            overview = detail_data.get("overview", "")[:200] + "..." if detail_data.get("overview") else ""
            genres = ", ".join([g["name"] for g in detail_data.get("genres", [])[:3]])
            year = (detail_data.get("release_date") or "")[:4]
            rating = detail_data.get("vote_average", 0)
            
            hero_html = f'''
            <div class="hero-container">
                <img class="hero-backdrop" src="{backdrop}" alt="{title}">
                <div class="hero-gradient"></div>
                <div class="hero-content">
                    <h1 class="hero-title">{title}</h1>
                    <div class="hero-info">
                        <span class="hero-rating">⭐ {rating:.1f}</span>
                        <span class="hero-year">{year}</span>
                        <span class="hero-genre">{genres}</span>
                    </div>
                    <p class="hero-overview">{overview}</p>
                </div>
            </div>
            '''
            st.markdown(hero_html, unsafe_allow_html=True)
            
            # Hero buttons
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("▶ Watch Now", key="hero_watch"):
                    goto_details(featured_id)
            with col2:
                st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                if st.button("ℹ️ More Info", key="hero_info"):
                    goto_details(featured_id)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Content Sections
    sections = [
        ("trending", "🔥 Trending Now"),
        ("popular", "⭐ Popular on MovieFlix"),
        ("top_rated", "🏆 Top Rated"),
        ("now_playing", "🎬 Now Playing"),
        ("upcoming", "📅 Coming Soon"),
    ]
    
    for section_key, section_title in sections:
        st.markdown(f'<div class="section-title">{section_title}</div>', unsafe_allow_html=True)
        
        section_data, err = api_get_json("/home", params={"category": section_key, "limit": 12})
        
        if section_data:
            render_movie_grid(section_data, key_prefix=f"section_{section_key}", cols_per_row=6)
        else:
            st.info(f"Could not load {section_title.lower()}")
        
        st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()
    
    # Back button
    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="back_btn"):
            goto_home()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fetch movie details
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    
    if err or not data:
        st.error(f"Could not load movie details: {err or 'Unknown error'}")
        st.stop()
    
    # Backdrop
    backdrop = data.get("backdrop_url")
    if backdrop:
        st.markdown(f'''
        <div class="detail-backdrop-container">
            <img class="detail-backdrop" src="{backdrop}">
            <div class="detail-backdrop-gradient"></div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        poster = data.get("poster_url")
        if poster:
            st.markdown(f'<img class="detail-poster" src="{poster}" alt="{data.get("title", "Movie")}">', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-poster" style="height:400px; border-radius:12px;">🎬</div>', unsafe_allow_html=True)
    
    with col2:
        # Title
        st.markdown(f'<h1 class="detail-title">{data.get("title", "Unknown Title")}</h1>', unsafe_allow_html=True)
        
        # Meta info
        release = data.get("release_date") or "N/A"
        year = release[:4] if release != "N/A" else "N/A"
        rating = data.get("vote_average", 0)
        runtime = data.get("runtime", 0)
        
        meta_html = f'''
        <div class="detail-meta">
            <div class="meta-item"><span class="meta-icon">📅</span> {year}</div>
            <div class="meta-item"><span class="meta-icon">⭐</span> {rating:.1f}/10</div>
            <div class="meta-item"><span class="meta-icon">⏱️</span> {runtime} min</div>
        </div>
        '''
        st.markdown(meta_html, unsafe_allow_html=True)
        
        # Genres
        genres = data.get("genres", [])
        if genres:
            genre_html = '<div class="genre-tags">'
            for g in genres:
                genre_html += f'<span class="genre-tag">{g["name"]}</span>'
            genre_html += '</div>'
            st.markdown(genre_html, unsafe_allow_html=True)
        
        # Overview
        overview = data.get("overview") or "No overview available."
        st.markdown(f'<p class="detail-overview">{overview}</p>', unsafe_allow_html=True)
        
        # Action buttons
        col_a, col_b, col_c = st.columns([1, 1, 3])
        with col_a:
            st.button("▶ Play", key="play_btn", use_container_width=True)
        with col_b:
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            st.button("+ My List", key="mylist_btn", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Recommendations
    title = (data.get("title") or "").strip()
    
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12}
        )
        
        if not err2 and bundle:
            # Similar Movies (TF-IDF)
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            if tfidf_cards:
                st.markdown('<div class="section-title">🎯 Because You Watched This</div>', unsafe_allow_html=True)
                render_movie_grid(tfidf_cards, key_prefix="detail_tfidf", cols_per_row=6)
            
            # Genre recommendations
            genre_cards = bundle.get("genre_recommendations", [])
            if genre_cards:
                st.markdown('<div class="section-title">🎭 More Like This</div>', unsafe_allow_html=True)
                render_movie_grid(genre_cards, key_prefix="detail_genre", cols_per_row=6)
        else:
            # Fallback to genre-only
            genre_only, err3 = api_get_json("/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18})
            if not err3 and genre_only:
                st.markdown('<div class="section-title">🎭 Similar Movies</div>', unsafe_allow_html=True)
                render_movie_grid(genre_only, key_prefix="detail_genre_fallback", cols_per_row=6)
            else:
                st.info("No recommendations available at the moment.")
    else:
        st.info("Unable to fetch recommendations.")

# =============================
# FOOTER
# =============================
st.markdown("""
<div class="footer">
    <p>Made with ❤️ using Streamlit | Powered by TMDB API</p>
    <p>© 2024 MovieFlix - Your Personal Movie Universe</p>
</div>
""", unsafe_allow_html=True)