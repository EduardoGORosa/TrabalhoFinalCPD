import struct
import bTree
import read_csv_save_binary as rcsb

STRUCT_BYTES = 216
INDEX_ID_BYTES = 8
INDEX_NAME_BYTES = 54

def main():
    btree = bTree.BTree(order=1000)
    games = rcsb.read_from_index_file()

    for i,game in enumerate(games):
        btree.insert(game)

    #insert_db()
    search_by_name()
    # byte = btree.search(1069460)
    # print(byte.keys)
    #read_block(byte.keys[0][0], STRUCT_BYTES)

def read_block(from_byte, block_size):
    games = []
    with open('steam.bin', 'rb') as file:
        for i in range(block_size):
            file.seek(from_byte + i*STRUCT_BYTES)
            data = file.read(STRUCT_BYTES)
            unpacked_data = struct.unpack('i50s50s10s50siiii30sf', data)
            formated_data = {'id': unpacked_data[0], 'info': (unpacked_data[1].decode('utf-8', errors='replace'), unpacked_data[2].decode('utf-8', errors='replace'), unpacked_data[3].decode('utf-8', errors='replace'),
                            unpacked_data[4].decode('utf-8', errors='replace'), unpacked_data[5], unpacked_data[7], unpacked_data[7], unpacked_data[8], 
                            unpacked_data[9].decode('utf-8', errors='replace'), round(float(unpacked_data[10]), 2))}
            games.append(formated_data)

#def search_by_id():


def search_by_name():
    name = input("Por qual jogo estás procurando?")
    games = []
    games_name = []
    with open('names.bin', 'rb') as file:     
        quant_games = rcsb.get_quant_games('names.bin') // INDEX_NAME_BYTES

        for i in range(quant_games):
            file.seek(i*INDEX_NAME_BYTES)
            data = file.read(INDEX_NAME_BYTES)
            unpacked_data = struct.unpack('i50s', data)
            games.append({'name': unpacked_data[1].decode('utf-8', errors='replace'), 'id': unpacked_data[0]})
    
    for game in games:
        if name in game['name']:
            games_name.append(game)
    
    for game in games_name:
        print(game['name'], game['id'])


def insert_db():
    fields = input("Insira separado por virgula as seguintes informações do jogo: (id, nome, desenvolvedor, lançamento, gênero, positive_ratings, negative_ratings, average_playtime, median_playtime, owners, price)")
    game = fields.split(",").strip()
    index = rcsb.get_quant_games('steam.bin') // STRUCT_BYTES

    def insert_in_steam():
        with open('steam.bin', 'wb') as bin_file:
            packed_data = struct.pack('i50s50s10s50siiii30sf', 
                                        int(game[0]), game[1].encode(), game[2].encode(),
                                        game[3].encode(), game[4].encode(),
                                        int(game[5]), int(game[6]), int(game[7]),
                                        int(game[8]), game[9].encode(), round(float(game[10]),2))
            bin_file.write(packed_data)
    def insert_in_names():
        with open('names.bin', 'wb') as bin_file:
            packed_data = struct.pack('i50s', int(game[0]), game[1].encode())
            bin_file.write(packed_data)  
    def insert_in_ids():
        with open('ids.bin', 'wb') as bin_file:
            packed_data = struct.pack('ii', index, int(game[0]))
            bin_file.write(packed_data)

    print(game)
    if len(game) == 11: 
        insert_in_steam()
        insert_in_names()
        insert_in_ids()
    else:
        print("Campos da estrutura jogo preenchidos incorretamente!")

if __name__ == '__main__':
    main()