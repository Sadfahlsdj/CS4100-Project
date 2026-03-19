import streamlit as st
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Music Sheet Generator", page_icon="🎵", layout="wide")

# ── Chord pools per mode ──────────────────────────────────────────────────────
CHORD_POOLS = {
    "major":  ["I","ii","iii","IV","V","vi","vii°","V/V","I⁷","IV⁷","V⁷","ii⁷","vi⁷"],
    "minor":  ["i","ii°","♭III","iv","v","V","♭VI","♭VII","i⁷","iv⁷","V⁷","♭VII⁷"],
    "jazz":   ["Imaj7","ii⁷","V⁷","iii⁷","vi⁷","ii⁷♭5","♭IImaj7","IV⁷","♭VII⁷","V⁷♯11"],
    "dorian": ["i","II","♭III","IV","v","vi°","♭VII","i⁷","IV⁷","v⁷"],
}

# ── Markov transition table ───────────────────────────────────────────────────
MARKOV_RULES = {
    "I":     ["IV","V","vi","ii","I⁷","V⁷"],
    "IV":    ["V","I","ii","IV⁷"],
    "V":     ["I","vi","V⁷"],
    "vi":    ["IV","ii","V","I"],
    "ii":    ["V","IV","vi"],
    "vii°":  ["I","V"],
    "iii":   ["vi","IV","I"],
    "I⁷":   ["IV","IV⁷"],
    "V⁷":   ["I","vi"],
    "IV⁷":  ["V⁷","I"],
    "ii⁷":  ["V⁷","ii"],
    "vi⁷":  ["ii⁷","V⁷"],
    "i":     ["iv","V","♭VII","♭VI"],
    "iv":    ["V","i","♭VII"],
    "♭VII":  ["♭VI","i","iv"],
    "♭VI":   ["♭VII","V","iv"],
    "ii°":   ["V","i"],
    "♭III":  ["♭VII","iv","i"],
    "Imaj7": ["ii⁷","V⁷","vi⁷","IV⁷"],
    "iii⁷":  ["vi⁷","ii⁷"],
    "♭IImaj7": ["Imaj7"],
    "♭VII⁷": ["Imaj7","IV⁷"],
    "V⁷♯11": ["Imaj7"],
    "ii⁷♭5": ["V⁷","♭IImaj7"],
    "i⁷":    ["IV⁷","v⁷"],
    "v⁷":    ["i⁷","♭VII⁷"],
    "II":    ["v⁷","IV⁷"],
    "vi°":   ["i","v⁷"],
}

# ── Harmonic function map ─────────────────────────────────────────────────────
FUNC_MAP = {
    "I":"T","IV":"PD","V":"D","vi":"T","ii":"PD","vii°":"D","iii":"T",
    "I⁷":"T","IV⁷":"PD","V⁷":"D","ii⁷":"PD","vi⁷":"T",
    "i":"T","iv":"PD","♭VII":"D","♭VI":"PD","ii°":"PD","♭III":"T",
    "Imaj7":"T","iii⁷":"T","♭IImaj7":"D","♭VII⁷":"D","V⁷♯11":"D","ii⁷♭5":"PD",
    "i⁷":"T","v⁷":"D","II":"PD","vi°":"D","V":"D",
}

FUNC_LABELS = {"T": "Tonic", "PD": "Predominant", "D": "Dominant"}
FUNC_COLORS = {"T": "🟢", "PD": "🟡", "D": "🔴"}

KEYS = ["C","G","D","A","E","B","F#","F","B♭","E♭","A♭","D♭"]

# ── Markov generation (mode static, no tempo control) ───────────────────────────
DEFAULT_MODE = "major"

def markov_generate(length: int) -> list[str]:
    pool = CHORD_POOLS[DEFAULT_MODE]
    progression = [random.choice(pool)]
    for _ in range(length - 1):
        cur = progression[-1]
        candidates = [c for c in MARKOV_RULES.get(cur, []) if c in pool]
        progression.append(random.choice(candidates) if candidates else random.choice(pool))
    return progression

# ── Theory score ──────────────────────────────────────────────────────────────
def score_progression(prog: list[str]) -> int:
    score = 50
    funcs = [FUNC_MAP.get(c, "?") for c in prog]
    for i in range(1, len(funcs)):
        transition = f"{funcs[i-1]}->{funcs[i]}"
        if transition in ["T->PD", "PD->D", "D->T", "T->D"]:
            score += 5
        if transition in ["D->PD", "PD->T"]:
            score -= 3
        if funcs[i] == funcs[i - 1]:
            score -= 2
    if funcs[-1] == "T":
        score += 10
    if funcs[-1] == "D":
        score -= 5
    if len(funcs) >= 2 and f"{funcs[-2]}->{funcs[-1]}" == "D->T":
        score += 8
    return max(0, min(100, score))

# ── Genetic algorithm ─────────────────────────────────────────────────────────
def genetic_generate(length: int, generations: int, pop_size: int) -> list[str]:
    pool = CHORD_POOLS[DEFAULT_MODE]
    population = [
        [random.choice(pool) for _ in range(length)]
        for _ in range(pop_size)
    ]
    fitness_history = []
    for _ in range(generations):
        population.sort(key=score_progression, reverse=True)
        fitness_history.append(score_progression(population[0]))
        survivors = population[:max(2, int(pop_size * 0.4))]
        offspring = []
        while len(offspring) < pop_size - len(survivors):
            p1, p2 = random.sample(survivors, 2)
            cut = random.randint(1, length - 1)
            child = p1[:cut] + p2[cut:]
            if random.random() < 0.15:
                child[random.randint(0, length - 1)] = random.choice(pool)
            offspring.append(child)
        population = survivors + offspring
    population.sort(key=score_progression, reverse=True)
    return population[0], fitness_history

# ── LSTM placeholder generation (frontend-only stub) ───────────────────────────
def lstm_generate(length: int) -> list[str]:
    # Replace this with real LSTM inference feeding a trained model in backend
    pool = CHORD_POOLS[DEFAULT_MODE]
    progression = []
    for i in range(length):
        if i == 0:
            progression.append(random.choice(pool))
        else:
            progression.append(random.choice(MARKOV_RULES.get(progression[-1], pool)))
    return progression

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🎵 Music Sheet Generator")
st.caption("CS 4100 · Markov Chain vs Genetic Algorithm · Northeastern University")

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar controls
with st.sidebar:
    st.header("Configuration")

    model = st.radio("Model", ["Markov Chain", "Genetic Algorithm", "LSTM"],
                     help="Markov = statistical patterns. GA = theory-guided evolution. LSTM = learned sequence generation.")

    st.divider()
    key    = st.selectbox("Key", KEYS)
    length = st.select_slider("Chord length", options=[4, 6, 8, 12, 16], value=8)

    if model == "Markov Chain":
        st.divider()
        st.subheader("Markov parameters")
        markov_size = st.number_input("Progression size", min_value=4, max_value=32, value=8, step=1)
    else:
        markov_size = length

    if model == "Genetic Algorithm":
        st.divider()
        st.subheader("GA parameters")
        generations = st.slider("Generations", 10, 300, 50, step=10)
        pop_size    = st.slider("Population size", 10, 100, 20, step=5)
    else:
        generations, pop_size = 50, 20

    if model == "LSTM":
        st.divider()
        st.subheader("LSTM parameters (frontend placeholder)")
        lstm_temperature = st.slider("Temperature", 0.5, 2.0, 1.0, step=0.1)
    else:
        lstm_temperature = 1.0

    generate = st.button("Generate progression", type="primary", use_container_width=True)

# Tabs
tab_gen, tab_history = st.tabs(["Generate", "History"])

# ── Generate tab ──────────────────────────────────────────────────────────────
with tab_gen:
    if generate:
        with st.spinner("Evolving population..." if model == "Genetic Algorithm" else "Generating..."):
            if model == "Markov Chain":
                prog = markov_generate(markov_size)
                fitness_history = None
            elif model == "Genetic Algorithm":
                prog, fitness_history = genetic_generate(length, generations, pop_size)
            else:
                prog = lstm_generate(length)
                fitness_history = None

            score = score_progression(prog)
            funcs = [FUNC_MAP.get(c, "?") for c in prog]
            has_cadence = len(funcs) >= 2 and f"{funcs[-2]}->{funcs[-1]}" == "D->T"

            result = dict(prog=prog, score=score, funcs=funcs, has_cadence=has_cadence,
                          model=model, key=key,
                          generations=generations, pop_size=pop_size,
                          fitness_history=fitness_history)
            st.session_state.result = result
            st.session_state.history.insert(0, result)
            if len(st.session_state.history) > 10:
                st.session_state.history = st.session_state.history[:10]

    if "result" in st.session_state:
        r = st.session_state.result
        st.subheader(f"Result — {r['key']} ({r['model']})")

        col_score, col_cadence, col_info = st.columns(3)
        col_score.metric("Theory score", f"{r['score']}/100")
        col_cadence.metric("Cadence", "D→T ✓" if r["has_cadence"] else "None")
        col_info.metric("Length", f"{len(r['prog'])} chords")

        st.divider()

        # Chord display
        cols = st.columns(len(r["prog"]))
        for i, (chord, func) in enumerate(zip(r["prog"], r["funcs"])):
            with cols[i]:
                st.markdown(f"<div style='text-align:center; font-size:22px; font-weight:600'>{chord}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center; font-size:12px; color:gray'>{FUNC_COLORS.get(func,'')} {func}</div>", unsafe_allow_html=True)

        st.divider()
        legend_cols = st.columns(3)
        for i, (k, v) in enumerate(FUNC_LABELS.items()):
            legend_cols[i].caption(f"{FUNC_COLORS[k]} {k} = {v}")

        st.divider()
        st.subheader("Playback / Export")
        txt = " ".join(r["prog"])
        if st.button("Generate TXT from progression"):
            st.success("Chord sequence converted to text. Use the download button below to save and play with an external library.")
        st.download_button("Download progression as .txt", data=txt, file_name="progression.txt", mime="text/plain")

        st.info(
            "Basic play idea: send `progression.txt` to a sound engine. "
            "A Python playback library (e.g., music21, fluidsynth, or pygame.midi) can read chords, map to pitches, and play."
        )
    else:
        st.info("Configure your parameters in the sidebar and hit **Generate progression**.")

# ── History tab ───────────────────────────────────────────────────────────────
with tab_history:
    if not st.session_state.history:
        st.info("No progressions generated yet.")
    else:
        for i, h in enumerate(st.session_state.history):
            with st.expander(f"{h['key']} · {h['model']} · Score: {h['score']}/100"):
                chord_str = "  →  ".join(h["prog"])
                st.markdown(f"**Progression:** {chord_str}")
                st.caption(f"Cadence: {'Yes' if h['has_cadence'] else 'No'}")