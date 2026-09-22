from NGramExtractor import NgramExtractor
from StreamReader import StreamReader
from repository.CombinationRepository import CombinationRepository
from essay.EssayAutoloader import autoLoadPaths

def process_essays(word_limit: int = 1000):
    essay_paths = autoLoadPaths()

    repo = CombinationRepository()
    try:
        for path in essay_paths:
            reader = StreamReader(path, word_limit)

            while True:
                has_more, chunk = reader.next()
                if not has_more:
                    print(f"Finished reading {path}")
                    break

                stats = NgramExtractor(chunk).getNgramStats()
                repo.add(stats)

                print(f"Got chunk from {path}: {chunk[:80]}...")  # preview
    finally:
        repo.close()
