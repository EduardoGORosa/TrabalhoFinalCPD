import csv
import struct
import os

STRUCT_BYTES = 316
INDEX_BYTES = 54

games = []


def get_quant_games(file):
    
    file_size = os.path.getsize(file)

    return file_size


def read_from_csv_file():
    # Open the CSV file in read mode
    with open('steam.csv', 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Pack the data from the CSV file into a binary string
        packed_data = b''
        for row in csv_reader:
            # Use the appropriate format string for each field
            games.append(row)
        
    return games


def write_into_b_file():
    # # Open a binary file in write mode
    with open('steam.bin', 'wb') as bin_file:
        # Write the packed binary string to the binary file
        for game in games:
            packed_data = struct.pack('i50s50s10s50s100siiii30sf', 
                                        int(game['appid']), game['name'].encode(), game['developer'].encode(),
                                        game['release_date'].encode(), game['genres'].encode(), game['steamspy_tags'].encode(),
                                        int(game['positive_ratings']), int(game['negative_ratings']), int(game['average_playtime']),
                                        int(game['median_playtime']), game['owners'].encode(), float(game['price']))
            bin_file.write(packed_data)

def read_from_b_file():
    # Open the CSV file in read mode
    with open('steam.bin', 'rb') as file:
        
        games = get_quant_games()
        file.seek(316 * 1000)
        data = file.read(316 * 1000)
            # Use the appropriate format string for each field
        unpacked_data = struct.unpack(1000 * 'i50s50s10s50s100siiii30sf', data)

        print(unpacked_data)
        print(unpacked_data[1].decode('utf-8', errors='replace'))

def index_file_id_name():
    #read_from_csv_file()

    with open('btree.bin', 'wb') as bin_file:
        for game in games:
            packed_data = struct.pack('i50s', int(game['appid']), game['name'].encode())
            bin_file.write(packed_data)
        
def read_from_index_file():
    # Open the CSV file in read mode
    with open('btree.bin', 'rb') as file:
        
        data = file.read(INDEX_BYTES)
            # Use the appropriate format string for each field
        unpacked_data = struct.unpack('i50s', data)

        #print(unpacked_data)

index_file_id_name()
#read_from_index_file()

