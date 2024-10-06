import unittest
import pandas as pd
from datalyzer.analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        # Przygotowanie danych do testów
        self.data = pd.DataFrame({'A': [1, 2, 3, None], 'B': [4, None, 6, 7]})
        self.analyzer = DataAnalyzer(self.data)

    def test_summary(self):
        summary = self.analyzer.summary()
        self.assertIn('A', summary.columns)
        self.assertIn('B', summary.columns)

    def test_missing_values(self):
        missing = self.analyzer.missing_values()
        self.assertEqual(missing['A'], 1)
        self.assertEqual(missing['B'], 1)

if __name__ == '__main__':
    unittest.main()
