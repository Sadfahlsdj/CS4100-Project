import streamlit as st
import requests
import io

# ─── CONFIG ───────────────────────────────────────────────────────────────────

API_BASE = "http://localhost:8000"

MODELS = {
    'Genetic Algorithm': 'ga',
    'Markov Chain': 'markov',
    'LSTM': 'lstm',
}

INSTRUMENTS = ['piano', 'violin', 'guitar', 'flute', 'trumpet', 'organ']

KEYS = ['C', 'G', 'D', 'A', 'E', 'F', 'Bb', 'Eb', 'C#', 'F#']

DATASET_TYPES = ['no_repeats', 'repeats']

# ─── PAGE SETUP ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Chord Progression Comparison",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Chord Progression Comparison")
st.caption("Comparing Statistical Imitation vs Rule-Based Optimization for Harmonic Progression")

st.divider()

# ─── SINGLE MODEL MODE ────────────────────────────────────────────────────────

st.subheader("Generate & Play")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    model_display = st.selectbox("Model", list(MODELS.keys()))
    model_type = MODELS[model_display]

with col2:
    instrument = st.selectbox("Instrument", INSTRUMENTS)

with col3:
    key = st.selectbox("Key", KEYS)

with col4:
    # LSTM requires multiples of 16
    length = st.selectbox("Length", [16, 32, 48, 64], index=0)

with col5:
    dataset_type = st.selectbox("Dataset", DATASET_TYPES)

if st.button("🎹 Generate", use_container_width=True, type="primary"):
    with st.spinner(f"Generating {model_display} progression..."):
        try:
            response = requests.get(
                f"{API_BASE}/audio",
                params={
                    "model_type": model_type,
                    "key": key,
                    "length": length,
                    "instrument": instrument,
                    "dataset_type": dataset_type,
                },
                timeout=60
            )
            if response.status_code == 200:
                st.success(f"✓ Generated! {model_display} · {key} · {instrument} · {length} chords")
                st.audio(io.BytesIO(response.content), format="audio/wav")
            else:
                st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Make sure the server is running: `python3 -m uvicorn main:app --reload`")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()

# ─── SIDE BY SIDE COMPARISON ──────────────────────────────────────────────────

st.subheader("Side-by-Side Comparison")
st.caption("Generate two models at once to compare them directly")

col_l, col_r = st.columns(2)

with col_l:
    st.markdown("**Model A**")
    model_a_display = st.selectbox("Model A", list(MODELS.keys()), index=0, key="model_a")
    instrument_a = st.selectbox("Instrument A", INSTRUMENTS, key="inst_a")
    key_a = st.selectbox("Key A", KEYS, key="key_a")
    length_a = st.selectbox("Length A", [16, 32, 48, 64], key="len_a")

with col_r:
    st.markdown("**Model B**")
    model_b_display = st.selectbox("Model B", list(MODELS.keys()), index=1, key="model_b")
    instrument_b = st.selectbox("Instrument B", INSTRUMENTS, key="inst_b")
    key_b = st.selectbox("Key B", KEYS, key="key_b")
    length_b = st.selectbox("Length B", [16, 32, 48, 64], key="len_b")

if st.button("🎼 Compare Both", use_container_width=True, type="primary"):
    col_l2, col_r2 = st.columns(2)

    def fetch_audio(model_type, instrument, key, length, dataset_type='no_repeats'):
        response = requests.get(
            f"{API_BASE}/audio",
            params={
                "model_type": model_type,
                "key": key,
                "length": length,
                "instrument": instrument,
                "dataset_type": dataset_type,
            },
            timeout=60
        )
        return response

    with col_l2:
        with st.spinner(f"Generating {model_a_display}..."):
            try:
                resp_a = fetch_audio(MODELS[model_a_display], instrument_a, key_a, length_a)
                if resp_a.status_code == 200:
                    st.success(f"✓ {model_a_display}")
                    st.audio(io.BytesIO(resp_a.content), format="audio/wav")
                else:
                    st.error(f"Error: {resp_a.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed: {e}")

    with col_r2:
        with st.spinner(f"Generating {model_b_display}..."):
            try:
                resp_b = fetch_audio(MODELS[model_b_display], instrument_b, key_b, length_b)
                if resp_b.status_code == 200:
                    st.success(f"✓ {model_b_display}")
                    st.audio(io.BytesIO(resp_b.content), format="audio/wav")
                else:
                    st.error(f"Error: {resp_b.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed: {e}")