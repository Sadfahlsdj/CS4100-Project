import random
from collections import defaultdict

#Class for the Markov model to generate chord progressions
class MarkovChordModel:

    #Constructor
    def __init__(self):
        #Count transitions between chords
        self.transition_counts = defaultdict(lambda: defaultdict(int))

        #Store normalized probabilities
        self.transition_probs = {}

    #Train the model
    def train(self, progressions):

        for prog in progressions:
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


def load_progressions(filepath):
    progressions = []

    with open(filepath, "r") as file:

        for line in file:
            line = line.strip()
            if not line:
                continue

            chords = line.split()
            progressions.append(chords)

    return progressions

#Main function to run the file/model
def main():
    #Load dataset
    data = load_progressions("models/data/chord_bases_1.txt")

    #Initialize model
    model = MarkovChordModel()

    #Train model
    model.train(data)

    #Generate some chord progressions
    for _ in range(5):
        progression = model.generate(start="I", length=6)
        print("Generated:", " ".join(progression))


if __name__ == "__main__":
    main()