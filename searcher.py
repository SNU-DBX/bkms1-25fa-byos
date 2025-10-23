import json
from typing import Dict, List, Set
from compressor import Compressor

class Searcher:
    def __init__(self, index_filepath: str, stop_words_path: str='stop_words.txt'):
        self.index_filepath = index_filepath
        self.term_dict = self._load_term_dict()
        self.file = open(index_filepath, 'rb')
        self.term_dict_json_len = len(json.dumps(self.term_dict).encode('utf-8'))
        self.compressor = Compressor()
        self.stop_words = self._load_stop_words(stop_words_path)

    def _load_term_dict(self) -> Dict:
        """Loads the term dictionary from the index file."""
        with open(self.index_filepath, 'rb') as f:
            header = f.read(4)
            term_dict_len = int.from_bytes(header, byteorder='big')
            term_dict_json = f.read(term_dict_len).decode('utf-8')
            return json.loads(term_dict_json)

    def _load_stop_words(self, filepath: str) -> Set[str]:
        """Loads stop words from a file into a set."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)

    def _get_postings(self, term: str) -> Dict[int, List[int]]:
        """
        Retrieves, decodes, and returns the postings list for a term.
        """
        if term not in self.term_dict:
            return {}
        
        offset, size = self.term_dict[term]
        
        self.file.seek(4 + self.term_dict_json_len + offset)
        compressed_postings = self.file.read(size)

        # TODO
        # We have done almost everything here - what else is needed?
        pass
        

    def search(self, query: str) -> List[str]:
        """
        Performs a search based on the query type.
        """
        if query.startswith('"') and query.endswith('"'):
            return self._phrase_search(query.strip('"'))
        elif ' OR ' in query:
            terms = query.split(' OR ')
            return self._or_search(terms)
        elif ' AND ' in query:
            terms = query.split(' AND ')
            return self._and_search(terms)
        else:
            return self._single_term_search(query)

    def _single_term_search(self, term: str) -> List[int]:
        """Finds documents containing the term and returns their Doc IDs, sorted in ascending order."""
        # TODO
        pass

    def _or_search(self, terms: List[str]) -> List[int]:
        """Finds documents containing at least one of the terms and returns their Doc IDs, sorted in ascending order."""
        # TODO
        pass

    def _and_search(self, terms: List[str]) -> List[int]:
        """Finds documents containing all terms using merge algorithm anmd returns their Doc IDs, sorted in ascending order."""
        # TODO
        pass

    def _intersect(self, p1: List[int], p2: List[int]) -> List[int]:
        """Computes the intersection of two sorted posting lists.
            Used by AND search."""
        # TODO
        pass

    def _phrase_search(self, phrase: str) -> List[int]:
        """
        (YOU DO NOT NEED TO MODIFY THIS)
        Finds documents containing the exact phrase."""
        terms = phrase.split()

        # exclude stop words
        terms = [term for term in terms if term not in self.stop_words]

        if not terms:
            return []

        # Fetch postings only once for each term.
        all_postings = {term: self._get_postings(term) for term in terms}

        # Get doc IDs that contain all terms.
        # This can be further optimized by passing all_postings to _and_search,
        # but the main bottleneck is what follows.
        common_docs = self._and_search(terms)
        
        results = []
        for doc_id in common_docs:
            # Get this doc's positions for each term from the cached postings
            pos_lists = [all_postings[term][doc_id] for term in terms]
            
            # Convert subsequent position lists to sets for fast O(1) lookups
            pos_sets = [set(p) for p in pos_lists[1:]]

            # Check for the phrase sequence
            for pos1 in pos_lists[0]:
                match_found = True
                # Check if pos1+1, pos1+2, etc. exist in the other sets
                for i, pos_set in enumerate(pos_sets):
                    if (pos1 + i + 1) not in pos_set:
                        match_found = False
                        break
                
                if match_found:
                    results.append(doc_id)
                    # Found a match in this doc, no need to check other positions
                    break 
        
        return sorted(results)

    def __del__(self):
        """Closes the file handle when the object is destroyed."""
        if hasattr(self, 'file') and self.file:
            self.file.close()

if __name__ == '__main__':
    # this is a simple example to help you test your searcher.
    # it is not part of the actual search engine.
    # You will need to build the index first using indexer.py.
    searcher = Searcher('index.bin', 'stop_words.txt')
    
    print("--- Single Term Search ---")
    print("Query: 'database'")
    print(f"Result: {searcher.search('database')}")

    print("\n--- OR Search ---")
    print("Query: 'database OR information'")
    print(f"Result: {searcher.search('database OR information')}")

    print("\n--- AND Search ---")
    print("Query: 'database AND system'")
    print(f"Result: {searcher.search('database AND system')}")
    
    print("\n--- Phrase Search ---")
    print("Query: '\"database management\"'")
    phrase_query = '"database management"'
    print(f"Result: {searcher.search(phrase_query)}")
    print("Query: '\"storing data\"'")
    phrase_query_2 = '"storing data"'
    print(f"Result: {searcher.search(phrase_query_2)}")

    del searcher
