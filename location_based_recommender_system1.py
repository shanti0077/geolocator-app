import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_nearby_cities(city_name, num_cities=5, distance_threshold=50):
    geolocator = Nominatim(user_agent="city_nearby_app")
    location = geolocator.geocode(city_name)
    if location:
        lat, lon = location.latitude, location.longitude
        nearby_cities = []
        for nearby_location in geolocator.reverse((lat, lon), exactly_one=False):
            if nearby_location.address != city_name:
                city_distance = geodesic((lat, lon), (nearby_location.latitude, nearby_location.longitude)).kilometers
                if city_distance <= distance_threshold:
                    nearby_cities.append((nearby_location.address, round(city_distance, 2)))
                if len(nearby_cities) >= num_cities:
                    break
        return nearby_cities
    else:
        return None

# Streamlit UI
st.title("Find Nearby Cities")
st.text("Developer - Shanti Trivedi")
input_city = st.text_input("Enter a city name:")
num_nearby_cities = st.slider("Number of nearby cities to display:", min_value=1, max_value=20, value=5)
distance_threshold = st.slider("Maximum distance (in kilometers):", min_value=10, max_value=200, value=50)

if input_city:
    nearby_cities = get_nearby_cities(input_city, num_cities=num_nearby_cities, distance_threshold=distance_threshold)
    if nearby_cities:
        st.success(f"Nearby cities to {input_city}:")
        for city, distance in nearby_cities:
            st.write(f"- {city} ({distance} km)")
    else:
        st.error("City not found or no nearby cities found.")

