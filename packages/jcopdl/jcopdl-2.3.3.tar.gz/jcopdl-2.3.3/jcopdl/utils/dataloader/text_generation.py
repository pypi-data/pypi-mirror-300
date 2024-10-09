from pathlib import Path

import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
from torchtext.vocab import build_vocab_from_iterator


class SpecialTokens:
    """
    special_tokens: List[Tuple(token_name, token_value)]
    """
    def __init__(self, unknown_tokens=None, start_token=None, stop_token=None, pad_token=None, mask_token=None, separator_token=None, classification_token=None):
        self.UNK = unknown_tokens
        self.BOS = start_token
        self.EOS = stop_token
        self.PAD = pad_token
        self.MASK = mask_token
        self.SEP = separator_token
        self.CLS = classification_token

        tokens = [unknown_tokens, start_token, stop_token, pad_token, mask_token, separator_token, classification_token]
        self.values = [token for token in tokens if token is not None]


class SlidingWindowTextDataset(Dataset):
    """
    Create Dataset with a sliding window through rows of sentences

    == Arguments ==
    txt_path: str
        alamat menuju dataset. Data mesti berupa file txt yang setiap barisnya merupakan 1 data

    tokenizer: function(text) -> list[str]
        a function that accepts string text input and returns a list of tokenized string

    unknown_token: str
        token yang ingin digunakan untuk kata yang belum pernah terlihat sebelumnya        

    start_token: str
        token sebagai penanda awal dari sebuah data

    stop_token: str
        token sebagai penanda akhir sebuah data

    window_length: int, range, None
        ukuran window untuk ekstrak data.
        - Jika int, misal window_length = 3, maka akan diambil per 3 kata untuk memprediksi 1 kata setelahnya.
        - Jika range, misal window_length = range(1, 3), maka akan diambil semua dari 1 kata hingga 3 kata, untuk memprediksi 1 kata setelahnya.
        - Jika None or 0, maka akan digunakan kalimat penuh

    window_stride: int
        stride dari window saat ekstraksi data. Misal window_stride = 1, maka window akan digeser per 1 kata.

    output_sequence: bool
        apakah hanya ingin menggunakan 1 data sebagai target (many to one)
        - Jika True, maka output berupa sequence (Many to Many)
        - Jika False, maka output berupa 1 data (Many to One)
    """
    def __init__(self, txt_path: str, tokenizer=None, unknown_token: str="[UNKNOWN]", start_token="[START]", stop_token="[STOP]", pad_token="[PAD]", window_length=8, window_stride=1, output_sequence=False):
        if tokenizer is None:
            tokenizer = lambda text: text.strip().lower().split()
        self.tokenizer = tokenizer
        
        self.window_length, self.use_window = self._compute_window(window_length)
        self.window_stride = window_stride
        self.output_sequence = output_sequence

        self.SPECIAL_TOKENS = SpecialTokens(
            unknown_tokens=unknown_token,
            start_token=start_token,
            stop_token=stop_token,
            pad_token=pad_token
        )

        self.sentences = self._load_data(txt_path)
        self.vocab = self._create_vocab()
        self.X, self.y = self._create_sequences()

        self.UNK_ID, self.BOS_ID, self.EOS_ID, self.PAD_ID = self.vocab([unknown_token, start_token, stop_token, pad_token])
    
    def __getitem__(self, index):        
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)

    def _compute_window(self, window_length):
        if window_length is None:
            return range(0, 1), False
        
        if isinstance(window_length, int):
            use_window = window_length > 0
            return range(window_length, window_length+1), use_window
        
        if isinstance(window_length, range):
            assert window_length.start > 0, "Start window should be larger than 0"
            return window_length, True

    def _load_data(self, txt_path):
        data_path = Path(txt_path)
        assert data_path.suffix == ".txt"
        
        with open(data_path, "r") as f:
            sentences = [[self.SPECIAL_TOKENS.BOS, *self.tokenizer(sentence), self.SPECIAL_TOKENS.EOS] for sentence in f]
            sentences.sort(key=len)
        return sentences
    
    def _create_vocab(self):
        vocab = build_vocab_from_iterator(self.sentences, specials=self.SPECIAL_TOKENS.values)
        vocab.set_default_index(vocab[self.SPECIAL_TOKENS.UNK])
        return vocab
    
    def _create_sequences(self):
        sentences_tensor = [torch.LongTensor(self.vocab(sentence)) for sentence in self.sentences]
        X = []
        y = []
        for length in self.window_length:
            for tensor in sentences_tensor:
                ngrams = tensor.unfold(0, length + 1, self.window_stride) if self.use_window else tensor.view(1, -1)
                X.extend(ngrams[:, :-1].tolist())
                if self.output_sequence:
                    y.extend(ngrams[:, 1:].tolist())
                else:
                    y.extend(ngrams[:, -1].tolist())
        return X, y
    

class SlidingWindowTextDataLoader(DataLoader):
    def __init__(self, dataset: SlidingWindowTextDataset, batch_size=1, drop_last=True, num_workers=0):
        super().__init__(dataset, batch_size, shuffle=False, collate_fn=self.collate, num_workers=num_workers, drop_last=drop_last)    

    def collate(self, batch):
        Xb, yb = zip(*batch)
        Xb = pad_sequence([torch.LongTensor(x) for x in Xb], batch_first=True, padding_value=self.dataset.PAD_ID)
        if self.dataset.output_sequence:
            yb = pad_sequence([torch.LongTensor(y) for y in yb], batch_first=True, padding_value=self.dataset.PAD_ID)
        else:
            yb = torch.LongTensor(yb)
        return Xb, yb
