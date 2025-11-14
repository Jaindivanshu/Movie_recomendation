import streamlit as st
from recommendation import recommend_movies, get_movie_info, movies

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    with st.spinner("Finding similar movies..."):
        recs = recommend_movies(selected_movie)

    st.subheader("You might also like:")

    for movie in recs:
        info = get_movie_info(movie)

        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(info["poster"], width=150)
            with cols[1]:
                st.markdown(f"### 🎥 {movie} ({info['year']})")
                st.markdown(f"**IMDb Rating:** ⭐ {info['rating']}")
                st.write(info["plot"])
            st.markdown("---")
