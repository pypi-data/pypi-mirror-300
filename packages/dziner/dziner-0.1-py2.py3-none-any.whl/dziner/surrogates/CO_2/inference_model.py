# from dziner.surrogates.MOFormer.model.transformer import Transformer, TransformerRegressor # type: ignore
import yaml
import torch
import numpy as np
import sys
import os
import math
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer

class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 2048):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x: Tensor, shape [seq_len, batch_size, embedding_dim]
        """
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)


class regressoionHead(nn.Module):
    # this is adjusted compred to the original MOFormer
    def __init__(self, d_embedding: int):
        super().__init__()
        self.layer1 = nn.Linear(d_embedding, d_embedding//2)
        self.layer2 = nn.Linear(d_embedding//2, d_embedding//4)
        self.layer3 = nn.Linear(d_embedding//4, d_embedding//8)
        self.layer4 = nn.Linear(d_embedding//8, 1)
        self.relu=nn.ReLU()
        

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x: Tensor, shape [seq_len, batch_size, embedding_dim]
        """
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.relu(self.layer3(x))
        
        return self.layer4(x)

class Transformer(nn.Module):

    def __init__(self, ntoken: int, d_model: int, nhead: int, d_hid: int,
                 nlayers: int, dropout: float = 0.1):
        super().__init__()
        self.model_type = 'Transformer'
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = TransformerEncoderLayer(d_model, nhead, d_hid, dropout, batch_first=True)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)
        self.token_encoder = nn.Embedding(ntoken, d_model)
        self.d_model = d_model
        # self.out = nn.Sequential(
        #     nn.LayerNorm(d_model),
        #     nn.Identity(),
        #     nn.Linear(d_model, ntoken) 
        # )
        self.init_weights()

    def init_weights(self) -> None:
        # initrange = 0.1
        # self.encoder.weight.data.uniform_(-initrange, initrange)
        nn.init.xavier_normal_(self.token_encoder.weight)

    def forward(self, src: Tensor) -> Tensor:
        """
        Args:
            src: Tensor, shape [seq_len, batch_size]
            src_mask: Tensor, shape [seq_len, seq_len]

        Returns:
            output Tensor of shape [seq_len, batch_size, ntoken]
        """
        src = self.token_encoder(src) * math.sqrt(self.d_model)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src)
        return output

class TransformerRegressor(nn.Module):
    # def __init__(self, transformer: nn.Module, d_model: int, lstm_hidden_size: int, lstm_num_layers: int = 1):
    #     super().__init__()
    #     self.d_model = d_model
    #     self.transformer = transformer
    #     self.regressionHead = regressoionHead(d_model, lstm_hidden_size, lstm_num_layers)
    def __init__(self, transformer, d_model: int):
        super().__init__()
        self.d_model = d_model
        self.transformer = transformer
        self.regressionHead = regressoionHead(d_model)

        # self.init_weights()

    def init_weights(self) -> None:
        # initrange = 0.1
        # self.encoder.weight.data.uniform_(-initrange, initrange)
        nn.init.xavier_normal_(self.regressionHead.weight)

    def forward(self, src: Tensor) -> Tensor:
        """
        Args:
            src: Tensor, shape [seq_len, batch_size]
            src_mask: Tensor, shape [seq_len, seq_len]

        Returns:
            output Tensor of shape [seq_len, batch_size, ntoken]
        """
        output = self.transformer(src)
        output = self.regressionHead(output[:, 0:1, :])
        return output

def _load_pre_trained_weights(model, path):
        try:            
            # checkpoints_folder = os.path.join(self.config['fine_tune_from'], 'checkpoints')
            checkpoints_folder = config['fine_tune_from']
            load_state = torch.load(path,  map_location=config['gpu']) 
 
            model_state = model.state_dict()

            for name, param in load_state.items():
                if name not in model_state:
                    print('NOT loaded:', name)
                    continue
                else:
                    print('loaded:', name)
                if isinstance(param, nn.parameter.Parameter):
                    # backwards compatibility for serialized parameters
                    param = param.data
                model_state[name].copy_(param)
            print("Loaded pre-trained model with success.")
        except FileNotFoundError:
            print("Pre-trained weights not found. Training from scratch.")

        return model





folder_path = '../dziner/surrogates/CO_2/' 
sys.path.append(folder_path)

if folder_path not in sys.path:
    sys.path.append(folder_path)


config = yaml.load(open(os.path.join(folder_path,("config_ft_transformer.yaml")), "r"), Loader=yaml.FullLoader)

if torch.cuda.is_available() and config['gpu'] != 'cpu':
    device = config['gpu']
    torch.cuda.set_device(device)
    config['cuda'] = True


from tokenizer.mof_tokenizer import MOFTokenizer
tokenizer = MOFTokenizer(os.path.join(folder_path,"tokenizer/vocab_full.txt"))

# inference_model = torch.load(os.path.join(folder_path,'hmof_finetuned_models/hmof_finetuned_0.pth'))
# inference_model.to(device)

def SMILES_to_CO2_adsorption(smiles, inference_model):
    token = np.array([tokenizer.encode(smiles, max_length=512, truncation=True,padding='max_length')])
    token = torch.from_numpy(np.asarray(token))
    token = token.to(device)
    return inference_model(token).item()


def predict_CO2_adsorption_with_uncertainty(smiles):
    predictions = []
    for fold in range(5):
        inference_model = torch.load(os.path.join(folder_path,f'hmof_finetuned_models/hmof_finetuned_{fold}.pth'))
        inference_model.to(device)
        predictions.append(SMILES_to_CO2_adsorption(smiles, model=inference_model))
    return np.mean(predictions), np.std(predictions)