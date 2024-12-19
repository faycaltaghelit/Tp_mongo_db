import webbrowser
import folium
import pymongo
from branca.element import IFrame

# MongoDB connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["velib"]
Cursor = mycol.find()
tablo_stations = list(Cursor)

# Create the map
m = folium.Map(location=[48.821270, 2.311693], tiles="OpenStreetMap", zoom_start=15)

# Add markers for stations
for station in tablo_stations:
    msg1 = f"{station['ebike']} vélos électriques"
    msg2 = f"{station['mechanical']} vélos mécaniques"
    msg3 = f"{station['numdocksavailable']} docks disponibles"

    html = f"""
    <html>
    <head>
        <style>
            .station-popup {{
                font-family: Arial, sans-serif;
                padding: 10px;
                max-width: 200px;
                box-shadow: 8px 8px 12px #aaa;
            }}
            .station-name {{
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }}
            .station-info {{
                font-size: 14px;
                color: #666;
                margin-bottom: 5px;
            }}
            .street-view-link {{
                display: inline-block;
                margin-top: 10px;
                padding: 5px 10px;
                background-color: #4285F4;
                color: white;
                text-decoration: none;
                border-radius: 3px;
            }}
        </style>
    </head>
    <body>
        <div class="station-popup">
            <div class="station-name">{station['name']}</div>
            <div class="station-info">{msg1}</div>
            <div class="station-info">{msg2}</div>
            <div class="station-info">{msg3}</div>
            <a href="https://www.google.com/maps?layer=c&cbll={station['coordonnees_geo']['lat']},{station['coordonnees_geo']['lon']}" target="_blank" class="street-view-link">View in Street View</a>
        </div>
    </body>
    </html>
    """

    iframe = IFrame(html=html, width=220, height=150)
    popup = folium.Popup(iframe, max_width=300)

    folium.Marker(
        [station['coordonnees_geo']['lat'], station['coordonnees_geo']['lon']],
        popup=popup,
        tooltip=station['name']  # Tooltip for station name
    ).add_to(m)

# Add search functionality
search_html = """
<script>
    function addSearchBar(mapId) {
        const searchBar = document.createElement('input');
        searchBar.type = 'text';
        searchBar.placeholder = 'Rechercher une station...';
        searchBar.style.width = '300px';
        searchBar.style.padding = '10px';
        searchBar.style.position = 'absolute';
        searchBar.style.top = '10px';
        searchBar.style.right = '10px';
        searchBar.style.zIndex = 1000;
        searchBar.style.border = '1px solid #ccc';
        searchBar.style.borderRadius = '5px';
        
        document.getElementById(mapId).appendChild(searchBar);

        searchBar.addEventListener('input', function() {
            const query = searchBar.value.toLowerCase();
            const markers = document.getElementsByClassName('leaflet-marker-icon');
            for (let marker of markers) {
                const title = marker.getAttribute('title') || '';
                if (title.toLowerCase().includes(query)) {
                    marker.style.display = '';
                } else {
                    marker.style.display = 'none';
                }
            }
        });
    }
    window.onload = function() {
        addSearchBar('map');
    };
</script>
"""

# Add the script to the map
m.get_root().html.add_child(folium.Element(search_html))

# Save the map and open it
m.save("velib_map.html")
webbrowser.open('velib_map.html')
