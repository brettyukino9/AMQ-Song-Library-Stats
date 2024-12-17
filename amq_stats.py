import json
import pandas as pd
with open('amq_stats2.json', 'rb') as file:
    data = json.load(file)

types = ['OP', 'ED', 'IN']

data_list = pd.DataFrame(columns=['song', 'artist', 'diff', 'anime', 'type', 'plays', 'correct count', 'percentage', 'recent percentage'])
list = []
for songid in data:
    entry = data[songid]
    song = entry['name']
    artist = entry['artist']
    diff = entry['globalPercent']
    type = types[entry['type'] - 1]
    last_eight = entry['recentPercent']
    for animeid in entry['anime']:
        anime_id_names = entry['anime'][animeid]['names']
        anime = anime_id_names['EN'] if anime_id_names['EN'] else anime_id_names['JA']
    try:
        correct_count = 0 if entry['totalCorrectCount'] is None else int(entry['totalCorrectCount'])
    except:
        print(entry)
        break
    wrong_count = 0 if entry['totalWrongCount'] is None else int(entry['totalWrongCount'])
    plays = correct_count + wrong_count
    percentage = 0 if plays == 0 else (correct_count / plays) * 100
    print(song, artist, diff, anime, type, plays, correct_count, percentage, last_eight)
    list.append([song, artist, diff, anime, type, plays, correct_count, percentage, last_eight])

data_list = pd.DataFrame(list, columns=['song', 'artist', 'diff','anime', 'type','plays', 'correct count', 'percentage', 'recent percentage'])
data_list = data_list.sort_values(by='plays', ascending=False)
data_list.to_csv('amq_stats.csv', index=False)


total_entries = len(data_list)
# amount of entires with percentage above 80
above_80 = len(data_list[data_list['percentage'] >= 80])
unlearned = len(data_list[(data_list['percentage'] < 80) & (data_list['plays'] > 0)])
unplayed = len(data_list[data_list['plays'] == 0])

# alternative method using recent percentage
# above_70 = len(data_list[data_list['recent percentage'] >= 70])
# unlearned = len(data_list[~((data_list['plays'] == 0) & (data_list['recent percentage'] == 0)) & (data_list['recent percentage'] < 70)])
# unplayed = len(data_list[(data_list['plays'] == 0) & (data_list['recent percentage'] == 0)])


# Overall Stats
print(f'Total entries: {total_entries}')
print(f"Guess rate: {data_list['correct count'].sum() / data_list['plays'].sum() * 100}%")
print(f'Learned entries (>80%): {above_80 / total_entries * 100}%')
print(f'Unlearned entries (<80%): {unlearned / total_entries * 100}%')
print(f'Unplayed entries: {unplayed / total_entries * 100}%')

# OP / ED / IN Stats
openings = data_list[data_list['type'] == 'OP']
endings = data_list[data_list['type'] == 'ED']
inserts = data_list[data_list['type'] == 'IN']

## Openings
print("Openings: ", len(openings))
print("Openings guess rate %: ", openings['correct count'].sum() / openings['plays'].sum() * 100)
print("Openings learned %: ", len(openings[openings['percentage'] >= 80]) / len(openings) * 100)
print("Openings unlearned %: ", len(openings[(openings['percentage'] < 80) & (openings['plays'] > 0)]) / len(openings) * 100)
print("Openings unplayed %: ", len(openings[openings['plays'] == 0]) / len(openings) * 100)
op_under_30 = openings[openings['diff'] < 30]
print("under 30 guess rate %: ", op_under_30['correct count'].sum() / op_under_30['plays'].sum() * 100)
print("under 30 openings learned %: ", len(op_under_30[op_under_30['percentage'] >= 80]) / len(op_under_30) * 100)
print("under 30 openings unlearned %: ", len(op_under_30[(op_under_30['percentage'] < 80) & (op_under_30['plays'] > 0)]) / len(op_under_30) * 100)
print("under 30 openings unplayed %: ", len(op_under_30[op_under_30['plays'] == 0]) / len(op_under_30) * 100)

## Endings
print("Endings: ", len(endings))
print("Endings guess rate %: ", endings['correct count'].sum() / endings['plays'].sum() * 100)
print("Endings learned %: ", len(endings[endings['percentage'] >= 80]) / len(endings) * 100)
print("Endings unlearned %: ", len(endings[(endings['percentage'] < 80) & (endings['plays'] > 0)]) / len(endings) * 100)
print("Endings unplayed %: ", len(endings[endings['plays'] == 0]) / len(endings) * 100)
end_under_30 = endings[endings['diff'] < 30]
print("under 30 guess rate %: ", end_under_30['correct count'].sum() / end_under_30['plays'].sum() * 100)
print("under 30 endings learned %: ", len(end_under_30[end_under_30['percentage'] >= 80]) / len(end_under_30) * 100)
print("under 30 endings unlearned %: ", len(end_under_30[(end_under_30['percentage'] < 80) & (end_under_30['plays'] > 0)]) / len(end_under_30) * 100)
print("under 30 endings unplayed %: ", len(end_under_30[end_under_30['plays'] == 0]) / len(end_under_30) * 100)

## Inserts
print("Inserts: ", len(inserts))
print("Inserts guess rate %: ", inserts['correct count'].sum() / inserts['plays'].sum() * 100)
print("Inserts learned %: ", len(inserts[inserts['percentage'] >= 80]) / len(inserts) * 100)
print("Inserts unlearned %: ", len(inserts[(inserts['percentage'] < 80) & (inserts['plays'] > 0)]) / len(inserts) * 100)
print("Inserts unplayed %: ", len(inserts[inserts['plays'] == 0]) / len(inserts) * 100)
in_under_30 = inserts[inserts['diff'] < 30]
print("under 30 guess rate %: ", in_under_30['correct count'].sum() / in_under_30['plays'].sum() * 100)
print("under 30 inserts learned %: ", len(in_under_30[in_under_30['percentage'] >= 80]) / len(in_under_30) * 100)
print("under 30 inserts unlearned %: ", len(in_under_30[(in_under_30['percentage'] < 80) & (in_under_30['plays'] > 0)]) / len(in_under_30) * 100)
print("under 30 inserts unplayed %: ", len(in_under_30[in_under_30['plays'] == 0]) / len(in_under_30) * 100)

# Under 30 stats overall
under_30_songs = data_list[data_list['diff'] < 30]
print("\n")
print("under 30 overall guess rate %: ", under_30_songs['correct count'].sum() / under_30_songs['plays'].sum() * 100)
print("under 30 songs learned %: ", len(under_30_songs[under_30_songs['percentage'] >= 80]) / len(under_30_songs) * 100)
print("under 30 songs unlearned %: ", len(under_30_songs[(under_30_songs['percentage'] < 80) & (under_30_songs['plays'] > 0)]) / len(under_30_songs) * 100)
print("under 30 songs unplayed %: ", len(under_30_songs[under_30_songs['plays'] == 0]) / len(under_30_songs) * 100)

# # print the under 30 songs in order of plays
# under_30_songs = under_30_songs.sort_values(by='plays', ascending=False)
# under_30_songs.to_csv('amq_under_30.csv', index=False)

openings = data_list[data_list['song'].str.contains('OP')]


# Anime Stats
data_list_anime = data_list.groupby('anime').agg({'plays': 'sum', 'correct count': 'sum'}).reset_index()
data_list_anime['percentage'] = (data_list_anime['correct count'] / data_list_anime['plays']) * 100
data_list_anime = data_list_anime.sort_values(by='plays', ascending=False)
data_list_anime.to_csv('amq_stats_anime.csv', index=False)
data_list_anime_unlearned = data_list_anime[data_list_anime['percentage'] < 60]
data_list_anime_unlearned = data_list_anime_unlearned.sort_values(by='plays', ascending=False)
data_list_anime_unlearned.to_csv('amq_anime_to_learn.csv', index=False)

# Artist Stats
data_list_artist = data_list.groupby('artist').agg({'plays': 'sum', 'correct count': 'sum'}).reset_index()
data_list_artist['percentage'] = (data_list_artist['correct count'] / data_list_artist['plays']) * 100
data_list_artist = data_list_artist.sort_values(by='plays', ascending=False)
data_list_artist.to_csv('amq_stats_artist.csv', index=False)

# Unlearned Songs
unlearned_df = data_list[(data_list['percentage'] < 50) & (data_list['plays'] > 0)]
unlearned_df = unlearned_df.sort_values(by='plays', ascending=False)
unlearned_df.to_csv('amq_songs_to_learn.csv', index=False)