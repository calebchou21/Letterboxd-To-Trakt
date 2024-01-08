import argparse
import authorize

from datetime import datetime
from CSVreader import CSVReader

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%m-%d-%Y')
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Use MM-DD-YYYY.")

def validate_csv_type(type):
    if type != 'diary' and type != 'watched':
        raise argparse.ArgumentTypeError("Invalid csv type. Use 'diary' or 'watched'.")
    return type
    
def parse_args(args):
    filename = args.f or (args.csv_type + '.csv' if args.csv_type else None)
    last_entered = args.last_entered or None
    csv_type = args.csv_type

    if csv_type == 'watched' and last_entered is not None:
        raise argparse.ArgumentError(None, "Last entered date should not be provided for 'watched' csv type.")
    
    reader = CSVReader(filename, last_entered)
    make_transfer(reader, csv_type)

def read_data(reader, csv_type):
    try:
        data = []
        if csv_type == 'watched':
            data = reader.read_watched(reader.filename)
        else:
            data = reader.read_diary(reader.filename)
        return data
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")

def make_transfer(reader, csv_type):
    data = read_data(reader, csv_type)
    print("Data successfully read from CSV.")
    print("Beginning Trakt.tv authentication progress.")
    authorize.authorize()
    print("Authentication successful, beginning data transfer.")
    
def main():
    parser = argparse.ArgumentParser(description='Letterboxd to Trakt.tv')

    parser.add_argument('csv_type', help ='Either `diary` or `watched`. Defines what type of data to transfer.', type=validate_csv_type)
    parser.add_argument('--f', help='CSV filename to read, if not specified defaults to <csv-type>.csv (this is the default name Letterboxd gives to exported CSV files)')
    parser.add_argument('--last_entered', help='Date of last movie logged on Letterboxd that was transfered to Trakt.tv in the format MM-DD-YYYY', type=validate_date)

    try:
        args = parser.parse_args()
        parse_args(args)
    except argparse.ArgumentError as e:
        print(f"ArgumentError: {e}")

if __name__ == "__main__":
    main()
