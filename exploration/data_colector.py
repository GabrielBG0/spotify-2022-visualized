import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ID",
                                                           client_secret="Secret"))

results = sp.playlist_tracks('37i9dQZF1DX18jTM2l2fJY')

results = results["items"]

for i in range(len(results)):
    for key in list(results[i].keys()):
        if key != "track":
            results[i].pop(key)

r_ids = []
pre_info = {}
for result in results:
    r_ids.append(result['track']["id"])
    pre_info.update({result['track']["id"]: {"name": result['track']
                                             ["name"], "popularity": result['track']["popularity"]}})

features = sp.audio_features(r_ids)

for feature in features:
    id = feature["id"]
    feature.pop('type')
    feature.pop('uri')
    feature.pop('track_href')
    feature.pop('analysis_url')
    pre_info[id].update({"features": feature})

final_info = []


position = 1
for info in pre_info.values():
    aux = {
        "position": position
    }
    aux.update({'name': info['name']})
    aux.update({'popularity': info['popularity']})
    for key, feature in info['features'].items():
        aux.update({key: feature})

    final_info.append(aux)

    position += 1

df = pd.DataFrame.from_dict(final_info)

df.to_csv('top_songs_2022.csv', index=False)


# for key in keys:
#     if key != "tracks":
#         results.pop(key)

# print(results["tracks"].keys())
