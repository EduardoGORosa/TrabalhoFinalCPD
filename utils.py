import struct
import read_csv_save_binary as rcsb
import heapq

STRUCT_BYTES = 216
INDEX_ID_BYTES = 8
INDEX_NAME_BYTES = 54
INDEX_GRADE_BYTES = 16

def insert_db():
    fields = input("Insira separado por virgula as seguintes informações do jogo: (id, nome, desenvolvedor, lançamento, gênero, positive_ratings, negative_ratings, average_playtime, median_playtime, owners, price)")
    game = fields.split(",")
    index = rcsb.get_quant_games('steam.bin') // STRUCT_BYTES

    def insert_in_steam():
        with open('steam.bin', 'ab') as bin_file:
            bin_file.seek(index*STRUCT_BYTES)
            packed_data = struct.pack('i50s50s10s50siiii30sf', 
                                        int(game[0]), game[1].encode(), game[2].encode(),
                                        game[3].encode(), game[4].encode(),
                                        int(game[5]), int(game[6]), int(game[7]),
                                        int(game[8]), game[9].encode(), round(float(game[10]),2))
            bin_file.write(packed_data)
    def insert_in_names():
        with open('names.bin', 'ab') as bin_file:
            bin_file.seek(index*INDEX_NAME_BYTES)
            packed_data = struct.pack('i50s', int(game[0]), game[1].encode())
            bin_file.write(packed_data)  
    def insert_in_ids():
        with open('ids.bin', 'ab') as bin_file:
            bin_file.seek(index*INDEX_ID_BYTES)
            packed_data = struct.pack('ii', index, int(game[0]))
            bin_file.write(packed_data)
    def insert_in_grades():
        with open('ids.bin', 'ab') as bin_file:
            bin_file.seek(index*INDEX_GRADE_BYTES)
            packed_data = struct.pack('iiif', int(game[0]), int(game[5]), int(game[6]), float(sum([int(x) for x in game[9].split("-")]) / 2))
            bin_file.write(packed_data)

    if len(game) == 11: 
        insert_in_steam()
        insert_in_names()
        insert_in_ids()
        insert_in_grades()
    else:
        print("Campos da estrutura jogo preenchidos incorretamente!")

def read_block(from_byte):

    with open('steam.bin', 'rb') as file:
        file.seek(from_byte)
        data = file.read(STRUCT_BYTES)
        unpacked_data = struct.unpack('i50s50s10s50siiii30sf', data)
        formated_data = {'id': int(unpacked_data[0]), 'info': (unpacked_data[1].decode('utf-8', errors='replace'), unpacked_data[2].decode('utf-8', errors='replace'), unpacked_data[3].decode('utf-8', errors='replace'),
                        unpacked_data[4].decode('utf-8', errors='replace'), unpacked_data[5], unpacked_data[7], unpacked_data[7], unpacked_data[8], 
                        unpacked_data[9].decode('utf-8', errors='replace'), round(float(unpacked_data[10]), 2))}
        game = formated_data

    show_game_info(game)

def search_by_best():
    games = []

    with open('grades.bin', 'rb') as file:
        quant_games = rcsb.get_quant_games('grades.bin') // INDEX_GRADE_BYTES

        for i in range(quant_games):
            file.seek(i * INDEX_GRADE_BYTES)
            data = file.read(INDEX_GRADE_BYTES)
            unpacked_data = struct.unpack('iiif', data)
            formated_data = {'id': int(unpacked_data[0]), 'grade': round(((int(unpacked_data[1]) - int(unpacked_data[2])) / float(unpacked_data[3])) * 1000, 2)}
            games.append(formated_data)

    best_grades = heapq.nlargest(10, games, key=lambda x: x['grade'])
    
    return best_grades


def search_by_name():
    name = input("Por qual jogo estás procurando? ")
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
    
    for i, game in enumerate(games_name):
        print(f"{i} - {game['name']}")
    print("Qual destes acima é o que estás buscando? ")
    search = -1
    while search < 0 or search > len(games_name):
        search = int(input("Digite o número do escolhido: "))
    return games_name[search]

def show_game_info(game):
    print("")
    print(f"id: {game['id']}")
    print(f"name: {game['info'][0]}")
    print(f"developer: {game['info'][1]}")
    print(f"release_date: {game['info'][2]}")
    print(f"genres: {game['info'][3]}")
    print(f"positive ratings: {game['info'][4]}")
    print(f"negative ratings: {game['info'][5]}")
    print(f"average playtime: {game['info'][6]}")
    print(f"median playtime: {game['info'][7]}")
    print(f"owners: {game['info'][8]}")
    print(f"price: {game['info'][9]}")