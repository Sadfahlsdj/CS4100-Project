# Music Sheet Generator
### CS 4100 - Artificial Intelligence | Northeastern University

**Instructor:** Rajagopal Venkatesaramani

**Team:** Mehr Singh Anand (Project Manager), Mihalis Koutouvos, William Sartorio, Nalini Singh

---

## Project Statement

Traditional chord progression follows patterns that simultaneously satisfy statistical regularities (e.g., transition probabilities between chords) and theoretical constraints (e.g., voice leading, resolution, tension). Existing work tends to optimize a single technique in isolation. This project directly compares two fundamentally different AI approaches applied to the same task, offering insight into the tradeoffs between learned pattern recognition and rule-guided optimization.



---

## Approach

### Markov Chain Model
Models chord transitions as conditional probabilities derived from observed sequences. Captures what composers statistically *do* based on training data.

### Genetic Algorithm Model
Encodes chord progressions as candidate solutions and evolves them over generations using a fitness function grounded in music theory rules. Captures what composers *should* do according to theoretical constraints.

### Evaluation
Both models are evaluated on the same dataset of chord progressions. Metrics include harmonic coherence, adherence to voice leading rules, and subjective musical quality. A rule-based system supplements both models for error correction and constraint enforcement.


## Repository Structure

```
.
├── data/                  # Chord progression datasets
├── markov/                # Markov Chain model implementation
├── genetic/               # Genetic Algorithm model implementation
├── evaluation/            # Evaluation scripts and metrics
├── utils/                 # Shared utilities (parsing, music theory rules)
├── results/               # Output progressions and comparison results
└── README.md
```

---

## Getting Started

### Prerequisites

```bash
Python 3.10+
pip install -r requirements.txt
```

### Running the Models

```bash
# Markov Chain
python markov/train.py --data data/progressions.csv
python markov/generate.py --length 8

# Genetic Algorithm
python genetic/evolve.py --generations 500 --population 100
```

---

## Timeline

| Milestone | Target Date |
|---|---|
| Project Proposal | January 25, 2025 |
| First Check-In | Last week of February |
| Second Check-In | Last week of March |
| Presentation Slides | April 8, 2025 |
| Presentations | April 10, 2025 |
| Final Deliverables | April 17, 2025 |


## Acknowledgments

We thank the CS 4100 teaching staff - in particular the TAs specializing in genetic algorithms and machine learning - for their guidance throughout this project.

---

*CS 4100 - Artificial Intelligence, Northeastern University*
