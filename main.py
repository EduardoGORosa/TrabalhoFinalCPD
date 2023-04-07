import csv
import struct
import bTree

test = ["Teste", "Teste2", "Teste3", "Teste4", "Teste5", "Teste6"]

def main():
    with open('index.bin', 'wb') as file:
        for i,name in enumerate(test):
            data = (i, name)
            structured_data = struct.pack("i10s", data[0], data[1].encode())
            file.write(structured_data)

if __name__ == '__main__':
    main()