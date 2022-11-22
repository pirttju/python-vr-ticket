import os.path
import sys
from docbarcodes.extract import process_document
from ssbdata import SSBData

"""
def to_bitstring(string):
    formatted_string = "".join("{0:08b}".format(x, "b") for x in bytearray(string, "iso-8859-1"))
    return formatted_string
"""


def extract_barcodes(filename):
    barcodes_raw, barcodes_combined = process_document(filename)
    return [b._asdict() for b in barcodes_raw]


def process_ticket_image(path_to_file):
    if os.path.exists(path_to_file):
        barcodes = extract_barcodes(path_to_file)
        for code in barcodes:
            raw = code.get("raw")
            raw_bytes = bytes(raw, encoding="iso-8859-1")
            data = SSBData(raw_bytes)
            print(data.__dict__)
    else:
        print(f"Error: File {path_to_file} does not exist!")


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "-i":
        process_ticket_image(args[1])
    else:
        print("Usage: vr-ticket -i <image>")


if __name__ == "__main__":
    main()
