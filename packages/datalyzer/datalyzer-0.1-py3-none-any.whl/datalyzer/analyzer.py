import pandas as pd

class DataAnalyzer:
    def __init__(self, data):
        self.data = data  # Przechowuje przekazane dane

    def summary(self):
        # Zwraca podstawowe statystyki danych
        return self.data.describe()

    def missing_values(self):
        # Zwraca liczbę brakujących wartości w każdej kolumnie
        return self.data.isnull().sum()
