from __future__ import annotations
from sentineltools.ai.models import assign_local_model_download
from diffusers import AutoencoderKL
import torch


class AutoVAE:
    def __init__(self, model_name: str = "CompVis/stable-diffusion-v1-4", cache_dir: str = "models\\pretrained\\autovae", device: str = 'cuda'):
        """
        Initializes the AutoVAE class by loading a pretrained VAE model.

        :param model_name: The name or path of the pretrained model to load
        :param cache_dir: Directory to cache the downloaded model
        :param device: Device to load the model on ('cuda' or 'cpu')
        """
        assign_local_model_download()
        self.device = torch.device(device)
        self.vae = AutoencoderKL.from_pretrained(
            model_name,
            subfolder="vae",  # Correct subfolder inside the model repository
            cache_dir=cache_dir  # Directory where the model should be cached
        ).to(self.device)

    def encode(self, image: torch.Tensor) -> torch.Tensor:
        """
        Encodes an image into a latent embedding.

        :param image: Tensor of shape (batch_size, 3, height, width)
        :returns: Latent embedding tensor
        """
        image = image.to(self.device)
        with torch.no_grad():
            embedding = self.vae.encode(image).latent_dist.sample()
            embedding = embedding * self.vae.config.scaling_factor
        return embedding

    def decode(self, embedding: torch.Tensor) -> torch.Tensor:
        """
        Decodes a latent embedding back into an image.

        :param latents: Latent embedding tensor
        :returns: Decoded image tensor
        """
        embedding = embedding.to(self.device)
        embedding = embedding / self.vae.config.scaling_factor
        with torch.no_grad():
            image = self.vae.decode(embedding).sample
        return image
