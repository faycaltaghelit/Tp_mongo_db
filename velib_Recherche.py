import folium
import pymongo
from geopy.geocoders import Nominatim
import webbrowser
from geopy.distance import geodesic

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="geo_locator_app")

# Demander l'adresse à l'utilisateur
adresse = input("Entrez une adresse (ville ou code postal inclus) : ")

# Géocoder l'adresse
location = geolocator.geocode(adresse)

# Vérifier si une localisation a été trouvée
if location:
    print(f"Latitude : {location.latitude}")
    print(f"Longitude : {location.longitude}")

    # Créer une carte centrée sur l'adresse saisie
    m = folium.Map(location=[location.latitude, location.longitude], tiles="OpenStreetMap", zoom_start=16)
    
    # Lien Google Street View pour l'adresse saisie
    street_view_url1 = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={location.latitude},{location.longitude}"

    # HTML pour le popup de l'adresse saisie
    msg_html1 = f"""
    <div style="font-family: Arial, sans-serif; width: 250px;">
        <h3 style="color: #4a4a4a;">{adresse}</h3>
        <p style="color: #666;">Localisation de l'adresse entrée.</p>
        <a href="{street_view_url1}" target="_blank" style="display: inline-block; background-color: #4285F4; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; margin-top: 10px;">Voir dans Street View</a>
    </div>
    """
    folium.Marker([location.latitude, location.longitude],
                  popup=folium.Popup(msg_html1, max_width=300),
                  icon=folium.Icon(color='blue', icon='home')).add_to(m)

    # Connexion au serveur MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["test"]
    mycol = mydb["velib"]
    stations = list(mycol.find())

    # Ajouter des marqueurs pour les stations Velib à proximité
    for station in stations:
        station_location = (station['coordonnees_geo']['lat'], station['coordonnees_geo']['lon'])
        distance = geodesic((location.latitude, location.longitude), station_location).meters
        if distance < 500:  # Limite de 500 mètres
            station_info = f"""
            <div style="font-family: Arial, sans-serif; width: 250px;">
                <h3 style="color: #4a4a4a;">{station['name']}</h3>
                <p style="color: #666;">{station['ebike']} vélos électriques</p>
                <p style="color: #666;">{station['mechanical']} vélos mécaniques</p>
                <p style="color: #666;">{station['numdocksavailable']} docks disponibles</p>
                <p style="color: #666; font-weight: bold;">Distance : {int(distance)} mètres</p>
                <a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={station['coordonnees_geo']['lat']},{station['coordonnees_geo']['lon']}" 
                   target="_blank" 
                   style="display: inline-block; background-color: #4285F4; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; margin-top: 10px;">Voir dans Street View</a>
            </div>
            """
            folium.Marker([station['coordonnees_geo']['lat'], station['coordonnees_geo']['lon']],
                          popup=folium.Popup(station_info, max_width=300),
                          icon=folium.Icon(color='green', icon='bicycle')).add_to(m)

    # Enregistrer la carte
    m.save("map.html")
    print("Carte enregistrée sous map.html")
    # Ouvrir la carte dans un navigateur
    webbrowser.open("map.html")
else:
    print("Adresse non trouvée.")
