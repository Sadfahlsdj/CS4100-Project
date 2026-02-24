

#This is our state space. Each of our algorithms and the fitness function for GA will use this
ROMAN_NUMERALS = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]

#For GA guidance:
CHORD_IDENTITIES = {
    "I": "Tonic",
    "ii": "Supertonic",
    "iii": "Mediant",
    "IV": "Subdominant",
    "V": "Dominant",
    "vi": "Submediant",
    "vii°": "Leading Tone"
}