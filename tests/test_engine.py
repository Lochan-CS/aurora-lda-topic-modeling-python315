import unittest
from lda_engine import fit_lda, tokenize

class TestLDA(unittest.TestCase):
    def test_tokenization(self):
        self.assertEqual(tokenize('The planets and stars!'), ['planets', 'stars'])

    def test_model(self):
        docs = ['Cats chase mice in gardens', 'Dogs chase balls in parks', 'Birds fly across open skies', 'Planets orbit distant stars', 'Telescopes observe distant galaxies', 'Spacecraft explore distant planets']
        result = fit_lda(docs, n_topics=2, iterations=30)
        self.assertEqual(result['documents'], 6)
        self.assertEqual(len(result['topics']), 2)
        self.assertEqual(len(result['topics'][0]['words']), 5)
        self.assertEqual(len(result['classifications']), 6)
        for row in result['classifications']:
            self.assertAlmostEqual(sum(row['distribution']), 1.0, places=3)

    def test_validation(self):
        with self.assertRaises(ValueError):
            fit_lda(['one document'], 2)

if __name__ == '__main__':
    unittest.main()
