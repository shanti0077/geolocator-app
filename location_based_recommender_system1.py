import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans

# Function to load and preprocess data
def load_data():
    file_path = 'locations.csv'  # assuming CSV file is named 'locations.csv' in the main folder
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
    st.title("Find Nearest Cities")

    df = load_data()
    city_names = df['location'].tolist()
    input_city = st.selectbox("Select a city", city_names)
    if st.button("Find Nearest Cities"):
        nearest_cities = find_nearest_cities(df, input_city)
        if nearest_cities:
            st.success(f"The 5 nearest cities to {input_city} are: {', '.join(nearest_cities)}")
            output_df = pd.DataFrame({'Nearest Cities': nearest_cities})
            output_df.to_csv('nearest_cities.csv', index=False)
            st.markdown("### Download Nearest Cities CSV")
            st.markdown(get_binary_file_downloader_html('nearest_cities.csv', 'Nearest Cities CSV'), unsafe_allow_html=True)
        else:
            st.warning("City not found or location data not available.")

# Function to create a download link for a file
def get_binary_file_downloader_html(file_path, file_label='File'):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{file_path}">{file_label}</a>'

if __name__ == "__main__":
    main()
