import os
import shutil
import json
from TSHIELD.TSHIELD import rshield,xshield
from TSHIELD.procedures import procedures
import torch
import torch.nn.functional as F
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard.writer import SummaryWriter
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

from torch.utils.data import random_split
from TSHIELD.tests.parser import arg_parser

from ReVel.perturbations import get_perturbation
from ReVel.load_data import load_data

n_classes = {
    "CIFAR10": 10,
    "CIFAR100": 100,
    "EMNIST": 47,
    "FashionMNIST": 10,
    "Flowers": 102,
    "OxfordIIITPet": 37,
}

if torch.cuda.is_available():
    torch.set_num_threads(4)
else:
    torch.set_num_threads(2)
device = "cuda" if torch.cuda.is_available() else "cpu"

if __name__ == "__main__":
    args_parser = arg_parser()

    args = args_parser.parse_args()

    classifier = procedures.classifier(args.pretrained_model, n_classes[args.dataset])
    classifier.to(device)

    configuration = "R-SHIELD" if args.rshield else ("X-SHIELD" if args.xshield else "Baseline")

    config_name = f"{configuration}_{args.pretrained_model}" + (
        "" if configuration == "Baseline" else f"_{args.percentage}"
    )
    save_model_dir = f"results/{args.dataset}/{config_name}"

    if args.force:
        shutil.rmtree(save_model_dir, ignore_errors=True)
    else:
        # Si no existe el directorio, lo creo
        if not os.path.exists(save_model_dir):
            os.makedirs(save_model_dir)
        else:
            event_accum = EventAccumulator(save_model_dir)
            event_accum.Reload()
            
            # Abro el tensorboard y compruebo si hay Test/Accuracy. Si lo hay, no hago nada. Si no, lo hago.
            if "Test/Accuracy" in event_accum.Tags()["scalars"] and "Test/Loss" in event_accum.Tags()["scalars"]:
                print("Acc: " + event_accum.Scalars("Test/Accuracy")[-1].value)
                print("Loss: " + event_accum.Scalars("Test/Loss")[-1].value)
                raise ValueError("Model already tested: " + save_model_dir)


    # transform = procedures.data_augmentation(args)

    perturbation = get_perturbation(
        name="square",
        dim=9,
        num_classes=n_classes[args.dataset],
        final_size=(224, 224),
        kernel=150.0,
        max_dist=20,
        ratio=0.5,
    )
    Train = load_data(
        args.dataset, perturbation=perturbation, train=True, dir="./data/"
    )
    Train, Val = random_split(
        Train, [int(len(Train) * 0.9), len(Train) - int(len(Train) * 0.9)]
    )
    TrainLoader = DataLoader(Train, batch_size=args.batch_size, shuffle=True)
    ValLoader = DataLoader(Val, batch_size=args.batch_size, shuffle=False)

    def loss_f(ypred, y_label):
        return F.cross_entropy(ypred, torch.argmax(y_label, 1))

    optimizer = torch.optim.AdamW(
        classifier.parameters(), lr=args.lr, weight_decay=0.01, amsgrad=True
    )
    epochs = 80

    if not os.path.exists(f"results/{args.dataset}/"):
        os.makedirs(f"results/{args.dataset}/")
    if os.path.exists(f"results/{args.dataset}/{config_name}"):
        shutil.rmtree(f"results/{args.dataset}/{config_name}")

    if not os.path.exists(f"results/{args.dataset}/{config_name}"):
        os.makedirs(f"results/{args.dataset}/{config_name}")
    best_loss = float("inf")

    writer = SummaryWriter(log_dir=f"results/{args.dataset}/{config_name}")
    dumped = json.dumps(vars(args), indent=4)

    writer.add_text("config", dumped)
    with open(f"results/{args.dataset}/{config_name}/config.json", "w") as f:
        f.write(dumped)
    best_loss = torch.inf

    for epoch in range(epochs):
        print(f"Epoch :{epoch+1}, {(epoch+1)/epochs*100:.2f}%")
        train_loss, train_acc, train_reg = procedures.train_step(
            ds_loader=TrainLoader,
            model=classifier,
            optimizer=optimizer,
            loss_f=loss_f,
            reg_f=lambda x,y:rshield(model=x,input=y,percentage=args.percentage,device=device) if args.rshield else 
                            xshield(model=x,input=y,percentage=args.percentage,device=device) if args.xshield else None,
            device=device,
            #transform=transform,
        )
        writer.add_scalar("Train/Accuracy", train_acc, epoch)
        writer.add_scalar("Train/Loss", train_loss, epoch)
        writer.add_scalar("Train/Regularization", train_reg, epoch)

        val_loss, val_acc, val_reg = procedures.validation_step(
            ds_loader=ValLoader,
            model=classifier,
            loss_f=loss_f,
            reg_f=lambda x,y:rshield(model=x,input=y,percentage=args.percentage,device=device) if args.rshield else 
                            xshield(model=x,input=y,percentage=args.percentage,device=device) if args.xshield else None,
            device=device,
        )
        writer.add_scalar("Val/Accuracy", val_acc, epoch)
        writer.add_scalar("Val/Loss", val_loss, epoch)
        writer.add_scalar("Val/Regularization", val_reg, epoch)
        if val_loss + val_reg < best_loss:
            best_loss = val_loss + val_reg
            torch.save(classifier.state_dict(), save_model_dir+"/model.pt")
            print("Saved model")

    classifier.load_state_dict(torch.load(save_model_dir+"/model.pt"), map_location=device)

    test = load_data(
        args.dataset,
        perturbation=perturbation,
        train=False,
        dir=f"./data/{args.dataset}/",
    )
    TestLoader = DataLoader(test, batch_size=args.batch_size, shuffle=False)
    test_loss, test_acc, test_reg = procedures.validation_step(
        ds_loader=TestLoader, model=classifier, loss_f=loss_f, 
        reg_f= lambda x,y:rshield(model=x.to(device),input=y.to(device),percentage=args.percentage) if args.rshield else 
                        xshield(model=x.to(device),input=y.to(device),percentage=args.percentage,device=device) if args.xshield else None,
        device=device
    )

    writer.add_scalar("Test/Loss", test_loss, 0)
    writer.add_scalar("Test/Accuracy", test_acc, 0)
    writer.add_scalar("Test/Regularization", test_reg, 0)
    writer.close()
