import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(filename: str = "books_data.csv") -> pd.DataFrame:
    """Load book data from CSV file."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        st.error("Data file not found. Please run the scraper first.")
        return pd.DataFrame()

def main():
    """Main function to create the Streamlit dashboard."""
    st.title("Books Data Dashboard")
    st.write("Visualizing scraped book data from books.toscrape.com")

    # Load data
    df = load_data()

    if df.empty:
        st.stop()

    # Bar chart: Average price by genre
    st.subheader("Average Price by Genre")
    avg_price = df.groupby('genre')['price'].mean().reset_index()
    fig_bar = px.bar(avg_price, x='genre', y='price', title="Average Book Price by Genre",
                     color='genre', color_discrete_sequence=px.colors.qualitative.Plotly)
    st.plotly_chart(fig_bar)

    # Scatter plot: Price vs. Rating
    st.subheader("Price vs. Rating")
    fig_scatter = px.scatter(df, x='rating', y='price', text='title',
                            title="Book Price vs. Rating", hover_data=['genre'])
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter)

    # Table: Top 10 highest-rated books
    st.subheader("Top 10 Highest-Rated Books")
    top_books = df.nlargest(10, 'rating')[['title', 'price', 'rating', 'genre']]
    st.dataframe(top_books)

if __name__ == "__main__":
    main()
