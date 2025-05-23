import hydra
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from hydra.utils import get_original_cwd
import os

@hydra.main(config_path='config', config_name='config',version_base=None)
def train(cfg):
    # Load Model with config file
    traffic_data_path = os.path.join(get_original_cwd(), "5GT-GAN/data/Traffics.csv")
    model = hydra.utils.instantiate(cfg.model)

    # Set Checkpoint config
    ckpt_callback = ModelCheckpoint(
        dirpath=f'ckpt_{cfg.model_name}_exp_V{cfg.version}',
        filename=f'{cfg.model_name}' + '-{epoch:02d}',
        every_n_epochs=10,
        save_top_k=-1
    )

    # Set Train options
    trainer = Trainer(accelerator="auto",devices="auto", log_every_n_steps=1,
                      num_sanity_val_steps=0, max_epochs=-1, callbacks=[ckpt_callback])

    # Load datamodule
    dm = hydra.utils.instantiate(cfg.data)

    # Train
    trainer.fit(model, dm)


if __name__ == "__main__":
    train()
