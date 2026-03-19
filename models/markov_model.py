import random
from collections import defaultdict


#Class for the Markov model to generate chord progressions
class MarkovChordModel:
    def __init__(self):
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.transition_probs = {}
        self.data = []

    def load_progressions(self, filepath):
        progressions = []

        with open(filepath, "r") as file:

            for line in file:
                line = line.strip()
                if not line:
                    continue

                chords = line.split()
                progressions.append(chords)

        self.data = progressions

    #Train the model
    def train(self):

        for prog in self.data:
            for i in range(len(prog) - 1):

                current_chord = prog[i]
                next_chord = prog[i + 1]
                self.transition_counts[current_chord][next_chord] += 1

        self._normalize()

    def _normalize(self):
        for chord, next_chords in self.transition_counts.items():

            total = sum(next_chords.values())

            self.transition_probs[chord] = {
                next_chord: count / total
                for next_chord, count in next_chords.items()
            }

    #Generate a chord progression using the learned probabilities.
    def generate(self, start="I", length=8):
        progression = [start]
        current_chord = start

        for _ in range(length - 1):
            if current_chord not in self.transition_probs:
                break

            next_chords = list(self.transition_probs[current_chord].keys())
            probabilities = list(self.transition_probs[current_chord].values())

            next_chord = random.choices(next_chords, probabilities)[0]

            progression.append(next_chord)
            current_chord = next_chord

        return progression



#Main function to run the file/model
def main():
    model = MarkovChordModel()
    model.load_progressions("data/chord_bases_1.txt")
    model.train()

    for _ in range(5):
        progression = model.generate(start="I", length=6)
        print("Generated:", " ".join(progression))


if __name__ == "__main__":
    main()