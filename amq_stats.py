import json
import pandas as pd
with open('amq_stats.json', 'rb') as file:
    data = json.load(file)

data_list = pd.DataFrame(columns=['song', 'artist', 'diff', 'anime', 'plays', 'correct count', 'percentage', 'recent percentage'])
list = []
for songid in data:
    entry = data[songid]
    song = entry['name']
    artist = entry['artist']
    diff = entry['globalPercent']
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
    print(song, artist, diff, anime, plays, correct_count, percentage, last_eight)
    list.append([song, artist, diff, anime, plays, correct_count, percentage, last_eight])

data_list = pd.DataFrame(list, columns=['song', 'artist', 'diff','anime', 'plays', 'correct count', 'percentage', 'recent percentage'])
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


print(f'Total entries: {total_entries}')
print(f"Guess rate: {data_list['correct count'].sum() / data_list['plays'].sum() * 100}%")
print(f'Learned entries (>80%): {above_80 / total_entries * 100}%')
print(f'Unlearned entries (<80%): {unlearned / total_entries * 100}%')
print(f'Unplayed entries: {unplayed / total_entries * 100}%')


print("\n")
under_30_songs = data_list[data_list['diff'] < 30]
print("under 30 guess rate %: ", under_30_songs['correct count'].sum() / under_30_songs['plays'].sum() * 100)
print("under 30 songs learned %: ", len(under_30_songs[under_30_songs['percentage'] >= 80]) / len(under_30_songs) * 100)
print("under 30 songs unlearned %: ", len(under_30_songs[(under_30_songs['percentage'] < 80) & (under_30_songs['plays'] > 0)]) / len(under_30_songs) * 100)
print("under 30 songs unplayed %: ", len(under_30_songs[under_30_songs['plays'] == 0]) / len(under_30_songs) * 100)

# # print the under 30 songs in order of plays
# under_30_songs = under_30_songs.sort_values(by='plays', ascending=False)
# under_30_songs.to_csv('amq_under_30.csv', index=False)

openings = data_list[data_list['song'].str.contains('OP')]


# group data_list by anime
data_list_anime = data_list.groupby('anime').agg({'plays': 'sum', 'correct count': 'sum'}).reset_index()
data_list_anime['percentage'] = (data_list_anime['correct count'] / data_list_anime['plays']) * 100
data_list_anime = data_list_anime.sort_values(by='plays', ascending=False)
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