import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("tracks.csv")
df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
df.dropna(subset=["year"], inplace=True)
df["year"] = df["year"].astype(int)

# Predefined Genre List
genre_options = ["All"] + sorted([
    "Alternative rock", "Ambient music", "American folk music", "Avant-garde music", "Bhangra",
    "Blues", "Bollywood", "Carnatic music", "Children's music", "Christian music", "Classical music",
    "Corridos", "Country music", "Cumbia", "Dance music", "Disco", "Easy listening",
    "Electronic dance music", "Electronic music", "Experimental music", "Flamenco", "Folk music",
    "Funk", "Grupero", "Hard rock", "Heavy metal", "Hindustani classical music", "Hip-hop culture",
    "Hip-hop", "Indie rock", "Indian classical music", "Jazz fusion", "Jazz", "K-pop",
    "Latin music", "Mariachi", "Music of Asia", "Music of Latin America", "New wave",
    "New-age music", "Norteño", "Pop music", "Pop rock", "Popular music",
    "Post-punk", "Progressive rock", "Punk rock", "Ranchera", "Reggae",
    "Reggaeton", "Rhythm and blues", "Rock and roll", "Salsa", "Ska",
    "Soul music", "Synth-pop", "Techno", "Vaporwave", "Vocal music",
    "World music"
])

# Sidebar Navigation
st.sidebar.title("🎵 Navigation")
selection = st.sidebar.radio("Go to", ["📊 Trends", "🎧 Recommender", "📈 Insights", "📖 About"], key="nav_radio_unique")

# --- Trends Tab ---
if selection == "📊 Trends":
    st.title("📊 Trends Over Time")
    genres_selected = st.multiselect("Filter by Genre(s):", genre_options, default=["All"], key="trends_genre_unique")

    feature = st.selectbox("Select a feature to plot:", ["popularity", "danceability", "energy", "duration_ms"], key="trends_feature_unique")
    start_year, end_year = st.slider("Select Year Range", 1921, 2020, (1921, 2020), key="trends_year_unique")

    filtered_df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]
    if "All" not in genres_selected and "genre" in df.columns:
        filtered_df = filtered_df[filtered_df["genre"].isin(genres_selected)]

    avg_feature = filtered_df.groupby("year")[feature].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(avg_feature.index, avg_feature.values, color="#1DB954")  # Spotify green for charts
    ax.set_title(f"Average {feature.capitalize()} ({start_year}-{end_year})")
    ax.set_xlabel("Year")
    ax.set_ylabel(feature.capitalize())
    st.pyplot(fig)

# --- Recommender Tab ---
elif selection == "🎧 Recommender":
    st.title("🎧 Song Recommender")
    genres_selected = st.multiselect("Filter by Genre(s):", genre_options, default=["All"], key="recommender_genre_unique")

    danceability = st.slider("Danceability", 0.0, 1.0, 0.5, key="recommender_danceability_unique")
    energy = st.slider("Energy", 0.0, 1.0, 0.5, key="recommender_energy_unique")

    recommendations = df[
        (df["danceability"].between(danceability - 0.1, danceability + 0.1)) &
        (df["energy"].between(energy - 0.1, energy + 0.1))
    ]
    if "All" not in genres_selected and "genre" in df.columns:
        recommendations = recommendations[recommendations["genre"].isin(genres_selected)]

    recommendations = recommendations.sort_values(by="popularity", ascending=False)[["name", "artists", "popularity"]].head(10)

    st.subheader("Top 10 Recommended Songs")
    st.table(recommendations)

# --- Insights Tab ---
elif selection == "📈 Insights":
    st.title("📈 Data Insights")
    st.markdown("Explore relationships between popularity and song features.")

    selected_feature = st.selectbox("Choose a feature to compare with popularity:", ["danceability", "energy", "valence", "acousticness", "tempo"], key="insights_scatter_unique")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.scatter(df[selected_feature], df["popularity"], alpha=0.5, color="#1DB954")
    ax1.set_xlabel(selected_feature.capitalize())
    ax1.set_ylabel("Popularity")
    ax1.set_title(f"Popularity vs {selected_feature.capitalize()}")
    st.pyplot(fig1)

    st.subheader("Feature Distribution")
    dist_feature = st.selectbox("Select a feature to view distribution:", ["danceability", "energy", "valence", "acousticness", "tempo"], key="insights_hist_unique")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.hist(df[dist_feature], bins=30, color="#1DB954", edgecolor="white")
    ax2.set_title(f"Distribution of {dist_feature.capitalize()}")
    ax2.set_xlabel(dist_feature.capitalize())
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

# --- About Tab ---
elif selection == "📖 About":
    st.title("📖 About This Dashboard")
    st.markdown("""
        <div style="background-color:#333; border-radius:15px; padding:20px; box-shadow:0 4px 8px rgba(0,0,0,0.2); color:white;">
            <h3 style="color:white;">About This Web App</h3>
            <p>This Spotify Data Analysis Dashboard helps users explore and visualize Spotify music trends, gain insights into song characteristics, and receive tailored song recommendations. You can:</p>
            <ul>
                <li>📊 View how song features like popularity, energy, and danceability change over time.</li>
                <li>🎧 Filter songs by genre and get personalized recommendations.</li>
                <li>📈 Analyze relationships between different audio features and popularity.</li>
            </ul>
            <p><strong>Rodrigo Pena</strong> created this app to combine data science with music analytics and share insights in an interactive way.</p>
            <p>🔗 <a href="https://github.com/Gamerzrod" target="_blank" style="color:white; text-decoration:underline;">View the GitHub Repository</a></p>
        </div>
    """, unsafe_allow_html=True)

# --- Fancy Fixed Footer ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        font-family: Arial, sans-serif;
    }
    .footer img {
        vertical-align: middle;
        margin-right: 8px;
        height: 20px;
    }
    .footer a {
        color: white;
        text-decoration: underline;
    }
    </style>
    <div class="footer">
        <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Spotify Logo">
        🎵 Created by <b>Rodrigo Pena</b> | 📅 July 2025 |
        <a href="https://github.com/Gamerzrod" target="_blank">GitHub</a>
    </div>
""", unsafe_allow_html=True)
