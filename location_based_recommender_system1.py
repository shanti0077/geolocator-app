import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans

# Function to load and preprocess data
def load_data():
    file_path = 'locations_30.csv'  # assuming CSV file is named 'locations.csv' in the main folder
    df = pd.read_csv(file_path)
    geolocator = Nominatim(user_agent="Trips")
    coordinates = []
    for city in df['location']:
        location = geolocator.geocode(city)
        coordinates.append((location.latitude, location.longitude) if location else (None, None))
    df[['Latitude', 'Longitude']] = pd.DataFrame(coordinates, columns=['Latitude', 'Longitude'])
    return df.dropna()

# Function to find nearest cities
def find_nearest_cities(df, input_city, n=5):
    input_city_row = df[df['location'] == input_city]
    if input_city_row.empty:
        return []
    input_lat, input_lon = input_city_row.iloc[0]['Latitude'], input_city_row.iloc[0]['Longitude']
    df['distance'] = ((df['Latitude'] - input_lat) ** 2 + (df['Longitude'] - input_lon) ** 2) ** 0.5
    nearest_cities = df.sort_values(by='distance').iloc[1:n+1]['location'].tolist()
    return nearest_cities

# Streamlit App
def main():
    st.title("Location Based Recommender System")
    st.text("Developer - Shanti Trivedi")

    df = load_data()
    city_names = df['location'].tolist()
    input_city = st.selectbox("Select a city", city_names)
    if st.button("Find Nearest Cities"):
        nearest_cities = find_nearest_cities(df, input_city)
        if nearest_cities:
            st.success(f"The 5 nearest cities to {input_city} are: {', '.join(nearest_cities)}")
            
        else:
            st.warning("City not found or location data not available.")

if __name__ == "__main__":
    main()
