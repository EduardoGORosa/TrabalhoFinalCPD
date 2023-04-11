import bTree
import read_csv_save_binary as rcsb
import utils

ORDER = 1000
STRUCT_BYTES = 216
INDEX_ID_BYTES = 8
INDEX_NAME_BYTES = 54
INDEX_GRADE_BYTES = 16

def main():
    btree = bTree.BTree(order=ORDER)
    games = rcsb.read_from_index_file()

    for i,game in enumerate(games):
        btree.insert(game)

    menu(btree)

def menu(btree):
    choice = -1
    while choice < 1 or choice > 3:
        print("1 - Ver o top 10 jogos mais bem avaliados")
        print("2 - Procurar informações de um jogo")
        print("3 - Inserir um jogo na base de dados")

        choice = int(input("Escolha uma ação: "))

    if choice == 1:
        best_grades = utils.search_by_best()
        for grade in best_grades:
            keys = btree.search(grade['id']).keys
            for k in keys:
                if grade['id'] == k[1]:
                    byte = k[0]
                    break
                else:
                    byte = None
            if byte != 0:
                utils.read_block(byte * STRUCT_BYTES)
    elif choice == 2:
        game = utils.search_by_name()
        keys = btree.search(game['id']).keys
        for k in keys:
            if game['id'] == k[1]:
                byte = k[0]
                break
            else:
                byte = None
        if byte != 0:
            utils.read_block(byte * STRUCT_BYTES)
    else:
        utils.insert_db()
if __name__ == '__main__':
    main()