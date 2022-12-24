from argparse import ArgumentParser
from os.path import join, exists, abspath, basename
from pathlib import Path



def main():
    # Argument parser
    parser = ArgumentParser(description='Decode a text file using the Huffman algorithm')
    parser.add_argument('inputFile', type=str, help='Input file before decoding')
    parser.add_argument('outputFile', type=str, help='Output file after decoding')
    args = parser.parse_args()


    inputFileName = basename(args.inputFile).split('.')[0]
    inputPath = abspath( join(args.inputFile, "..") )

    outputPath = abspath( join(args.outputFile, "..") )

    jsonOrPickele = True


    if not exists(args.inputFile):
        print(f"file {args.inputFile} not found")
        return 0


    if not exists(join(inputPath, f"{inputFileName}." + "json" if jsonOrPickele else "pickle" )):
        print(inputFileName)
        print(f"file {join(inputPath, f'{inputFileName}.' + 'json' if jsonOrPickele else 'pickle')} not found")
        return 0


    with open(args.inputFile, "rb") as file:
        bytess = file.read()

    if jsonOrPickele:
        import json
        with open(join(inputPath, f"{inputFileName}.json"), 'r', encoding="utf-8") as file:
            decodeDict = json.load(file)
    else:
        import pickle
        with open(join(inputPath, f"{inputFileName}.pickle"), 'rb') as file:
            decodeDict = pickle.load(file)


    data = bin(int.from_bytes(bytess, 'big')).split('b')[1]

    # Decode
    decoded = ""
    key = ""
    decodeKeys = decodeDict.keys()
    for i in data[1:]:
        key += i
        if key in decodeKeys:
            decoded += decodeDict[key]
            key = ""

    if not exists(outputPath):
        Path( outputPath ).mkdir(parents=True, exist_ok=True)


    with open(args.outputFile, 'w', encoding="utf-8") as file:
        file.write(decoded)

if __name__ == "__main__":
    main()