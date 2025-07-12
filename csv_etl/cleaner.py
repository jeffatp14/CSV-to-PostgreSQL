import re
import csv
import pandas as pd
from csv_etl.config import Config

class Cleaner():
    def __init__(self):
        pass

    def clean_raw(self, filepath):
        with open(filepath, encoding='utf-8', errors='replace') as f:
            text = f.read()

        # csv.reader : parse correctly quoted multiline CSV
        reader = csv.reader(text.splitlines(), skipinitialspace=True)
        rows = list(reader)

        return rows

    def parse_raw(self,fields):
        if len(fields) < 9:
            fields += [None] * (9 - len(fields))  # pad missing fields

        movie_name = fields[0].strip()

        raw_year = fields[1].strip() if fields[1] else None
        if raw_year:
            raw_year = re.sub(r'\(I{1,3,}\)', '', raw_year).strip()
            year_match = re.search(r'\(?(\d{4}(?:–\d{4}|–)?)\)?', raw_year)
            year = year_match.group(1) if year_match else None
        else:
            year = None

        genre = [g.strip() for g in fields[2].split(',')] if fields[2] else []
        rating = float(fields[3]) if fields[3] and fields[3].replace('.', '', 1).isdigit() else None
        one_line = fields[4].strip() if fields[4] else None

        # Director & Stars block
        people_blob = fields[5] or ""
        people_blob = re.sub(r'\s+', ' ', people_blob.strip())
        director = None
        stars = []

        match = re.search(r'Director:\s*(.*?)\s*\|\s*Stars:\s*(.*)', people_blob)
        if match:
            director = match.group(1).strip()
            stars_raw = match.group(2)
        else:
            match = re.search(r'Stars:\s*(.*)', people_blob)
            stars_raw = match.group(1) if match else ""

        stars = [s.strip() for s in stars_raw.split(',') if s.strip()]

        # Parse votes, runtime, gross
        def clean_int(val):
            try:
                return int(val.replace(",", "")) if val else None
            except:
                return None

        def clean_float(val):
            try:
                val = val.replace('$', '').replace('M', '')  # $402.45M → 402.45
                return float(val) if val else None
            except:
                return None

        votes = clean_int(fields[6])
        runtime = clean_int(fields[7])
        gross = clean_float(fields[8])

        return {
            "movie_name": movie_name,
            "year": year,
            "genre": genre,
            "rating": rating,
            "one_line": one_line,
            "director": director,
            "stars": stars,
            "votes": votes,
            "runtime": runtime,
            "gross": gross
        }

    
    def remove_duplicate(self, clean_data):
        df = pd.DataFrame([{
            "movie_name": d["movie_name"],
            "year": d["year"],
            "genre": ", ".join(d["genre"]),
            "rating": d["rating"],
            "one_line": d["one_line"],
            "director": d["director"],
            "stars": ", ".join(d["stars"]),
            "votes": d["votes"],
            "runtime": d["runtime"],
            "gross": d["gross"]
        } for d in clean_data])
        df = df.loc[~df.duplicated(keep='first')]
        return df