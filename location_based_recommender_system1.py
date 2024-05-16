import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

st.title("Location Based Recommender System Using Clustering")
st.text("Developer - Shanti Trivedi")

# Load the data
df = pd.read_csv('cities2.csv')

# Extract relevant columns for clustering
L2 = df.iloc[:, -1: -3: -1]

# Perform KMeans clustering
kmeans = KMeans(n_clusters=10, random_state=0)  #north South West East and Central India
kmeans.fit(L2)

# Add cluster labels to the dataframe
df['loc_clusters'] = kmeans.labels_

# Create input box for user to enter city name
input_city = st.text_input("Enter a city name:")

if input_city:
    # Find the cluster of the input city
    try:
        cluster = int(df.loc[df['location'] == input_city, 'loc_clusters'].iloc[0])
        
        # Find cities in the same cluster and display them
        cities = df.loc[df['loc_clusters'] == cluster, 'location']
        st.write("Cities in the same cluster:")
        for c in cities:
            if c != input_city:
                st.write(c)
    except IndexError:
        st.write("City not found in the dataset.")

