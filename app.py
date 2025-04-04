import pickle
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Page configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with modern UI elements
st.markdown("""
<style>
    /* Global Typography */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Modern Color Scheme */
    :root {
        --primary: #7F5AF0;         /* Main brand color - vibrant purple */
        --primary-dark: #6B40D8;    /* Darker purple for hover states */
        --secondary: #FF8E3C;       /* Accent color - orange */
        --text-primary: #242629;    /* Dark slate for main text */
        --text-secondary: #94A1B2;  /* Medium gray for secondary text */
        --bg-light: #F9F9FB;        /* Very light gray for backgrounds */
        --bg-card: #FFFFFE;         /* White for cards */
        --bg-dark: #16161A;         /* Dark background */
        --shadow-sm: 0 8px 30px rgba(0,0,0,0.05);
        --shadow-md: 0 15px 35px rgba(0,0,0,0.08);
        --gradient-primary: linear-gradient(135deg, #7F5AF0 0%, #6B40D8 100%);
        --gradient-secondary: linear-gradient(135deg, #FF8E3C 0%, #FF5400 100%);
    }

    /* App Container */
    .main {
        background-color: var(--bg-light);
        padding: 0 !important;
    }

    /* Header Styling */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 4rem !important;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.25rem !important;
        font-weight: 500;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }

    /* Movie Card Styling */
    .poster-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 0.75rem;
        padding: 1.5rem;
        background-color: var(--bg-card);
        border-radius: 24px;
        box-shadow: var(--shadow-sm);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        overflow: hidden;
        border: 1px solid rgba(127, 90, 240, 0.1);
    }

    .poster-container:hover {
        transform: translateY(-12px);
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(127, 90, 240, 0.3);
    }

    .poster-container img {
        border-radius: 16px;
        object-fit: cover;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .poster-container:hover img {
        transform: scale(1.03);
    }

    .movie-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-primary);
        height: 2.5rem;
        margin-top: 1.25rem;
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }

    .movie-metadata {
        margin-top: 0.5rem;
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Selected Movie Container */
    .selected-movie-container {
        background-color: var(--bg-card);
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: var(--shadow-sm);
        margin-bottom: 2rem;
        height: 100%;
        border: 1px solid rgba(127, 90, 240, 0.1);
        position: relative;
        overflow: hidden;
    }

    .selected-movie-container:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 24px 0 0 24px;
    }

    .selected-movie-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.25rem;
    }

    .selected-movie-metadata {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
    }

    /* Search Box Styling */
    .search-container {
        background: var(--bg-card);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid rgba(127, 90, 240, 0.1);
        border-left: 9px solid var(--primary);
        position: relative;
        margin: 0 auto 3rem auto;
        max-width: 800px;
    }

    .search-icon {
        position: absolute;
        left: 1.5rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--primary);
        font-size: 1.5rem;
    }

    .stSelectbox > div {
        background-color: transparent !important;
    }

    .stSelectbox > div > div {
        background-color: transparent;
        border: 2px solid rgba(127, 90, 240, 0.2);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        color: var(--text-primary);
        font-size: 1.1rem;
        box-shadow: none !important;
        
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover, .stSelectbox > div > div:focus {
        border-color: var(--primary);
    }

    /* Button Styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 2.5rem;
        font-size: 1.15rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 15px rgba(127, 90, 240, 0.3);
        width: 100%;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }

    .stButton > button:hover {
        box-shadow: 0 10px 20px rgba(127, 90, 240, 0.4);
        transform: translateY(-3px);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 5px 10px rgba(127, 90, 240, 0.3);
    }

    .stButton > button:after {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: -100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: all 0.5s ease;
    }

    .stButton > button:hover:after {
        left: 100%;
    }

    /* Section Headers */
    .recommendation-text {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 3rem 0 2rem 0;
        text-align: center;
        position: relative;
    }

    .recommendation-text:after {
        content: '';
        position: absolute;
        width: 100px;
        height: 5px;
        background: var(--gradient-primary);
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        border-radius: 100px;
    }

    /* App Background Container */
    .app-background {
        background-color: var(--bg-light);
        padding: 3rem;
        border-radius: 30px;
        border-left: 12px solid var(--primary);
        margin: 2rem auto;
        max-width: 1440px;
    }

    /* Rating Badge */
    .rating-badge {
        background-color: rgba(255, 213, 0, 0.1);
        color: #FFB700;
        padding: 0.4rem 0.8rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        margin-right: 0.9rem;
        border: 1px solid rgba(255, 213, 0, 0.2);
    }

    .year-badge {
        background-color: rgba(127, 90, 240, 0.1);
        color: var(--primary);
        padding: 0.4rem 0.8rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        border: 1px solid rgba(127, 90, 240, 0.2);
    }

    .genre-badge {
        background-color: rgba(255, 142, 60, 0.1);
        color: var(--secondary);
        padding: 0.3rem 0.7rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(255, 142, 60, 0.2);
    }

    /* Overview Section */
    .overview-section {
        background-color: rgba(127, 90, 240, 0.03);
        padding: 1.25rem;
        border-radius: 12px;
        margin-top: 1.25rem;
        border-left: 3px solid var(--primary);
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 5rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(148, 161, 178, 0.2);
        color: var(--text-secondary);
        font-size: 0.95rem;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background-color: var(--bg-card) !important;
    }

    .sidebar-header {
        color: var(--primary);
        font-weight: 700;
        font-size: 1.75rem;
        margin-bottom: 1.5rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }

    .sidebar-subheader {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.25rem;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid rgba(127, 90, 240, 0.2);
        padding-bottom: 0.5rem;
    }

    /* Loading Animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
        flex-direction: column;
    }

    /* Movie Poster Styling */
    .poster-image {
        position: relative;
        width: 100%;
        transition: all 0.4s ease;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }

    .poster-image:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, rgba(0,0,0,0) 70%, rgba(0,0,0,0.7) 100%);
        z-index: 1;
        opacity: 0;
        transition: all 0.4s ease;
    }

    .poster-container:hover .poster-image:before {
        opacity: 1;
    }

    /* Match Score Badge */
    .match-score {
        background: var(--gradient-primary);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        position: relative;
        margin-top: 0.75rem;
        box-shadow: 0 4px 10px rgba(127, 90, 240, 0.3);
    }

    /* How It Works Steps */
    .how-it-works-step {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
    }

    .step-number {
        background: var(--gradient-primary);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-right: 0.75rem;
        flex-shrink: 0;
    }

    .step-text {
        color: var(--text-secondary);
        font-size: 0.95rem;
    }

    /* Card hover effect */
    .hover-scale {
        transition: all 0.4s ease;
    }

    .hover-scale:hover {
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)


# Function to load Lottie animation
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


# Function to fetch movie poster and details
def fetch_poster(movie_id):
    try:
        data = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=9a05ae3f6e37d158f35f6214d24e7790&language=en-US'.format(
                movie_id))
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        # Get additional movie details
        release_year = data.get('release_date', '')[:4] if data.get('release_date') else 'N/A'
        rating = data.get('vote_average', 'N/A')
        overview = data.get('overview', 'No overview available')
        genres = [genre['name'] for genre in data.get('genres', [])]
        runtime = data.get('runtime', 'N/A')

        return full_path, release_year, rating, overview, genres, runtime
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available", 'N/A', 'N/A', 'No overview available', [], 'N/A'


# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_years = []
        recommended_movie_ratings = []
        recommended_movie_details = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            poster, year, rating, overview, genres, runtime = fetch_poster(movie_id)
            recommended_movie_posters.append(poster)
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_years.append(year)
            recommended_movie_ratings.append(rating)
            recommended_movie_details.append({
                'overview': overview,
                'genres': genres,
                'runtime': runtime,
                'similarity': round(i[1] * 100, 1)  # Similarity percentage
            })

        return recommended_movie_names, recommended_movie_posters, recommended_movie_years, recommended_movie_ratings, recommended_movie_details
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [], [], [], [], []


# Load animations
lottie_movie = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_khzniaya.json")
lottie_loading = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_p8bfn5to.json")

# Sidebar for additional information
with st.sidebar:
    st.image("https://mir-s3-cdn-cf.behance.net/projects/404/500615208701615.Y3JvcCwxMzA5LDEwMjQsNjQsMA.png",
             use_container_width=True)
    st.markdown("<h3 class='sidebar-header'>About CineMatch</h3>", unsafe_allow_html=True)
    st.write(
        "CineMatch is an AI-powered movie recommendation system that suggests films based on your preferences and viewing habits.")

    st.markdown("<h4 class='sidebar-subheader'>How it works</h4>", unsafe_allow_html=True)

    # Enhanced how it works section with steps
    st.markdown("""
    <div class="how-it-works-step">
        <div class="step-number">1</div>
        <div class="step-text">Select a movie you love from our extensive database</div>
    </div>
    <div class="how-it-works-step">
        <div class="step-number">2</div>
        <div class="step-text">Our algorithm analyzes your selection using content-based filtering</div>
    </div>
    <div class="how-it-works-step">
        <div class="step-number">3</div>
        <div class="step-text">Discover personalized movie recommendations tailored to your taste</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h4 class='sidebar-subheader'>Dataset Information</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: rgba(127, 90, 240, 0.05); padding: 1rem; border-radius: 10px; border-left: 3px solid var(--primary);">
        Our system leverages data from TMDB (The Movie Database) with information on thousands of movies including genres, cast, crew, and user ratings.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h4 class='sidebar-subheader'>Created by</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: rgba(127, 90, 240, 0.05); padding: 1rem; border-radius: 10px; text-align: center;">
        <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.1rem;">Sojal Jain</div>
    """, unsafe_allow_html=True)

    # Add social media links as icons
    col1, col2= st.columns(2)
    with col1:
        st.markdown(
            "[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sojaljain02)")
    with col2:
        st.markdown(
            "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sojal-jain-985221281/)")

    st.markdown("</div>", unsafe_allow_html=True)

# Main content
st.markdown('<div class="app-background">', unsafe_allow_html=True)

# Header section with animation and title
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])

with header_col2:
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; gap: 20px;">',
                unsafe_allow_html=True)
    if lottie_movie:
        st_lottie(lottie_movie, speed=1, height=120, key="movie_animation")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">CineMatch</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover your next favorite movie with AI-powered recommendations</p>',
                unsafe_allow_html=True)

# Load movies data
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie_list = movies['title'].values
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    st.stop()

# Search box with autocomplete - enhanced design
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.markdown('<p style="font-weight: 600; font-size: 1.2rem; margin-bottom: 1rem;">🔍 Find Movies You Love</p>',
            unsafe_allow_html=True)
selected_movie = st.selectbox(
    "Search for a movie title",
    movie_list,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# Fetch selected movie poster and details for display
try:
    selected_movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
    selected_poster, selected_year, selected_rating, selected_overview, selected_genres, selected_runtime = fetch_poster(
        selected_movie_id)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div style="position: relative; border-radius: 20px; overflow: hidden; margin-top:12rem; box-shadow: 0 20px 40px rgba(0,0,0,0.2);" class="hover-scale">
        """, unsafe_allow_html=True)
        st.image(selected_poster, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="selected-movie-container">', unsafe_allow_html=True)
        st.markdown(f'<h2 class="selected-movie-title">{selected_movie}</h2>', unsafe_allow_html=True)

        # Movie metadata with improved styling
        st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 1.25rem;">',
                    unsafe_allow_html=True)
        st.markdown(f'<span class="rating-badge">⭐ {selected_rating}/10</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="year-badge">🗓️ {selected_year}</span>', unsafe_allow_html=True)
        if selected_runtime != 'N/A':
            st.markdown(f'<span class="year-badge">⏱️ {selected_runtime} min</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Genres with individual badges
        if selected_genres:
            st.markdown('<div style="margin-bottom: 1.25rem;">', unsafe_allow_html=True)
            for genre in selected_genres[:4]:
                st.markdown(f'<span class="genre-badge">#{genre}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Overview with styled container
        st.markdown('<div class="overview-section">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight: 600; margin-bottom: 0.5rem;'>Overview</p>", unsafe_allow_html=True)
        if len(selected_overview) > 300:
            st.markdown(f"<p style='color: var(--text-secondary);'>{selected_overview[:300]}...</p>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: var(--text-secondary);'>{selected_overview}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
        find_button = st.button('✨ Find Similar Movies')
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
except:
    st.markdown('<div style="max-width: 400px; margin: 2rem auto; text-align: center;">', unsafe_allow_html=True)
    st.markdown(
        '<div style="background: var(--bg-card); padding: 2rem; border-radius: 20px; box-shadow: var(--shadow-sm);">',
        unsafe_allow_html=True)
    st.markdown(
        '<p style="font-weight: 600; font-size: 1.2rem; margin-bottom: 1.5rem;">Ready to discover new movies?</p>',
        unsafe_allow_html=True)
    find_button = st.button('✨ Find Similar Movies')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Create a container for the loading animation
loading_container = st.empty()

# Recommendations section
if find_button:
    # Show loading animation in the container with enhanced styling
    with loading_container.container():
        st.markdown('<div class="loading-animation">', unsafe_allow_html=True)
        if lottie_loading:
            st_lottie(lottie_loading, speed=1, height=200, key="loading_animation")
        st.markdown(
            '<p style="text-align: center; margin-top: 20px; font-size: 1.25rem; color: var(--primary); font-weight: 500;">Finding the perfect movies for you...</p>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Process recommendations
    recommended_movie_names, recommended_movie_posters, recommended_movie_years, recommended_movie_ratings, recommended_movie_details = recommend(
        selected_movie)

    # Clear the loading animation after processing
    loading_container.empty()

    if recommended_movie_names:
        st.markdown('<h2 class="recommendation-text">Movies You Might Enjoy</h2>', unsafe_allow_html=True)
        cols = st.columns(5)

        for i, col in enumerate(cols):
            with col:
                if i < len(recommended_movie_posters):
                    st.markdown(f'<div class="poster-container">', unsafe_allow_html=True)

                    # Enhanced poster container with hover effects
                    st.markdown(f'<div class="poster-image">', unsafe_allow_html=True)
                    st.image(recommended_movie_posters[i], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="movie-title">{recommended_movie_names[i]}</div>', unsafe_allow_html=True)

                    # Enhanced metadata display
                    st.markdown(
                        f'''<div class="movie-metadata">
                            <span style="color: #FFB700;">⭐ {recommended_movie_ratings[i]}/10</span> &bull; {recommended_movie_years[i]}
                        </div>''',
                        unsafe_allow_html=True)

                    # Add similarity score with improved badge
                    if i < len(recommended_movie_details):
                        similarity_score = recommended_movie_details[i]['similarity']
                        st.markdown(
                            f'<div class="match-score">{similarity_score}% Match</div>',
                            unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer with enhanced styling
st.markdown('''
<div class="footer">
    <div style="margin-bottom: 15px; font-size: 1.2rem; font-weight: 600; color: var(--primary);">CineMatch</div>
    <div style="margin-bottom: 10px;">Bringing personalized movie recommendations to cinephiles everywhere</div>
    <div style="color: var(--text-secondary); font-size: 0.8rem;">© 2025 CineMatch - All rights reserved</div>
</div>
''', unsafe_allow_html=True)
