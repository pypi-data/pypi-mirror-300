from IPython.display import HTML
        

SNIPPETS = {
    "name": "J.COp DL Snippets",
    "menu": {
        "Import Common Packages": """
            %load_ext autoreload
            %autoreload 2                         

            import torch
            from torch import nn, optim
            from jcopdl.callback import Callback

            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            device
        """,
        "Dataset & Dataloader": {
            "Multiclass Image Classification": """
                from torchvision import datasets, transforms
                from torch.utils.data import DataLoader

                bs = "______"

                train_transform = transforms.Compose([
                    "____________",
                    transforms.ToTensor()
                ])

                test_transform = transforms.Compose([
                    "____________",
                    transforms.ToTensor()
                ])

                train_set = datasets.ImageFolder("________", transform=train_transform)
                trainloader = DataLoader(train_set, batch_size=bs, shuffle=True)

                test_set = datasets.ImageFolder("________", transform=test_transform)
                testloader = DataLoader(test_set, batch_size=bs, shuffle="____")


                configs = {
                    "batch_size": bs,
                    'classes': train_set.classes,
                    'transform': test_transform
                }
            """,
            "CharRNN Text Classification": """
                from jcopdl import transforms
                from jcopdl.utils.dataloader import CharRNNDataset, CharRNNDataloader

                train_set = CharRNNDataset("data / train.csv", text_col="_______", label_col="_______", max_len=_______)
                test_set = CharRNNDataset("data / test.csv", text_col="_______", label_col="_______", chars=train_set.chars, classes=train_set.classes, pad=train_set.pad, max_len=_______)

                bs = "______"
                transform = transforms.Compose([
                    transforms.PadSequence(),
                    transforms.OneHotEncode(train_set.n_chars),
                    transforms.TruncateSequence(200)
                ])

                trainloader = CharRNNDataloader(train_set, batch_size=bs, batch_transform=transform, drop_last=True)
                testloader = CharRNNDataloader(test_set, batch_size=bs, batch_transform=transform, drop_last=True)


                configs = {
                    "batch_size": bs,
                    "chars": train_set.chars,
                    "pad": train_set.pad,
                    "classes": train_set.classes,
                    "transform": transform
                }
            """
        },
        "Exploratory Data Analysis": {
            "Visualize Batch": """
                from jcopdl.visualization import visualize_image_batch

                feature, target = next(iter(trainloader))
                visualize_image_batch(feature, n_col=8)
            """
        },
        "Architecture": {
            "ANN Regression": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ANN(nn.Module):
                    def __init__(self, input_size, n1, n2, output_size, dropout):
                        super().__init__()
                        self.fc = nn.Sequential(
                            linear_block(input_size, n1, dropout=dropout),
                            linear_block(n1, n2, dropout=dropout),
                            linear_block(n2, output_size, activation="identity")
                        ),
                    
                    def forward(self, x):
                        return self.fc(x)
                    

                configs["model"] = {
                    "input_size": train_set.n_features,
                    "n1": 128,
                    "n2": 64,
                    "output_size": 1,
                    "dropout": 0
                }
            """,
            "ANN Multiclass Classification": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ANN(nn.Module):
                    def __init__(self, input_size, n1, n2, output_size, dropout):
                        super().__init__()
                        self.fc = nn.Sequential(
                            linear_block(input_size, n1, dropout=dropout),
                            linear_block(n1, n2, dropout=dropout),
                            linear_block(n2, output_size, activation="lsoftmax")
                        ),
                    
                    def forward(self, x):
                        return self.fc(x)
                    

                configs["model"] = {
                    "input_size": train_set.n_features,
                    "n1": 128,
                    "n2": 64,
                    "output_size": 1,
                    "dropout": 0
                }
            """,
            "CNN Multiclass Classification": """
                from torch import nn
                from jcopdl.layers import linear_block, conv_block

                class CNN(nn.Module):
                    def __init__(self, output_size, fc_dropout):
                        super().__init__()
                        self.conv = nn.Sequential(
                            conv_block("___", "___"),
                            conv_block("___", "___"),
                            nn.Flatten()
                        )
                        
                        self.fc = nn.Sequential(
                            linear_block("_____", "_____", dropout=fc_dropout),
                            linear_block("_____", output_size, activation="lsoftmax")
                        )
                        
                    def forward(self, x):
                        return self.fc(self.conv(x))
                    

                configs["model"] = {
                    "output_size": len(train_set.classes),
                    "fc_dropout": 0
                }
            """,
            "RNN Many-to-Many Regression": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ManytoManyRNN(nn.Module):
                    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
                        super().__init__()
                        self.rnn = nn.RNN(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)
                        self.fc = linear_block(hidden_size, output_size, activation="identity")
                        
                    def forward(self, x, hidden):        
                        x, hidden = self.rnn(x, hidden)
                        x = self.fc(x)
                        return x, hidden


                configs["model"] = {
                    "input_size": ________,
                    "output_size": ________,
                    "hidden_size": 64,
                    "num_layers": 2,
                    "dropout": 0
                }    
            """,
            "RNN Many-to-One Classification": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ManyToOneRNN(nn.Module):
                    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
                        super().__init__()
                        self.rnn = nn.RNN(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)
                        self.fc = linear_block(num_layers*hidden_size, output_size, activation="lsoftmax")
                        
                    def forward(self, x, hidden):        
                        x, hidden = self.rnn(x, hidden)
                        n_layers, n_batch, n_hidden = hidden.shape
                        last_state = hidden.permute(1, 0, 2).reshape(-1, n_layers*n_hidden) # LBH -> BLH -> BF
                        x = self.fc(last_state)
                        return x, hidden


                configs["model"] = {
                    "input_size": ________,
                    "output_size": ________,
                    "hidden_size": 64,
                    "num_layers": 2,
                    "dropout": 0
                }
            """,
            "LSTM Many-to-Many Regression": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ManytoManyLSTM(nn.Module):
                    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
                        super().__init__()
                        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)
                        self.fc = linear_block(hidden_size, output_size, activation="identity")
                        
                    def forward(self, x, hidden):        
                        x, hidden = self.rnn(x, hidden)
                        x = self.fc(x)
                        return x, hidden


                configs["model"] = {
                    "input_size": ________,
                    "output_size": ________,
                    "hidden_size": 64,
                    "num_layers": 2,
                    "dropout": 0
                }
            """,
            "LSTM Many-to-One Classification": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ManyToOneLSTM(nn.Module):
                    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
                        super().__init__()
                        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)
                        self.fc = linear_block(num_layers*2*hidden_size, output_size, activation="lsoftmax")
                        
                    def forward(self, x, hidden):        
                        x, (h, c) = self.rnn(x, hidden)
                        state = torch.cat([h, c], dim=2)
                        n_layers, n_batch, n_2hidden = state.shape
                        last_state = state.permute(1, 0, 2).reshape(-1, n_layers*n_2hidden) # LBH -> BLH -> BF
                        x = self.fc(last_state)
                        return x, (h, c)


                configs["model"] = {
                    "input_size": ________,
                    "output_size": ________,
                    "hidden_size": 64,
                    "num_layers": 2,
                    "dropout": 0
                }
            """,
            "GRU Many-to-Many Regression": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ManytoManyGRU(nn.Module):
                    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
                        super().__init__()
                        self.rnn = nn.GRU(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)
                        self.fc = linear_block(hidden_size, output_size, activation="identity")
                        
                    def forward(self, x, hidden):        
                        x, hidden = self.rnn(x, hidden)
                        x = self.fc(x)
                        return x, hidden


                configs["model"] = {
                    "input_size": ________,
                    "output_size": ________,
                    "hidden_size": 64,
                    "num_layers": 2,
                    "dropout": 0
                }
            """,
            "GRU Many-to-One Classification": """
                from torch import nn
                from jcopdl.layers import linear_block

                class ManyToOneGRU(nn.Module):
                    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
                        super().__init__()
                        self.rnn = nn.GRU(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)
                        self.fc = linear_block(num_layers*hidden_size, output_size, activation="lsoftmax")
                        
                    def forward(self, x, hidden):        
                        x, hidden = self.rnn(x, hidden)
                        n_layers, n_batch, n_hidden = hidden.shape
                        last_state = hidden.permute(1, 0, 2).reshape(-1, n_layers*n_hidden) # LBH -> BLH -> BF
                        x = self.fc(last_state)
                        return x, hidden


                configs["model"] = {
                    "input_size": ________,
                    "output_size": ________,
                    "hidden_size": 64,
                    "num_layers": 2,
                    "dropout": 0
                }
            """,
            "Transfer Learning Template": """
                class TLModel(nn.Module):
                    def __init__(self):
                        super().__init__()
                        self.model = _______
                        self.freeze()
                        
                    def freeze(self):
                        for param in self.model.parameters():
                            param.requires_grad = False
                            
                    def unfreeze(self):
                        for param in self.model.parameters():
                            param.requires_grad = True
                            
                    def forward(self, x):
                        return self.model(x)
            """
        },
        "Training Preparation": {
            "Standard": """
                configs["optimizer"] = {"lr": 0.001}                         

                model = _______(**configs["model"]).to(device)
                criterion = _______
                optimizer = optim.AdamW(model.parameters(), **configs["optimizer"])
                callback = Callback(model, configs, optimizer, outdir="_______")
                                
                # Plot Loss
                callback.add_plot(["train_cost", "test_cost"], scale="semilogy")
                # Plot Score
                callback.add_plot(["train_score", "test_score"], scale="linear_positive")
                # Plot Image
                callback.add_image("test_predict")
            """,            
            "with OneCycleLR": """
                configs["scheduler"] = {
                    "pct_start": 0.2,
                    "max_lr": 1e-3,
                    "div_factor": 10,
                    "final_div_factor": 1000,
                    "steps_per_epoch": len(train_set) // bs + 1,
                    "epochs": 100
                }                      

                model = _______(**configs["model"]).to(device)
                criterion = _______
                optimizer = optim.AdamW(model.parameters())
                scheduler = optim.lr_scheduler.OneCycleLR(optimizer, **configs["scheduler"])
                callback = Callback(model, configs, optimizer, scheduler, max_epoch=100, outdir="_______")
                                
                # Plot Loss
                callback.add_plot(["train_cost", "test_cost"], scale="semilogy")
                # Plot Score
                callback.add_plot(["train_score", "test_score"], scale="linear_positive")
                # Plot Image
                callback.add_image("test_predict")
            """
        },
        "Training Loop": {
            "Standard Loop + Accuracy": """
                from tqdm.auto import tqdm
                from jcopdl.metrics import MiniBatchCost, MiniBatchAccuracy
                from jcopdl.visualization import visualize_prediction_batch


                def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):
                    if mode == "train":
                        model.train()
                    elif mode == "test":
                        model.eval()
                    
                    cost = MiniBatchCost()
                    score = MiniBatchAccuracy()
                    for feature, target in tqdm(dataloader, desc=mode.title(), leave=False):
                        feature, target = feature.to(device), target.to(device)
                        output = model(feature)
                        loss = criterion(output, target)
                        
                        if mode == "train":
                            loss.backward()
                            optimizer.step()
                            optimizer.zero_grad()

                        cost.add_batch(loss, feature.size(0))
                        score.add_batch(output, target)
                    callback.log(f"{mode}_cost", cost.compute())
                    callback.log(f"{mode}_score", score.compute())
                    
                    if mode == "test":
                        preds = output.argmax(1)
                        classes = dataloader.dataset.classes
                        image = visualize_prediction_batch(feature, target, preds, classes)
                        callback.log_image("test_predict", image)
            """,
            "Standard Loop + F1": """
                from tqdm.auto import tqdm
                from jcopdl.metrics import MiniBatchCost, MiniBatchBinaryF1


                def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):
                    if mode == "train":
                        model.train()
                    elif mode == "test":
                        model.eval()
                    
                    cost = MiniBatchCost()
                    score = MiniBatchBinaryF1()
                    for feature, target in tqdm(dataloader, desc=mode.title(), leave=False):
                        feature, target = feature.to(device), target.to(device)
                        output = model(feature)
                        loss = criterion(output, target)
                        
                        if mode == "train":
                            loss.backward()
                            optimizer.step()
                            optimizer.zero_grad()

                        cost.add_batch(loss, feature.size(0))
                        score.add_batch(output, target)
                    callback.log(f"{mode}_cost", cost.compute())
                    callback.log(f"{mode}_score", score.compute(pos_label=1))
            """,
            "RNN Loop": """
                from tqdm.auto import tqdm
                from torch.nn.utils import clip_grad_norm_
                from jcopdl.metrics import MiniBatchCost, MiniBatchBinaryF1


                def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):
                    if mode == "train":
                        model.train()
                    elif mode == "test":
                        model.eval()
                    
                    cost = MiniBatchCost()
                    score = MiniBatchBinaryF1()
                    for feature, target in tqdm(dataloader, desc=mode.title(), leave=False):
                        feature, target = feature.to(device), target.to(device)
                        output, hidden = model(feature, None)
                        loss = criterion(output, target)
                        
                        if mode == "train":
                            loss.backward()
                            clip_grad_norm_(model.parameters(), 2)
                            optimizer.step()
                            optimizer.zero_grad()

                        cost.add_batch(loss, feature.size(0))
                        score.add_batch(output, target)
                    callback.log(f"{mode}_cost", cost.compute())
                    callback.log(f"{mode}_score", score.compute(pos_label=1))
            """,
            "RNN TBPTT Loop": """
                from tqdm.auto import tqdm
                from torch.nn.utils import clip_grad_norm_
                from jcopdl.metrics import MiniBatchCost, MiniBatchBinaryF1


                def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):
                    if mode == "train":
                        model.train()
                    elif mode == "test":
                        model.eval()
                    
                    cost = MiniBatchCost()
                    score = MiniBatchBinaryF1()
                    for (prior, feature), target in tqdm(dataloader, desc=mode.title(), leave=False):
                        prior, feature, target = prior.to(device), feature.to(device), target.to(device)
                        with torch.no_grad():
                            output, hidden = model(prior, None)
                        output, hidden = model(feature, hidden)
                        loss = criterion(output, target)
                        
                        if mode == "train":
                            loss.backward()
                            clip_grad_norm_(model.parameters(), 2)
                            optimizer.step()
                            optimizer.zero_grad()

                        cost.add_batch(loss, feature.size(0))
                        score.add_batch(output, target)
                    callback.log(f"{mode}_cost", cost.compute())
                    callback.log(f"{mode}_score", score.compute(pos_label=1))
            """
        },
        "Training": {
            "Minimize Cost": """
                while True:
                    train_loop_fn("train", trainloader, model, criterion, optimizer, callback, device)
                    with torch.no_grad():
                        train_loop_fn("test", testloader, model, criterion, optimizer, callback, device)
                    
                    if callback.early_stopping("minimize", "test_cost"):
                        model = callback.load_best_state()
                        break
            """,
            "Maximize Score": """
                while True:
                    train_loop_fn("train", trainloader, model, criterion, optimizer, callback, device)
                    with torch.no_grad():
                        train_loop_fn("test", testloader, model, criterion, optimizer, callback, device)
                    
                    if callback.early_stopping("maximize", "test_score"):
                        model = callback.load_best_state()                         
                        break
            """,
            "Transfer Learning with Unfreezing": """
                phase = 1
                while True:
                    train_loop_fn("train", trainloader, model, criterion, optimizer, callback, device)
                    with torch.no_grad():
                        train_loop_fn("test", testloader, model, criterion, optimizer, callback, device)

                    if callback.early_stopping("maximize", "test_score"):
                        phase += 1
                        match phase:
                            case 2: # Phase 2: Fine-tuning
                                model.unfreeze()
                                callback.early_stop_patience = _____
                                configs["optimizer"] = {"lr": _____}
                                optimizer = optim.AdamW(model.parameters(), **configs["optimizer"])  
                            case 3: # Phase 3: 2nd Fine-tuning
                                model = callback.load_best_state()
                                callback.early_stop_patience = _____
                                configs["optimizer"] = {"lr": _____}
                                optimizer = optim.AdamW(model.parameters(), **configs["optimizer"])
                            case 4:
                                model = callback.load_best_state()
                                break
            """,
            "Multiphase Training": """
                phase = 1
                while True:
                    train_loop_fn("train", trainloader, model, criterion, optimizer, callback, device)
                    with torch.no_grad():
                        train_loop_fn("test", testloader, model, criterion, optimizer, callback, device)

                    if callback.early_stopping("maximize", "test_score"):
                        phase += 1
                        match phase:
                            case 2: # Phase 2: Fine-tuning
                                callback.early_stop_patience = 25
                                configs["optimizer"] = {"lr": 1e-4}
                                optimizer = optim.AdamW(model.parameters(), **configs["optimizer"])  
                            case 3: # Phase 3: 2nd Fine-tuning
                                model = callback.load_best_state()
                                callback.early_stop_patience = 20
                                configs["optimizer"] = {"lr": 1e-5}
                                optimizer = optim.AdamW(model.parameters(), **configs["optimizer"])
                            case 4:
                                model = callback.load_best_state()
                                break                
            """
        },
        "Evaluation": {
            "Visualize Classification": """
                from jcopdl.eval import evaluate_prediction

                configs = torch.load("______/configs.pth")

                train_set = datasets.ImageFolder("______", transform=configs["transform"])
                trainloader = DataLoader(train_set, batch_size=configs["batch_size"], shuffle=True)

                test_set = datasets.ImageFolder("______", transform=configs["transform"])
                testloader = DataLoader(test_set, batch_size=configs["batch_size"], shuffle=True)

                img_train = evaluate_prediction(trainloader, model, device)
                img_test = evaluate_prediction(testloader, model, device)
            """,
            "Evaluate Accuracy": """
                from jcopdl.eval import evaluate_accuracy
                
                configs = torch.load("______/configs.pth")

                train_set = datasets.ImageFolder("______", transform=configs["transform"])
                trainloader = DataLoader(train_set, batch_size=configs["batch_size"], shuffle=False)

                test_set = datasets.ImageFolder("______", transform=configs["transform"])
                testloader = DataLoader(test_set, batch_size=configs["batch_size"], shuffle=False)
                                
                acc_train = evaluate_accuracy(trainloader, model, device)
                acc_test = evaluate_accuracy(testloader, model, device)
            """,
            "Evaluate Confusion Matrix": """
                from jcopdl.eval import evaluate_confusion_matrix
                from jcopdl.visualization import plot_confusion_matrix

                configs = torch.load("______/configs.pth")

                train_set = datasets.ImageFolder("______", transform=configs["transform"])
                trainloader = DataLoader(train_set, batch_size=configs["batch_size"], shuffle=False)

                test_set = datasets.ImageFolder("______", transform=configs["transform"])
                testloader = DataLoader(test_set, batch_size=configs["batch_size"], shuffle=False)

                cm_train = evaluate_confusion_matrix(trainloader, model, device)
                cm_test = evaluate_confusion_matrix(testloader, model, device)

                fig = plot_confusion_matrix([cm_train, cm_test], configs["classes"])
            """,
            "Evaluate Misclassified": """
                from jcopdl.eval import evaluate_misclassified

                configs = torch.load("______/configs.pth")

                test_set = datasets.ImageFolder("______", transform=configs["transform"])
                testloader = DataLoader(test_set, batch_size=configs["batch_size"], shuffle=False)

                images = evaluate_misclassified(testloader, model, device)
            """
        },
        "Load": {
            "Load Checkpoint": """
                from jcopdl.io import load_from_checkpoint

                checkpoint = load_from_checkpoint("_______/checkpoint/_________.pth")
                model, optimizer, scheduler, callback = checkpoint.model, checkpoint.optimizer, checkpoint.scheduler, checkpoint
                criterion = _______
            """,
            "Load Model": """
                import torch
                device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

                model = torch.load("______/model_best.pth", map_location="cpu").to(device)
            """,
            "Load Config": """
                import torch

                configs = torch.load("______/configs.pth")
            """
        }      
    }
}

COPIED_HTML = HTML("""
    <style>
        /* Style for the box */
        .jcopml-snippet-box {
            background-color: #008000;
            color: white;
            padding: 5px 10px;
            line-height: 30px;
            border-radius: 5px;
        }

        /* Fading animation */
        .jcopml-snippet-fade-out {
            opacity: 1;
            animation: fadeOut 3s ease forwards;
        }
        @keyframes fadeOut {
            from { opacity: 1 }
            to { opacity: 0 }
        }    
    </style>
    <span class="jcopml-snippet-box jcopml-snippet-fade-out">Copied &#10003;</span>
""")
