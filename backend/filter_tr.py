import csv

with open('../data/universal_top_spotify_songs.csv', encoding='utf-8') as inp, \
     open('../data/tr_top_spotify_songs.csv', 'w', newline='', encoding='utf-8') as out:
    reader = csv.reader(inp)
    writer = csv.writer(out)
    header = next(reader)
    writer.writerow(header)
    country_idx = header.index('country')
    count = 0
    for row in reader:
        if row[country_idx] == 'TR':
            writer.writerow(row)
            count += 1
    print('Kaydedildi:', count, 'satir')