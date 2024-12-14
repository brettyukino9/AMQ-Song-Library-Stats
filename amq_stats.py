import json
import pandas as pd
with open('amq_stats.json', 'rb') as file:
    data = json.load(file)

data_list = pd.DataFrame(columns=['song', 'artist', 'type', 'anime', 'plays', 'correct count', 'percentage'])
list = []
for songid in data:
    entry = data[songid]
    song = entry['name']
    artist = entry['artist']
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
    print(song, artist, anime, plays, correct_count, percentage)
    list.append([song, artist, anime, plays, correct_count, percentage])

data_list = pd.DataFrame(list, columns=['song', 'artist', 'anime', 'plays', 'correct count', 'percentage'])
data_list = data_list.sort_values(by='plays', ascending=False)
data_list.to_csv('amq_stats.csv', index=False)


total_entries = len(data_list)
# amount of entires with percentage above 80
above_80 = len(data_list[data_list['percentage'] >= 80])
unlearned = len(data_list[(data_list['percentage'] < 80) & (data_list['plays'] > 0)])
unplayed = len(data_list[data_list['plays'] == 0])

print(f'Total entries: {total_entries}')
print(f'Learned entries (>80%): {above_80 / total_entries * 100}%')
print(f'Unlearned entries (<80%): {unlearned / total_entries * 100}%')
print(f'Unplayed entries: {unplayed / total_entries * 100}%')

openings = data_list[data_list['song'].str.contains('OP')]


# group data_list by anime
data_list_anime = data_list.groupby('anime').agg({'plays': 'sum', 'correct count': 'sum'}).reset_index()
data_list_anime['percentage'] = (data_list_anime['correct count'] / data_list_anime['plays']) * 100
data_list_anime = data_list_anime.sort_values(by='percentage', ascending=False)
data_list_anime.to_csv('amq_stats_anime.csv', index=False)

data_list_anime_unlearned = data_list_anime[data_list_anime['percentage'] < 60]
data_list_anime_unlearned = data_list_anime_unlearned.sort_values(by='plays', ascending=False)
data_list_anime_unlearned.to_csv('amq_anime_to_learn.csv', index=False)

# group data_list by artist
data_list_artist = data_list.groupby('artist').agg({'plays': 'sum', 'correct count': 'sum'}).reset_index()
data_list_artist['percentage'] = (data_list_artist['correct count'] / data_list_artist['plays']) * 100
data_list_artist = data_list_artist.sort_values(by='plays', ascending=False)
data_list_artist.to_csv('amq_stats_artist.csv', index=False)

unlearned_df = data_list[(data_list['percentage'] < 50) & (data_list['plays'] > 0)]
unlearned_df = unlearned_df.sort_values(by='plays', ascending=False)
unlearned_df.to_csv('amq_songs_to_learn.csv', index=False)