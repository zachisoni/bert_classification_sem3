import argparse

from utils.preprocessor import PreprocessorClass
from models.multi_class_model import MultiClassModel

import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger

def collect_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--accelerator", type=str, default='gpu')
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--num_nodes", type=int, default=1)
    parser.add_argument("--batch_size", type=int, default=10)
    parser.add_argument("--max_length", type=int, default=100)
    parser.add_argument("--test_data_dir", type=str, default="data/testing.res")
    parser.add_argument("--test_data_dir", type=str, default="data/training.res")

    return parser.parse_args()

if __name__ == '__main__':
    args = collect_parser()

    dm = PreprocessorClass(preprocessed_dir = "bert_classification_sem3/data/preprocessed",
                           train_data_dir= args.train_data_dir,
                           test_data_dir= args.test_data_size,
                           batch_size = args.batch_size,
                           max_length = args.max_length)

    # Learning rate diganti 1e-3 ke 1e-5
    model = MultiClassModel(
        n_out = 5,
        dropout = 0.3,
        lr = 1e-5
    )

    logger = TensorBoardLogger("logs", name="bert-multi-class")

    trainer = pl.Trainer(
        accelerator= args.accelerator,
        gpus = args.gpu_id,
        num_nodes=args.num_nodes,
        max_epochs = 10,
        default_root_dir = "bert_classification_sem3/checkpoints/class",
        logger= logger
    )

    trainer.fit(model, datamodule = dm)
    # pred, true = trainer.predict(model = model, datamodule = dm)

