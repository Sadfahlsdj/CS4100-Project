import torch
import numpy as np
from models.lstm import ChordLSTM


def load_model_and_generate(model_path, data_path, seed_chords, length=20, temperature=0.8, dataset_type='no_repeats'):
    # load the already processed data
    data_meta = torch.load(data_path)
    vocab = data_meta['vocab']
    c2i = data_meta['c2i']
    i2c = data_meta['i2c']

    # re-initializing using same parameters as the model was initialized with
    if dataset_type == 'no_repeats':
        model = ChordLSTM(vocab_size=len(vocab), embed_dim=64, hidden_dim=128)
    else:
        model = ChordLSTM(vocab_size=len(vocab), embed_dim=64, hidden_dim=256)

    # load weights
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    # seed sequence
    try:
        current_seq = [c2i[c] for c in seed_chords]
    except KeyError as e:
        print(f"Error: Chord {e} in seed was not in the training vocabulary.")
        return []

    generated = []

    # actual generation
    with torch.no_grad():
        for _ in range(length):
            x = torch.LongTensor([current_seq])
            logits = model(x)

            # temperature
            probs = torch.softmax(logits / temperature, dim=1).numpy().squeeze()
            next_chord_idx = np.random.choice(len(probs), p=probs)
            generated.append(i2c[next_chord_idx])
            current_seq = current_seq[1:] + [next_chord_idx]

    return generated


if __name__ == "__main__":
    MODEL_PATH = "model_states/chord_model_epoch_10.pth"
    DATA_PATH = "data/chord_bases_processed.pt"

    # starting sequence of same seq_length that model initially used (8 here)
    my_seed = ["I", "V", "vi", "IV", "I", "V", "I", "I"]

    new_progression = load_model_and_generate(MODEL_PATH, DATA_PATH, my_seed)

    print("seed:", " ".join(my_seed))
    print("generated progression:", " ".join(new_progression))
