import sys
import os
import json
import unittest
try:
    from termcolor import colored
except ImportError:
    print("Warning: 'termcolor' package not found. Installing it is recommended for colored output.")
    print("You can install it using: pip install termcolor")
    # Define a fallback function if termcolor is not available
    def colored(text, color):
        return text

# Add the parent directory to the Python path to import student modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from tokenizer import Tokenizer
    from compressor import Compressor
    from indexer import Indexer
    from searcher import Searcher
except ImportError as e:
    print(colored(f"CRITICAL ERROR: Could not import necessary modules.", 'red'))
    print(colored(f"Please ensure tokenizer.py, compressor.py, indexer.py, and searcher.py exist in the parent directory.", 'red'))
    print(colored(f"Details: {e}", 'red'))
    sys.exit(1)

# --- Hard-coded Solutions ---

TOKENIZER_TEXT = "The quick brown fox ran 1.5 miles to his \"ultra-secret\" den, but couldn't get in!"
TOKENIZER_SOLUTION = ['quick', 'brown', 'fox', 'ran', '1', '5', 'miles', 'ultra-secret', 'den', 'couldnt', 'get']

VBYTE_ENCODE_TEST_CASES = {
    'case_0': {'input': [1, 2, 3, 4, 5], 'output': b'\x81\x82\x83\x84\x85'},
    'case_1': {'input': [127, 128, 255, 256], 'output': b'\xff\x01\x80\x01\xff\x02\x80'},
    'case_2': {'input': [10, 100, 1000, 10000, 100000], 'output': b'\x8a\xe4\x07\xe8N\x90\x06\r\xa0'},
    'case_3': {'input': [0], 'output': b'\x80'},
    'case_4': {'input': [], 'output': b''},
}

SEARCHER_TEST_CASES = {
    'search': [3, 4, 5],
    'quick OR dog': [0, 1],
    'search AND engine': [3, 5],
    '"information retrieval"': [4, 5],
}

class ColoredTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(colored(f"  PASSED", 'green'))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln(colored(f"  FAILED", 'red'))

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.writeln(colored(f"  ERROR", 'red'))

class ColoredTestRunner(unittest.TextTestRunner):
    resultclass = ColoredTestResult

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

class PublicTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up paths and ensure test files are present before running tests."""
        cls.base_dir = os.path.dirname(os.path.abspath(__file__))
        cls.parent_dir = os.path.dirname(cls.base_dir)
        
        cls.sample_data_path = os.path.join(cls.base_dir, 'sample_data.jsonl')
        cls.solution_json_path = os.path.join(cls.base_dir, 'solution_index.json')
        cls.solution_bin_path = os.path.join(cls.base_dir, 'solution_index.bin')
        cls.stop_words_path = os.path.join(cls.parent_dir, 'stop_words.txt')

        required_files = [cls.sample_data_path, cls.solution_json_path, cls.solution_bin_path, cls.stop_words_path]
        if not all(os.path.exists(p) for p in required_files):
            missing = [os.path.basename(p) for p in required_files if not os.path.exists(p)]
            raise FileNotFoundError(f"Error: Missing necessary test file(s): {', '.join(missing)}")

    def test_01_tokenizer(self):
        """Tests the Tokenizer implementation."""
        tokenizer = Tokenizer(stop_words_path=self.stop_words_path)
        student_tokens = tokenizer.tokenize(TOKENIZER_TEXT)
        self.assertEqual(student_tokens, TOKENIZER_SOLUTION, "Tokenizer output does not match the expected solution.")

    def test_02_compressor_vbyte_encode(self):
        """Tests the Compressor's VByte encoding for various cases."""
        compressor = Compressor()
        for name, case in VBYTE_ENCODE_TEST_CASES.items():
            with self.subTest(case=name, input=case['input']):
                student_encoded = compressor._vbyte_encode(case['input'])
                self.assertEqual(student_encoded, case['output'], f"VByte encoding failed for input: {case['input']}")

    def test_03_compressor_roundtrip(self):
        """Tests if VByte encoding and decoding a list returns the original list."""
        compressor = Compressor()
        test_list = [10, 200, 3000, 40000, 500000]
        encoded = compressor._vbyte_encode(test_list)
        self.assertIsNotNone(encoded, "The _vbyte_encode method should not return None.")
        decoded = compressor._vbyte_decode(encoded)
        self.assertEqual(test_list, decoded, "VByte encode/decode roundtrip failed. The decoded list does not match the original.")

    def test_04_indexer(self):
        """Tests index generation by comparing student-generated files with solution files."""
        student_json_path = os.path.join(self.base_dir, 'student_index.json')
        student_bin_path = os.path.join(self.base_dir, 'student_index.bin')
        
        try:
            indexer = Indexer(
                self.sample_data_path,
                json_index_path=student_json_path,
                bin_index_path=student_bin_path,
                stop_words_path=self.stop_words_path
            )
            indexer.build_index()
            indexer.save_index_json()
            indexer.compress_and_save_index_bin()

            with open(self.solution_json_path, 'r') as f_sol, open(student_json_path, 'r') as f_stu:
                solution_json = json.load(f_sol)
                student_json = json.load(f_stu)
                self.assertEqual(solution_json, student_json, "Generated JSON index content does not match solution.")
            
            with open(self.solution_bin_path, 'rb') as f_sol, open(student_bin_path, 'rb') as f_stu:
                solution_bin = f_sol.read()
                student_bin = f_stu.read()
                self.assertEqual(solution_bin, student_bin, "Generated binary index content does not match solution.")
        finally:
            if os.path.exists(student_json_path):
                os.remove(student_json_path)
            if os.path.exists(student_bin_path):
                os.remove(student_bin_path)

    def test_05_searcher(self):
        """Tests the Searcher with various query types against the solution index."""
        searcher = Searcher(self.solution_bin_path, self.stop_words_path)
        for query, solution in SEARCHER_TEST_CASES.items():
            with self.subTest(query=query):
                student_results = searcher.search(query)
                self.assertIsNotNone(student_results, f"Search method returned None for query: '{query}'. It should return a list.")
                self.assertListEqual(sorted(student_results), sorted(solution), f"Search results for query '{query}' are incorrect.")
        del searcher

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PublicTestSuite)
    runner = ColoredTestRunner(verbosity=2)
    print("======================================================")
    print("           Running Public Test Suite")
    print("======================================================")
    runner.run(suite)