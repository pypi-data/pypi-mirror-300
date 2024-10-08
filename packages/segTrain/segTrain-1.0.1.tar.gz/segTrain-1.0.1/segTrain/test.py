import segTrain
    train_loader, val_loader, args, pth_root = select_data("FBP", 8)

    model, args, device = design_model("upernet", "sswin-l", args, pth_root)

    optimizer, scheduler, evaluator, earlystopping = design_optimizer(model, args)

    criterion = design_loss(args)

    train_model(80, model, pth_root, train_loader,val_loader, device, optimizer, scheduler, evaluator, earlystopping, criterion)