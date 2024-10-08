from __future__ import annotations
from typing import Union
import torch.nn.functional as F
import cv2
from torch.optim import Adam
import pickle

from sentineltools.images import load_image, thumbnail_fill, convert_image_format, from_pil_image
from sentineltools.utils.progressbar import ProgressBar
from sentineltools.ai.models.autovae import AutoVAE

from torch.utils.data import Dataset
import os
import torch.nn as nn
import torch

from PIL import Image


class NextFrameGeneratorDataset(Dataset):
    def __init__(self, model: NextFrameGenerator, autovae: AutoVAE, folder_path: str, chunk_size: int = 16, frame_frequency: int = 5, overwrite_frames: bool = False, overwrite_cache: bool = False):
        """
        Initializes the ClipDataset class.

        :param folder_path: path to the main folder containing clip folders (should contain folders with numbered images like car\\frame_001.png)
        :param model: An instance of the NextFrameGenerator model to preprocess images
        """
        self.folder_path = folder_path
        self.model = model
        self.autovae = autovae
        self.chunk_size = chunk_size
        self.data = []

        # Load and process all clip folders
        self._create_frames_from_videos(
            folder_path, frame_frequency, overwrite_frames)
        self._load_data(overwrite_cache)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx) -> tuple[list[tuple[torch.Tensor, str]], tuple[torch.Tensor, str]]:
        """
        Returns an example from the dataset.

        :param idx: Index of the example to return
        :returns: Tuple of (list of tensors, target tensor)
        """
        return self.data[idx]

    def _load_data(self, overwrite_cache: bool = False):
        """
        Loads and processes images from clip folders into the dataset, with caching support.
        """
        clip_folders = [os.path.join(self.folder_path, d) for d in os.listdir(
            self.folder_path) if os.path.isdir(os.path.join(self.folder_path, d)) and not d.startswith("_")]

        total_images = 0
        new_clip_folder_data = []
        for folder_path in clip_folders:
            folder_name = os.path.basename(folder_path)
            folder_dirname = os.path.dirname(folder_path)
            cached_folder_name = folder_name + "_cached.pkl"
            cached_folder_path = os.path.join(
                folder_dirname, cached_folder_name)

            # Count total images for progress bar
            if os.path.exists(cached_folder_path) and not overwrite_cache:
                # If cache exists, load image count from cache
                with open(cached_folder_path, 'rb') as cache_file:
                    cached_data = pickle.load(cache_file)
                    total_images += len(cached_data)
            else:
                # If no cache, count the number of image files
                image_files = [f for f in os.listdir(
                    folder_path) if f.endswith('.jpg') or f.endswith('.png')]
                total_images += len(image_files)

            new_clip_folder_data.append(
                (folder_path, folder_name, cached_folder_path, cached_folder_name))

        clip_folders = new_clip_folder_data

        # Create progress bar with total number of images
        progressbar = ProgressBar(
            total_images, f"Folder: [0/{len(clip_folders)}] Frame: [0/0]")

        for i, (folder_path, folder_name, cached_folder_path, cached_folder_name) in enumerate(clip_folders):
            if os.path.exists(cached_folder_path) and not overwrite_cache:
                # Load from cache
                with open(cached_folder_path, 'rb') as cache_file:
                    cached_data = pickle.load(cache_file)

                    # Move all cached tensors to the correct device
                    for j in range(len(cached_data)):
                        cached_data[j] = [(tensor_emb.to(self.autovae.device), image_path)
                                          for tensor_emb, image_path in cached_data[j]]
                        progressbar.update(1)

                    # Extend the dataset with the cached training examples
                    self.data.extend(cached_data)
            else:
                # Process new images and create training examples
                image_files = [f for f in os.listdir(
                    folder_path) if f.endswith('.jpg') or f.endswith('.png')]
                image_files = sorted(image_files, key=lambda x: int(
                    ''.join(filter(str.isdigit, os.path.splitext(x)[0]))))

                processed_images = []

                for j, image_file in enumerate(image_files):
                    image_path = os.path.join(folder_path, image_file)
                    pillow_image = load_image(image_path)
                    thumbnail_image = thumbnail_fill(
                        convert_image_format(pillow_image, "RGB"), size=(512, 512))
                    tensor_image = from_pil_image(
                        thumbnail_image)
                    tensor_emb = self.autovae.encode(tensor_image)
                    processed_images.append((tensor_emb, image_path))

                    progressbar.set_description(
                        f"Folder: [{i + 1}/{len(clip_folders)}] Frame: [{j + 1}/{len(image_files)}]")
                    progressbar.update(1)

                # Create training examples with a sliding window of 16, offset by 1
                training_examples = []
                for start_idx in range(len(processed_images) - self.chunk_size):
                    chunk = processed_images[start_idx:start_idx +
                                             self.chunk_size]

                    if len(chunk) < self.chunk_size * 0.5:
                        continue

                    training_examples.append(chunk)

                # Save training examples to cache
                with open(cached_folder_path, 'wb') as cache_file:
                    pickle.dump(training_examples, cache_file)

                # Add the training examples to the dataset
                self.data.extend(training_examples)

        progressbar.close()

    def delete_images_from_folder(self, folder_path: str):
        """
        Deletes all .png and .jpg images from the specified folder.

        :param folder_path: The path to the folder from which images should be deleted
        """
        # Supported image extensions
        extensions = ('.png', '.jpg', '.jpeg')

        # Iterate through files in the folder
        for filename in os.listdir(folder_path):
            # Check if the file has a valid image extension
            if filename.lower().endswith(extensions):
                file_path = os.path.join(folder_path, filename)
                try:
                    os.remove(file_path)  # Delete the file
                    # print(f"Deleted: {file_path}")
                except Exception as e:
                    pass
                    # print(f"Failed to delete {file_path}. Reason: {e}")

    def _create_frames_from_videos(self, folder_path: str, frame_frequency: int = 5, overwrite_frames: bool = False):
        """
        Collects video file paths from subfolders in the given folder path and processes them.
        First loop collects valid MP4 paths. Second loop processes them by extracting every 5th frame
        and saving the frames as PNGs in the same subfolder. A 'processed.txt' file is created in the folder.

        :param folder_path: Path to the main folder containing subfolders with an MP4 file.
        """
        video_paths = []

        total_frames = 0  # Initialize a variable to keep track of total frames

        # First loop: Collect paths of videos to process
        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)

            # Skip if not a directory or if folder starts with an underscore
            if not os.path.isdir(subfolder_path) or subfolder.startswith('_'):
                continue

            if overwrite_frames == False:
                # Check if 'processed.txt' already exists to skip processed folders
                if os.path.exists(os.path.join(subfolder_path, 'processed.txt')):
                    # print(f"Skipping {subfolder} as it is already processed.")
                    continue
            else:
                self.delete_images_from_folder(subfolder_path)

            # Find the MP4 file in the subfolder
            mp4_files = [f for f in os.listdir(
                subfolder_path) if f.endswith('.mp4')]
            if not mp4_files:
                # print(f"No MP4 file found in {subfolder}. Skipping.")
                continue

            # Assuming there's only one MP4 file per folder
            video_path = os.path.join(subfolder_path, mp4_files[0])
            video_paths.append(video_path)

            # Open the video file to get frame count
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                # print(f"Could not open video {video_path}. Skipping.")
                continue

            # Get the frame count for this video and add it to the total
            video_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            total_frames += video_frame_count

            # Release the video capture object after use
            cap.release()

        progressbar = ProgressBar(total_frames, "Video: [0/0] Frame: [0/0]")

        # Second loop: Process the collected video paths
        for i, video_path in enumerate(video_paths):
            # Get the subfolder path from video path
            subfolder_path = os.path.dirname(video_path)

            # Open the video file using cv2
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                # print(f"Could not open video {video_path}. Skipping.")
                continue

            total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            frame_count = -1
            saved_frame_count = 0

            # Process the video frame by frame
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # Only save every 5th frame
                if frame_count % frame_frequency == 0:
                    # Convert the frame to a PIL image for saving
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)

                    thumbnail_image = thumbnail_fill(
                        convert_image_format(img, "RGB"), size=(512, 512))

                    # Save the frame in the same subfolder with the name 'frame_0001.png', etc.
                    frame_filename = os.path.join(subfolder_path, f'frame_{
                        saved_frame_count:04d}.png')
                    thumbnail_image.save(frame_filename)
                    saved_frame_count += 1

                progressbar.set_description(
                    f"Video: [{i+1}/{len(video_paths)}] Frame: [{frame_count + 1}/{total_frame_count}]")

                progressbar.update(1)

            # Release the video capture object
            cap.release()

            # Create the 'processed.txt' file to mark the folder as processed
            with open(os.path.join(subfolder_path, 'processed.txt'), 'w') as f:
                f.write("This folder has been processed.")

        progressbar.set_description(
            f"Finished! Videos: [{len(video_paths)}] Frames: [{total_frames}]")
        progressbar.set_progress(total_frames)

        progressbar.close()

    def example_to_pair(self, example) -> tuple[torch.Tensor, torch.Tensor]:
        tensors = [item[0] for item in example]
        inputs = tensors[:-1]
        output = tensors[-1]
        inputs = torch.cat(inputs, dim=0)
        return inputs.unsqueeze(0), output


class NextFrameGenerator(nn.Module):
    def __init__(self, hidden_dim: int = 16, sequence_len: int = 15, device="cuda"):
        super(NextFrameGenerator, self).__init__()
        self.device = device

        # Hardcoded parameters
        self.in_channels = 4
        self.sequence_len = sequence_len
        self.hidden_channels = hidden_dim
        self.kernel_size = (3, 3, 3)
        self.stride = 1
        self.padding = 1

        # First 3D convolution to process sequence and spatial dimensions
        self.conv3d_1 = nn.Conv3d(in_channels=self.in_channels,
                                  out_channels=self.hidden_channels,
                                  kernel_size=self.kernel_size,
                                  stride=self.stride,
                                  padding=self.padding)

        # Second 3D convolution layer
        self.conv3d_2 = nn.Conv3d(in_channels=self.hidden_channels,
                                  out_channels=self.hidden_channels * 2,
                                  kernel_size=self.kernel_size,
                                  stride=self.stride,
                                  padding=self.padding)

        # Third 3D convolution layer to collapse temporal dimension
        self.conv3d_3 = nn.Conv3d(in_channels=self.hidden_channels * 2,
                                  out_channels=self.in_channels,
                                  # Reduce depth to 1
                                  kernel_size=(self.sequence_len, 3, 3),
                                  stride=1,
                                  # No temporal padding, only spatial padding
                                  padding=(0, 1, 1))

        # Activation and normalization layers
        self.relu = nn.ReLU()
        self.batch_norm = nn.BatchNorm3d(self.hidden_channels)

        self.to(device)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for predicting the next embedding

        :param x: Input tensor of shape [batch_size, sequence_len, in_channels, height, width]
        :returns: Predicted next embedding of shape [batch_size, in_channels, height, width]
        """
        # Reorder to [batch_size, in_channels, sequence_len, height, width]

        x = x.permute(0, 2, 1, 3, 4)

        # Pass through 3D convolution layers
        x = self.relu(self.batch_norm(self.conv3d_1(x)))
        x = self.relu(self.conv3d_2(x))
        x = self.conv3d_3(x)  # Final layer to collapse sequence dimension to 1

        # Output shape will be [batch_size, in_channels, 1, height, width]
        # Squeeze the sequence dimension to output shape [batch_size, in_channels, height, width]
        return x.squeeze(2)

    def next(self, data):
        inputs = torch.cat(data, dim=0).unsqueeze(0)
        output = self(inputs)

        new_data = data[:-1] + [output]

        return output, new_data

    def train_model(self, dataset: NextFrameGeneratorDataset, iterations: int = 10, learning_rate: float = 0.001):
        """
        Train the model using the provided dataset.

        :param dataset: Dataset of sequences and expected next-frame embeddings
        :param iterations: Number of training epochs
        :param learning_rate: Learning rate for optimizer
        """
        self.train()  # Set model to training mode
        optimizer = Adam(self.parameters(), lr=learning_rate)
        criterion = nn.MSELoss()

        # Progress bar using the previously defined ProgressBar class
        progressbar = ProgressBar(
            iterations * len(dataset),
            f"Epoch: [0/{iterations}] Step: [0/{len(dataset)}] Loss: [0]"
        )

        for epoch in range(iterations):
            total_loss = 0.0
            loss_count = 0

            for dataset_iter, inputs in enumerate(dataset):
                if len(inputs) < 16:
                    progressbar.update(1)
                    continue

                # Reset gradients
                optimizer.zero_grad()

                input_tensor, expected_output = dataset.example_to_pair(inputs)

                # Initial hidden state set to None to let GRU handle it
                actual_output = self(input_tensor)

                # Calculate loss
                loss = criterion(actual_output, expected_output)
                total_loss += loss.item()
                loss_count += 1

                # Backpropagation and optimization
                loss.backward()
                optimizer.step()

                # Update progress bar
                progressbar.update(1)
                progressbar.set_description(
                    f"Epoch: [{(epoch+1):0{len(str(abs(iterations)))}d}/{iterations}] Step: [{(dataset_iter +
                                                                                               1):0{len(str(abs(len(dataset))))}d}/{len(dataset)}] Loss: [{total_loss / loss_count:.4f}]"
                )

        progressbar.close()
        self.eval()

    def save_model(self, folder_path: str, full_model: bool = False):
        """
        Save the model's state_dict or the full model to a .pth file in the given folder.

        :param folder_path: Path to the folder where model.pth will be saved
        :param full_model: Boolean flag to indicate whether to save the full model (default: False)
        """
        # Ensure the folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Define the full path for the model file
        model_path = os.path.join(folder_path, 'model.pth')

        # Save current device (cuda or cpu) to move the model back later
        current_device = next(self.parameters()).device

        # Move model to CPU before saving
        self.cpu()

        # Save either the state_dict or the full model based on the flag
        if full_model:
            # Save the entire model object
            torch.save(self, model_path)
        else:
            # Save the state dictionary (recommended)
            torch.save(self.state_dict(), model_path)

        print(f"Model saved at {model_path}")

        # Move the model back to the original device
        self.to(current_device)

    def load_model(self, folder_path: str, full_model: bool = False):
        """
        Load the model's state_dict or the full model from a .pth file in the given folder.

        :param folder_path: Path to the folder where model.pth is located
        :param full_model: Boolean flag to indicate whether to load the full model (default: False)
        """
        # Define the full path for the model file
        model_path = os.path.join(folder_path, 'model.pth')

        # Check if the model file exists
        if os.path.exists(model_path):
            if full_model:
                # Load the entire model object
                loaded_model = torch.load(model_path, map_location=self.device)
                self.load_state_dict(loaded_model.state_dict())
            else:
                # Load only the state dictionary
                self.load_state_dict(torch.load(
                    model_path, map_location=self.device))

            self.to(self.device)  # Move the model to the correct device
            print(f"Model loaded from {model_path}")
        else:
            raise FileNotFoundError(f"No model file found at {model_path}")
