import json
from dataclasses import dataclass
import tensorflow as tf
import selfies as sf
import kdens
import numpy as np
import sys
import os

folder_path = '../dziner/surrogates/solubility/' 
sys.path.append(folder_path)

if folder_path not in sys.path:
    sys.path.append(folder_path)

with open(os.path.join(folder_path,"sol_model/voc.json"), 'r') as f:
  voc = json.load(f)


@dataclass
class Config:
    vocab_size: int = len(voc)
    batch_size: int = 16
    buffer_size: int = 10000
    rnn_units: int = 64
    hidden_dim: int = 32
    embedding_dim: int = 64
    reg_strength: float = 0.01
    lr: float = 1e-4
    drop_rate: float = 0.35
    nmodels: int = 10
    adv_epsilon: float = 1e-3
    epochs: int = 150

config = Config()

def build_inf_model():
    inputs = tf.keras.Input(shape=(None,))

    # make embedding and indicate that 0 should be treated as padding mask
    e = tf.keras.layers.Embedding(input_dim=config.vocab_size,
                                        output_dim=config.embedding_dim,
                                        mask_zero=True)(inputs)

    # RNN layer
    x = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(config.rnn_units, return_sequences=True))(e)
    x = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(config.rnn_units))(x)
    x = tf.keras.layers.LayerNormalization()(x)
    # a dense hidden layer
    x = tf.keras.layers.Dense(config.hidden_dim, activation="swish")(x)
    x = tf.keras.layers.Dense(config.hidden_dim // 2, activation="swish")(x)
    # predicting prob, so no activation
    muhat = tf.keras.layers.Dense(1)(x)
    stdhat = tf.keras.layers.Dense(1, activation='softplus')(x)
    out = tf.squeeze(tf.stack([muhat, stdhat], axis=-1))
    model = tf.keras.Model(inputs=inputs, outputs=out, name='sol-rnn-infer')
    # model = tf.keras.Model(inputs=inputs, outputs=(muhat, stdhat), name='sol-rnn-infer')
    return model

def enc(smiles):
  try:
    return sf.encoder(smiles)
  except:
    # print(smiles)
    return None
  
# models = []
# for i in range(config.nmodels):
#   with open(f"sol_model/m{i}.json", "r") as json_file:
#     json_model = json_file.read()
#     m = tf.keras.models.model_from_json(json_model)
#     m.load_weights(f"sol_model/m{i}.h5")

#     models.append(m)
#     # models[i].load_weights(f"{model_path}/m{i}.h5")

# m = kdens.DeepEnsemble(build_inf_model, config.nmodels, config.adv_epsilon)
# m.models = models

# m.compile(
#     tf.optimizers.Adam(),
#     loss=kdens.neg_ll,
#     metrics=[tf.keras.metrics.MeanSquaredError(), tf.keras.metrics.MeanAbsoluteError()])


vocab = voc.keys()
vocab_stoi = {o:i for o,i in zip(vocab, range(len(vocab)))}

def selfies2ints(s):
    result = []
    for token in sf.split_selfies(s):
        if token in vocab_stoi:
          result.append(vocab_stoi[token])
        else:
          # print(token)
          result.append(0) #[nop]  #np.nan)
          #print('Warning')
    return result

smiles = 'CN1CCN(C2=C(NC(C3=CC=C(Cl)C4=CC=CC=C43)=O)C=C(C(=O)NCO)C=C2)C(C)C1'


def predict_solubility(smiles, model_path):

    models = []
    for i in range(config.nmodels):
        with open(f"{model_path}/m{i}.json", "r") as json_file:
            json_model = json_file.read()
            m = tf.keras.models.model_from_json(json_model)
            m.load_weights(f"{model_path}/m{i}.h5")
            models.append(m)
    m = kdens.DeepEnsemble(build_inf_model, config.nmodels, config.adv_epsilon)
    m.models = models

    m.compile(
        tf.optimizers.Adam(),
        loss=kdens.neg_ll,
        metrics=[tf.keras.metrics.MeanSquaredError(), tf.keras.metrics.MeanAbsoluteError()])
    selfies_list = [sf.encoder(smiles)]
    encoded = [selfies2ints(s) for s in selfies_list if s is not None]
    padded_seqs = tf.keras.preprocessing.sequence.pad_sequences(encoded, padding="post")
    predicitions = []
    for m in models:
        predicitions.append(m.predict(padded_seqs))
    predicitions = np.array(predicitions)

    sol = np.mean(predicitions[:,0])
    error = np.mean((sol-predicitions[:,0])**2)
    return sol, error