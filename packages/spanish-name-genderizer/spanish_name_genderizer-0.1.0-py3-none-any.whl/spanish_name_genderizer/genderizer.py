# genderizer.py

import csv
from pathlib import Path

class SpanishNameGenderizer:
    def __init__(self):
        self.name_data = self._load_name_data()

    def _load_name_data(self):
        data_path = Path(__file__).parent / 'data' / 'spanish_names.csv'
        name_data = {}
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['Name'].lower()
                name_data[name] = {
                    'Male_frequency': float(row['Male_frequency']),
                    'Female_frequency': float(row['Female_frequency'])
                }
        return name_data

    def genderize(self, name):
        name = name.lower()
        if '-' in name:
            first_name = name.split('-')[0]
        else:
            first_name = name.split()[0]

        if first_name in self.name_data:
            male_freq = self.name_data[first_name]['Male_frequency']
            female_freq = self.name_data[first_name]['Female_frequency']
            
            if male_freq > female_freq:
                return 'male'
            elif female_freq > male_freq:
                return 'female'
            else:
                return 'unknown'
        else:
            return 'unknown'