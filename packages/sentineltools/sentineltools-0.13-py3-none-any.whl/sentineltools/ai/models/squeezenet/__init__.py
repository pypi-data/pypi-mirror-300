import torch
import torch.nn as nn
import torchvision.models as models
import os


class SqueezeNet:
    def __init__(self, cache_dir: str = "models\\pretrained\\squeezenet", device: str = 'cuda'):
        """
        Initializes the SqueezeNet class by loading a pretrained SqueezeNet model.
        If the model is cached, it will load it from the cache_dir, otherwise it
        will download and save the model in the cache_dir.

        :param cache_dir: Directory to cache the downloaded model
        :param device: Device to load the model on ('cuda' or 'cpu')
        """
        self.device = torch.device(device)
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

        # Path to cache the model
        model_path = os.path.join(self.cache_dir, 'squeezenet1_1.pth')

        # Load the model, either from cache or by downloading
        if os.path.exists(model_path):
            # print(f"Loading model from cache: {model_path}")
            self.model = models.squeezenet1_1()
            self.model.load_state_dict(torch.load(model_path, weights_only=True))
        else:
            # print("Downloading and caching the model...")
            self.model = models.squeezenet1_1(
                weights=models.SqueezeNet1_1_Weights.DEFAULT
            )
            # Save model to the cache directory
            torch.save(self.model.state_dict(), model_path)

        self.model.classifier = nn.Identity()
        self.model.to(self.device)

    def encode(self, image: torch.Tensor) -> torch.Tensor:
        """
        Encodes an image into a latent embedding.

        :param image: Tensor of shape (batch_size, 3, height, width)
        :returns: Latent embedding tensor
        """
        image = image.to(self.device)
        with torch.no_grad():
            # Here you may want to replace with actual encoding logic.
            embedding = self.model(image)
        return embedding
