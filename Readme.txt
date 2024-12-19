
projet Python permettant de localiser une adresse saisie par l'utilisateur, de visualiser les stations Velib à proximité (dans un rayon de 500 mètres), et d'afficher leurs informations (nombre de vélos disponibles, docks, etc.) sur une carte interactive.

## Fonctionnalités

- Géocodage d'une adresse pour obtenir ses coordonnées GPS (latitude et longitude).
- Création d'une carte interactive centrée sur l'adresse saisie.
- Recherche des stations Velib situées dans un rayon de 500 mètres.


## Prérequis

- Python 3.x
- Les bibliothèques Python suivantes :
  - `folium`
  - `pymongo`
  - `geopy`
  - `webbrowser`
- Une base de données MongoDB avec une collection `velib` contenant les informations des stations. Exemple de document pour une station :
  ```json
  {
    "name": "Station Velib Example",
    "coordonnees_geo": {
      "lat": 48.8566,
      "lon": 2.3522
    },
    "ebike": 5,
    "mechanical": 10,
    "numdocksavailable": 7
  }
