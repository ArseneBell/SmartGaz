from serpapi import GoogleSearch
import json
from model.station import Station
from werkzeug.security import generate_password_hash, check_password_hash
import geocoder



api_key = '18d339a63a0c0be2510751f2742fa2730540059c105713a49ca17e0620dcf60d'


def get_all_stations_ville(ville = 'Yaounde'):
    params = {
    "engine": "google_local",
    "q": f"Toutes les station Total Energies de {ville}",
    'gl' : 'cm',
    'hl' : 'fr',
    "location": "Cameroon",
    "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    local_results = results["local_results"]

    with open(f'TotalEnergies{ville}.json', 'w', encoding='utf-8') as f:
        json.dump(local_results, f, indent=4, ensure_ascii=False)
        
    return local_results
        
        
        
def get_stations_quartier(ville = 'Yaounde', quartier = ''):
    params = {
    "engine": "google_local",
    "q": f"Localisation du quartier {quartier} à {ville} Cameroun",
    'gl' : 'cm',
    'hl' : 'fr',
    "location": "Cameroon",
    "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    local_results = results["local_results"]

        
    return local_results

def get_stations_area(ville = 'Yaounde'):
    params = {
    "engine": "google_local",
    "q": f"Les stations Total Energies de {ville} au Cameroun",
    'gl' : 'cm',
    'hl' : 'fr',
    "location": "Cameroon",
    "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    local_results = results["local_results"]

        
    return local_results


def get_localisation(ville = 'Yaounde', quartier = ''):
    params = {
    "engine": "google_local",
    "q": f"Localisation du quartier {quartier} à {ville}.",
    "ludocid": "11859840425088059614",
    "location": "Cameroon",
    "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    local_results = results["local_results"]
        
    return local_results


def trunc_name(name):
    trunc = name.split(' ')
    result = ''
    if name != '' and name != None:
        if len(trunc) >= 2:
            result += trunc[0][0]
            result += trunc[1][0]
        else:
            result += trunc[0][0]
            result += trunc[0][1]
    return result.upper()


def get_nearest_stations(stations, quarter = 'Nkoldongo'):
    try:
        quartier = get_localisation(ville = 'Yaounde', quartier = quarter)
    except:
        return stations[:9]
    nearest = []
    for station in stations:
        longitude = quartier[0]['gps_coordinates']['longitude']
        latitude = quartier[0]['gps_coordinates']['latitude']
        

        distance = ((longitude - station.longitude) ** 2 + (latitude - station.latitude) ** 2) ** 0.5
        nearest.append((station, distance)) 

        
    nearest.sort(key=lambda x: x[1])
    nearest = [n for n in nearest if n[1] != 0]
    print(longitude, latitude)
    result = []
    for n in nearest[:9]:
        result.append(n[0])
    return result

"""stations = Station().Get_all()
nearest = get_nearest_stations(stations, quarter= 'Nkomo')
for n in nearest:
    print(n[0].title, n[1])"""
#print(get_nearest_stations(stations))

"""stations = get_stations_quartier(ville = 'Yaounde', quartier = 'Nkoldongo')
for station in stations:
    try :
        if 'hours' not in station:
            station['hours'] = 'Non disponible'
        s = Station(
            ville = 'Yaounde',
            title = station['title'],
            address = station['address'],
            tel = station['phone'],
            longitude = station['gps_coordinates']['longitude'],
            latitude = station['gps_coordinates']['latitude'],
            localisation = station['links']['directions'],
            hours = station['hours'],
            stock = 'disponible',
            password = generate_password_hash('1234')
        )
    except KeyError:
        s = Station(
            ville = 'Yaounde',
            title = station['title'],
            address = station['address'],
            tel = 'Non disponible',
            longitude = station['gps_coordinates']['longitude'],
            latitude = station['gps_coordinates']['latitude'],
            localisation = station['links']['directions'],
            hours = station['hours'],
            stock = 'disponible',
            password = generate_password_hash('1234')
        )
        print('KeyError: phone')
    s.Add_station()"""