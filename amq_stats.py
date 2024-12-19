import json
import pandas as pd
with open('amq_stats-nick.json', 'rb') as file:
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
data_list.to_csv('amq_stats_songs.csv', index=False)


total_entries = len(data_list)
percentage_method = 0
if not percentage_method: #default
    # amount of entires with percentage above 70
    learned = data_list[data_list['percentage'] >= 70]
    unlearned = data_list[(data_list['percentage'] < 70) & (data_list['plays'] > 0)]
    unplayed = data_list[data_list['plays'] == 0]
else: # 1 - use recent percentage
    # alternative method using recent percentage
    learned = data_list[data_list['recent percentage'] >= 70]
    unlearned = data_list[~((data_list['plays'] == 0) & (data_list['recent percentage'] == 0)) & (data_list['recent percentage'] < 70)]
    unplayed = data_list[(data_list['plays'] == 0) & (data_list['recent percentage'] == 0)]


# Overall Stats
print("--------------------")
print(f'Total entries: {total_entries}')
print(f"Guess rate: {data_list['correct count'].sum()} / {data_list['plays'].sum()} {data_list['correct count'].sum() / data_list['plays'].sum() * 100}%")
print(f"Gettable %: {len(data_list[data_list['correct count'] > 0])} / {total_entries} {len(data_list[data_list['correct count'] > 0]) / total_entries * 100}%")
print(f'Learned entries (>70%): {len(learned)} / {total_entries} {len(learned) / total_entries * 100}%')
print(f'Unlearned entries (<70%): {len(unlearned)} / {total_entries} {len(unlearned) / total_entries * 100}%')
print(f'Unplayed entries: {len(unplayed)} / {total_entries} {len(unplayed) / total_entries * 100}%')
print("--------------------")
# OP / ED / IN Stats
openings = data_list[data_list['type'] == 'OP']
endings = data_list[data_list['type'] == 'ED']
inserts = data_list[data_list['type'] == 'IN']

## Openings
print("Openings: ", len(openings))
print(f"Openings guess rate %: {openings['correct count'].sum()} / {openings['plays'].sum()}", openings['correct count'].sum() / openings['plays'].sum() * 100)
print(f"Openings gettable %: {len(openings[openings['correct count'] > 0])} / {len(openings)} ", len(openings[openings['correct count'] > 0]) / len(openings) * 100)
print(f"Openings learned %: {len(learned[learned['type'] == 'OP'])} / {len(openings)} ", len(learned[learned['type'] == 'OP']) / len(openings) * 100)
print("Openings unlearned %: ", len(unlearned[unlearned['type'] == 'OP']) / len(openings) * 100)
print("Openings unplayed %: ", len(unplayed[unplayed['type'] == 'OP']) / len(openings) * 100)
op_under_30 = openings[openings['diff'] < 30]
print(f"Openings under 30 guess rate %: {op_under_30['correct count'].sum()} / {op_under_30['plays'].sum()} ", op_under_30['correct count'].sum() / op_under_30['plays'].sum() * 100)
print(f"Openings under 30 gettable %: {len(op_under_30[op_under_30['correct count'] > 0])} / {len(op_under_30)} ", len(op_under_30[op_under_30['correct count'] > 0]) / len(op_under_30) * 100)
print(f"Openings under 30 learned %: {len(learned[(learned['type'] == 'OP') & (learned['diff'] < 30)])} / {len(op_under_30)}", len(learned[(learned['type'] == 'OP') & (learned['diff'] < 30)]) / len(op_under_30) * 100)
print("Openings under 30 unlearned %: ", len(unlearned[(unlearned['type'] == 'OP') & (unlearned['diff'] < 30)]) / len(op_under_30) * 100)
print("Openings under 30 unplayed %: ", len(unplayed[(unplayed['type'] == 'OP') & (unplayed['diff'] < 30)]) / len(op_under_30) * 100)
print("--------------------")

## Endings
print("Endings: ", len(endings))
print(f"Endings guess rate %: {endings['correct count'].sum()} / {endings['plays'].sum()} ", endings['correct count'].sum() / endings['plays'].sum() * 100)
print(f"Endings gettable %: {len(endings[endings['correct count'] > 0])} / {len(endings)} ", len(endings[endings['correct count'] > 0]) / len(endings) * 100)
print(f"Endings learned %: {len(learned[learned['type'] == 'ED'])} / {len(endings)} ", len(learned[learned['type'] == 'ED']) / len(endings) * 100)
print("Endings unlearned %: ", len(unlearned[unlearned['type'] == 'ED']) / len(endings) * 100)
print("Endings unplayed %: ", len(unplayed[unplayed['type'] == 'ED']) / len(endings) * 100)
end_under_30 = endings[endings['diff'] < 30]
print(f"Endings under 30 guess rate %: {end_under_30['correct count'].sum()} / {end_under_30['plays'].sum()} ", end_under_30['correct count'].sum() / end_under_30['plays'].sum() * 100)
print(f"Endings under 30 gettable %: {len(end_under_30[end_under_30['correct count'] > 0])} / {len(end_under_30)} ", len(end_under_30[end_under_30['correct count'] > 0]) / len(end_under_30) * 100)
print(f"Endings under 30 learned %: {len(learned[(learned['type'] == 'ED') & (learned['diff'] < 30)])} / {len(end_under_30)}", len(learned[(learned['type'] == 'ED') & (learned['diff'] < 30)]) / len(end_under_30) * 100)
print("Endings under 30 unlearned %: ", len(unlearned[(unlearned['type'] == 'ED') & (unlearned['diff'] < 30)]) / len(end_under_30) * 100)
print("Endings under 30 unplayed %: ", len(unplayed[(unplayed['type'] == 'ED') & (unplayed['diff'] < 30)]) / len(end_under_30) * 100)
print("--------------------")

## Inserts
print("Inserts: ", len(inserts))
print(f"Inserts guess rate %: {inserts['correct count'].sum()} / {inserts['plays'].sum()}", inserts['correct count'].sum() / inserts['plays'].sum() * 100)
print(f"Inserts gettable %: {len(inserts[inserts['correct count'] > 0])} / {len(inserts)} ", len(inserts[inserts['correct count'] > 0]) / len(inserts) * 100)
print(f"Inserts learned %: {len(learned[learned['type'] == 'IN'])} / {len(inserts)} ", len(learned[learned['type'] == 'IN']) / len(inserts) * 100)
print("Inserts unlearned %: ", len(unlearned[unlearned['type'] == 'IN']) / len(inserts) * 100)
print("Inserts unplayed %: ", len(unplayed[unplayed['type'] == 'IN']) / len(inserts) * 100)
in_under_30 = inserts[inserts['diff'] < 30]
print(f"Inserts under 30 guess rate %: {in_under_30['correct count'].sum()} / {in_under_30['plays'].sum()} ", in_under_30['correct count'].sum() / in_under_30['plays'].sum() * 100)
print(f"Inserts under 30 gettable %: {len(in_under_30[in_under_30['correct count'] > 0])} / {len(in_under_30)} ", len(in_under_30[in_under_30['correct count'] > 0]) / len(in_under_30) * 100)
print(f"Inserts under 30 learned %: {len(learned[(learned['type'] == 'IN') & (learned['diff'] < 30)])} / {len(in_under_30)}", len(learned[(learned['type'] == 'IN') & (learned['diff'] < 30)]) / len(in_under_30) * 100)
print("Inserts under 30 unlearned %: ", len(unlearned[(unlearned['type'] == 'IN') & (unlearned['diff'] < 30)]) / len(in_under_30) * 100)
print("Inserts under 30 unplayed %: ", len(unplayed[(unplayed['type'] == 'IN') & (unplayed['diff'] < 30)]) / len(in_under_30) * 100)
print("--------------------")
# Under 30 stats overall
under_30_songs = data_list[data_list['diff'] < 30]
print(f"under 30 overall guess rate %: {under_30_songs['correct count'].sum()} / {under_30_songs['plays'].sum()} ", under_30_songs['correct count'].sum() / under_30_songs['plays'].sum() * 100)
print(f"under 30 overall gettable %: {len(under_30_songs[under_30_songs['correct count'] > 0])} / {len(under_30_songs)} ", len(under_30_songs[under_30_songs['correct count'] > 0]) / len(under_30_songs) * 100)
print(f"under 30 overall  learned %: {len(learned[(learned['diff'] < 30)])} / {len(under_30_songs)}", len(learned[(learned['diff'] < 30)]) / len(under_30_songs) * 100)
print("under 30 overall  unlearned %: ", len(unlearned[(unlearned['diff'] < 30)]) / len(under_30_songs) * 100)
print("under 30 overall  unplayed %: ", len(unplayed[(unplayed['diff'] < 30)]) / len(under_30_songs) * 100)

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

# Not Known Songs
not_known_df = data_list[(data_list['correct count'] == 0) & (data_list['plays'] > 0)]
not_known_df = not_known_df.sort_values(by='plays', ascending=False)
not_known_df.to_csv('amq_songs_never_got.csv', index=False)