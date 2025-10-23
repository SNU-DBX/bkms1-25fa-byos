
import os
import json
from tokenizer import Tokenizer
from compressor import Compressor

class Indexer:
    def __init__(self, data_filepath: str, json_index_path='index.json', bin_index_path: str='index.bin', stop_words_path='stop_words.txt'):
        """
        Initializes the Indexer.

        Args:
            data_filepath (str): Path to the file containing the data.
            index_path (str): Path to save the compressed binary index.
            json_index_path (str): Path to save the uncompressed JSON index.
        """
        self.data_filepath = data_filepath
        self.bin_index_path = bin_index_path
        self.json_index_path = json_index_path
        self.tokenizer = Tokenizer(stop_words_path=stop_words_path)
        self.compressor = Compressor()
        self.index = {}

    def build_index(self):
        """
        Builds the inverted index from the documents in the data directory.
        Stores the index in memory in the `self.index` attribute.
        """
        # Remove this 'pass' statement and implement the method.
        pass

    def save_index_json(self):
        """
        Saves only the uncompressed JSON index to a file.
        """    
        # Remove this 'pass' statement and implement the method.
        pass

    def compress_and_save_index_bin(self):
        """
        (YOU DON'T NEED TO MODIFY THIS METHOD)
        Saves only the compressed binary index to a file.

        File Format:
        - Header (4 bytes): Length of the term dictionary JSON.
        - Term Dictionary: JSON string of the term dictionary.
        - Postings Data: Raw bytes of the compressed postings.
        """
        term_dict, postings_data = self.compressor.compress_index(self.index)

        term_dict_json = json.dumps(term_dict).encode('utf-8')
        header = len(term_dict_json).to_bytes(4, byteorder='big')

        with open(self.bin_index_path, 'wb') as f:
            f.write(header)
            f.write(term_dict_json)
            f.write(postings_data)

if __name__ == '__main__':
    # This is a simple example to help you test your indexer.
    # It is not part of the actual search engine.
    indexer = Indexer('./test/sample_data.jsonl', json_index_path='index.json', bin_index_path='index.bin')
    print("Building index...")
    indexer.build_index()
    print("Saving index...(JSON)")
    indexer.save_index_json()
    print("Saving index...(Binary)")
    indexer.compress_and_save_index_bin()
    print("Indexing Complete.")
