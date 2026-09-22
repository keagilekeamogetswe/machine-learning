class NgramExtractor:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def _getGroups(self, word: str, group_size: int) -> list[str]:
        """
        Internal helper: extracts all adjacent sliding window combinations
        of a given size.
        """
        if len(word) < group_size or group_size <= 0:
            return []

        total_number_of_outputs = len(word) - group_size + 1
        return [word[i : i + group_size] for i in range(total_number_of_outputs)]

    def getNgramStats(self) -> dict[str, dict[str, int]]:
        """
        Returns a dictionary where each n-gram is a key,
        and the value is an object with {size, frequency}.
        """
        words = self.prompt.split()
        stats: dict[str, dict[str, int]] = {}

        for word in words:
            for current_size in range(2, len(word) + 1):
                for combo in self._getGroups(word, current_size):
                    if combo not in stats:
                        stats[combo] = {"size": current_size, "frequency": 0}
                    stats[combo]["frequency"] += 1

        return stats
