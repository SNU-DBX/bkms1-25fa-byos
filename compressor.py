from typing import Dict, List, Tuple

class Compressor:
    def __init__(self):
        # TODO (if any)

        pass

    def compress_index(self, index:Dict) -> Tuple[Dict, bytes]:
        """
        Compresses the index using Gap Encoding and VByte Encoding.
        
        For each term, the compressed format is:
        - Number of documents (VByte encoded)
        - Doc ID gaps (VByte encoded)
        - For each doc ID:
            - Number of positions (VByte encoded)
            - Position gaps (VByte encoded)

        Returns:
            - Term Dictionary: {"term": (offset, size_in_bytes), ...}
            - Postings Data: A single bytes object with all compressed postings.
        """
        # TODO

        pass

    def decompress_postings(self, compressed_postings: bytes) -> Dict[int, List[int]]:
        """
        (YOU DON'T NEED TO MODIFY THIS METHOD)

        Decompresses a compressed postings list.

        Args:
            compressed_postings (bytes): The compressed postings list.

        Returns:
            dict: The decompressed postings list.
        """
        # decode all numbers from the bytestream
        try:
            numbers = self._vbyte_decode(bytearray(compressed_postings))
        except Exception as e:
            print(f"Error decoding bytestream: {e}")
            return {}

        if not numbers:
            return {}

        postings: Dict[int, List[int]] = {}
        
        try:
            num_docs = numbers.pop(0)
            
            if num_docs == 0:
                return {}
            
            doc_id_gaps = numbers[:num_docs]
            numbers = numbers[num_docs:]
            
            doc_ids = []
            last_doc_id_num = 0
            for gap in doc_id_gaps:
                doc_id_num = last_doc_id_num + gap
                doc_ids.append(int(doc_id_num))
                last_doc_id_num = doc_id_num
            
            for doc_id in doc_ids:
                num_positions = numbers.pop(0)
                
                pos_gaps = numbers[:num_positions]
                numbers = numbers[num_positions:] 
                
                positions = []
                last_pos = 0
                for gap in pos_gaps:
                    pos = last_pos + gap
                    positions.append(pos)
                    last_pos = pos
                
                postings[doc_id] = positions
                
        except IndexError:
            print(f"Error: Index data is corrupt or incomplete.")
            return {}
                
        return postings

    def _vbyte_encode(self, numbers: List[int]) -> bytearray:
        """Encodes a list of integers using Variable Byte Encoding (Big-Endian: 0=CONTINUE, 1=STOP)."""

        # TODO
        
        pass

    def _vbyte_decode(self, bytestream: bytearray) -> List[int]:
        """Decodes a Variable Byte encoded bytestream."""
        
        # TODO

        pass

if __name__ == '__main__':
    # this is a simple example to help you test your compressor.
    # it is not part of the actual search engine.
    compressor = Compressor()
    # You can add simple tests here to verify your implementation.
    test_numbers = [10, 11, 13]
    encoded = compressor._vbyte_encode(test_numbers)
    print(f"Encoded: {list(encoded)}")
    decoded = compressor._vbyte_decode(encoded)
    print(f"Decoded: {decoded}")
