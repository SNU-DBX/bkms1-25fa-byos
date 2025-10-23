# High-Performance Text Search Engine

Welcome! In this assignment, you will build a high-performance text search engine from scratch in Python. You will implement the core components of a search engine, including an inverted index with positional information, efficient index compression, and a searcher that supports various query types.

## Your Task

Your task is to complete the implementation of the four core modules of the search engine. Each file contains `TODO` comments to guide you.

1.  `tokenizer.py`: Implement a text tokenizer that processes raw text into a clean list of tokens. This involves converting text to lowercase, handling punctuation, and removing common "stop words".
2.  `compressor.py`: Implement the Variable Byte (VByte) encoding and decoding algorithms. You will then use these to build a compressor that can significantly reduce the size of the search index.
3.  `indexer.py`: Build a positional inverted index from a collection of documents. This index will map terms to the documents they appear in, along with the positions of each occurrence. You will save this index to a compressed binary file.
4.  `searcher.py`: Implement the search logic to query the compressed index. Your searcher will support single-term, `OR`, `AND`, and exact phrase queries.

## Project Structure

You are provided with the following files and directories:

-   `tokenizer.py`: **(You need to implement this)**
-   `compressor.py`: **(You need to implement this)**
-   `indexer.py`: **(You need to implement this)**
-   `searcher.py`: **(You need to implement this)**
-   `stop_words.txt`: A predefined list of common English words to be ignored by the tokenizer.
-   `test/`: A directory containing a public test suite to help you verify your implementation.
    -   `test.py`: The main test script.
    -   `sample_data.jsonl`: A small sample dataset used by the tests.
    -   `solution_index.json`: The correct uncompressed index for the sample data.
    -   `solution_index.bin`: The correct compressed binary index for the sample data.

## Recommended Workflow

We suggest you implement the components in the following order:

1.  **Tokenizer**: Start with `tokenizer.py`. This is the first step in the indexing pipeline. You can test your implementation by running `python3 tokenizer.py` and modifying the example text.
2.  **Compressor**: Next, implement the VByte encoding/decoding methods in `compressor.py`. The public test suite in `test/test.py` has specific tests for this. Use the `if __name__ == '__main__':` block for your own simple checks.
3.  **Indexer**: With a working tokenizer, you can now build the index in `indexer.py`. Run `python3 indexer.py` to generate your own `index.json` and `index.bin` from the sample data. You can compare your `index.json` with the provided `test/solution_index.json` to see if your logic is correct.
4.  **Searcher**: Finally, implement the search logic in `searcher.py`. Once you have a correctly built index (`index.bin`), you can use `python3 searcher.py` to test your query processing logic.

## How to Test Your Code

There are two primary ways to test your implementation:

### 1. Individual File Testing

Each of the four main `.py` files contains a `if __name__ == '__main__':` block at the end. This allows you to run each file individually to test its functionality in isolation.

```bash
# Test your tokenizer
python3 tokenizer.py

# Test your indexer (this will create index.json and index.bin)
python3 indexer.py

# Test your searcher (requires index.bin to exist)
python3 searcher.py
```

Feel free to modify the code inside these blocks for your own testing purposes. These changes will not affect your grade.

### 2. Public Test Suite

We have provided a public test suite that checks the correctness of all components together. This is a great way to check your progress and catch bugs.

To run the test suite, execute the following command from the `skeleton/` directory:

```bash
python3 test/test.py
```

The test script will run a series of tests and tell you which ones pass or fail. **Passing all public tests is a strong indicator that your implementation is on the right track.** However, your final grade will be determined by a more comprehensive set of private tests on Gradescope.

## Submission

You must submit the following **four files** to Gradescope. Do **not** zip them.

-   `tokenizer.py`
-   `compressor.py`
-   `indexer.py`
-   `searcher.py`

Good luck!