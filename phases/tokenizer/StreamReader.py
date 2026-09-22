import re
from pathlib import Path

class ChunkedTextReader:
    def __init__(self, file_path: str, word_limit: int = 300):
        self.file_path = Path(file_path)
        self.word_limit = word_limit
        self._file = None
        self._buffer = []
        self._generator = None

    def _tokenize_line(self, line: str):
        return re.findall(r"[A-Za-z]+", line)

    def _chunk_generator(self):
        with self.file_path.open(encoding="utf-8") as f:
            for line in f:
                words = self._tokenize_line(line)
                self._buffer.extend(words)

                while len(self._buffer) >= self.word_limit:
                    chunk_words = self._buffer[:self.word_limit]
                    yield " ".join(chunk_words)
                    self._buffer = self._buffer[self.word_limit:]

            if self._buffer:
                yield " ".join(self._buffer)

    def start(self):
        """Initialize the generator."""
        self._generator = self._chunk_generator()

    def next(self):
        """
        Return (has_more, chunk_string).
        has_more = True if more chunks remain, False when finished.
        """
        if self._generator is None:
            self.start()
        try:
            chunk = next(self._generator)
            return True, chunk
        except StopIteration:
            return False, None


#USage example
#----------------------------------------------------------------------------
# from chunked_reader import ChunkedTextReader  # adjust filename if needed
#----------------------------------------------------------------------------

# reader = ChunkedTextReader("The_secret_of_Father_Brown.txt", word_limit=5)

# while True:
#     has_more, chunk = reader.next()
#     if not has_more:
#         print("Finished reading file.")
#         break
#     print("Got chunk:", chunk)
