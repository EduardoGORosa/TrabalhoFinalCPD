import csv
import struct
import os

STRUCT_BYTES = 216
INDEX_ID_BYTES = 8
INDEX_NAME_BYTES = 54

games = []

def get_quant_games(file):
    
    file_size = os.path.getsize(file)

    return file_size


def read_from_csv_file():
    with open('steam.csv', 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        packed_data = b''
        for row in csv_reader:
            games.append(row)
        
    return games


def write_into_b_file():
    with open('steam.bin', 'wb') as bin_file:
        for game in games:
            packed_data = struct.pack('i50s50s10s50siiii30sf', 
                                        int(game['appid']), game['name'].encode(), game['developer'].encode(),
                                        game['release_date'].encode(), game['genres'].encode(),
                                        int(game['positive_ratings']), int(game['negative_ratings']), int(game['average_playtime']),
                                        int(game['median_playtime']), game['owners'].encode(), round(float(game['price']),2))
            bin_file.write(packed_data)

def index_file_position_id():
    with open('ids.bin', 'wb') as bin_file:
        for i,game in enumerate(games):
            packed_data = struct.pack('ii', i, int(game['appid']))
            bin_file.write(packed_data)

def index_file_id_name():
    with open('names.bin', 'wb') as bin_file:
        for i,game in enumerate(games):
            packed_data = struct.pack('i50s', int(game['appid']), game['name'].encode())
            bin_file.write(packed_data)
        
def read_from_index_file():
    index_games = []
    with open('ids.bin', 'rb') as file:     
        games = get_quant_games('ids.bin') // INDEX_ID_BYTES
        for i in range(games):
            file.seek(i*INDEX_ID_BYTES)
            data = file.read(INDEX_ID_BYTES)
            unpacked_data = struct.unpack('ii', data)
            index_games.append(unpacked_data)

    return index_games
