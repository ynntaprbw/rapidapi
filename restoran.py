import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_restaurants(location_type, location):
    base_url = "https://restaurants-near-me-usa.p.rapidapi.com/restaurants/location/"
    if location_type.lower() == "state":
        url = base_url + "state/" + location + "/0"
    elif location_type.lower() == "zipcode":
        url = base_url + "zipcode/" + location + "/0"
    else:
        return "Invalid location type. Please choose 'state' or 'zipcode'."

    headers = {
        "X-RapidAPI-Key": "aa9a42ef2amshbe9ea8ebc8369d9p1e5926jsn3ca9e409fa0a",
        "X-RapidAPI-Host": "restaurants-near-me-usa.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return "Error: " + str(response.status_code)

# Streamlit app
st.title("Restaurants Near Me")

location_type = st.radio("Select location type:", ("State", "Zipcode"))
location = st.text_input("Enter location:")

if st.button("Search"):
    if location_type and location:
        restaurants_data = get_restaurants(location_type, location)
        if isinstance(restaurants_data, dict) and "restaurants" in restaurants_data:
            restaurants_list = restaurants_data["restaurants"]
            # Mengkonversi data ke DataFrame
            df = pd.DataFrame(restaurants_list)
            # Menghapus kolom "id" dan "email"
            df = df.drop(columns=["id", "email"], errors="ignore")
            st.write("Found restaurants:")
            st.dataframe(df)
            
            # Visualisasi pie chart persentase untuk kolom 'cuisineType'
            cuisine_counts = df['cuisineType'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(cuisine_counts, labels=cuisine_counts.index, autopct='%1.1f%%')
            ax.axis('equal')  # Memastikan lingkaran berbentuk lingkaran
            st.pyplot(fig)
            
        else:
            st.write(restaurants_data)
    else:
        st.write("Please enter location information.")
