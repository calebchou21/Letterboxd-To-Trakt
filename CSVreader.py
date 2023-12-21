import csv
from datetime import datetime, timedelta

class CSVReader:
    def __init__(self, filename, last_entered_date = None):
        self.filename = filename
        self.last_entered_date = None
        if last_entered_date != None:
            self.last_entered_date = last_entered_date + timedelta(days=1)

    def read_watched(self, filename):
        data = []
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            # Skip header
            next(csvreader, None)
            for row in csvreader:
                date, name, year, letterboxd_uri = row
                data.append({
                    'date': date,
                    'name': name,
                    'year': year,
                    'uri': letterboxd_uri
                })
        return data

    def read_diary(self, filename):
        data = []
       
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            # Skip header
            next(csvreader, None)
            for row in csvreader:
                # If a last entered date is specified, skip rows until we have a greater date
                if self.last_entered_date is not None:
                    date_str = row[7]  
                    row_date = datetime.strptime(date_str, '%Y-%m-%d')  
                    if row_date <= self.last_entered_date:
                        continue  
                   
                # We get diary data here
                date, name, year, letterboxd_uri, rating, rewatch, tags, watched_date = row
                data.append({
                    'date': date,
                    'name': name,
                    'year': year,
                    'uri': letterboxd_uri,
                    'rating': rating,
                    'rewatch': rewatch,
                    'tags': tags,
                    'watched_date': watched_date
                })
        return data