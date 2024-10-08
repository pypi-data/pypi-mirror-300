import torch
from typing import Union
from typing import Generator, Union
from PIL import Image
import numpy as np
import os


def load_image(file_path: str) -> Image.Image:
    """
    Loads an image from the specified file path using Pillow.

    :param file_path: The path to the image file to be loaded.
    :returns: The loaded image as a PIL Image object.
    """
    image = Image.open(file_path)
    image.load()  # Ensure the image is fully loaded
    return image


def load_images(folder_path: str) -> Generator[Image.Image, None, None]:
    """
    Generator function that yields loaded PIL Image objects from all image files in a given folder.

    :param folder_path: The path to the folder containing image files.
    :yields: Loaded PIL Image objects.
    """
    for image_file in get_image_files(folder_path):
        yield load_image(image_file)


def save_image(image: Image.Image, file_path: str, format: str = None) -> None:
    """
    Saves a given image to the specified file path using Pillow.

    :param image: The PIL Image object to be saved.
    :param file_path: The path where the image will be saved.
    :param format: Optional. The format to use for saving (e.g., 'JPEG', 'PNG'). 
                   If None, the format is inferred from the file extension.
    :returns: None
    """
    image.save(file_path, format=format)


def _load_or_return_image(image: Union[Image.Image, str]) -> Image.Image:
    """
    Loads an image if a file path is provided, otherwise returns the image.

    :param image: Either a PIL Image object or a file path to an image.
    :returns: A PIL Image object.
    """
    if isinstance(image, str):
        return load_image(image)
    return image


def crop_image(image: Union[Image.Image, str], size: tuple[int, int]) -> Image.Image:
    """
    Crops an image from the center to the specified size. 
    If the specified size is larger than the image, the extra area is filled with 
    background pixels matching the original image mode (transparent black for RGBA, black for RGB or grayscale).

    :param image: Either a PIL Image object or a file path to an image.
    :param size: A tuple (width, height) specifying the size of the crop.
    :returns: A new PIL Image object that is the cropped version of the original image.
    """
    image = _load_or_return_image(image)
    original_mode = image.mode  # Save the original mode of the image

    target_width, target_height = size
    original_width, original_height = image.size

    # Calculate the center crop box
    left = max((original_width - target_width) // 2, 0)
    top = max((original_height - target_height) // 2, 0)
    right = min(left + target_width, original_width)
    bottom = min(top + target_height, original_height)

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    # If the crop size is larger than the original image, create a new image with the original mode
    if target_width > original_width or target_height > original_height:
        # Create a new image with the original mode and size
        if original_mode in ("RGBA", "LA"):
            # Transparent for RGBA or LA
            new_image = Image.new(original_mode, size, (0, 0, 0, 0))
        elif original_mode == "RGB":
            # Black background for RGB
            new_image = Image.new(original_mode, size, (0, 0, 0))
        else:
            # Black for grayscale or other modes
            new_image = Image.new(original_mode, size, 0)

        # Calculate the position to paste the cropped image onto the new image
        paste_x = (target_width - cropped_image.width) // 2
        paste_y = (target_height - cropped_image.height) // 2

        # Paste the cropped image onto the background
        new_image.paste(cropped_image, (paste_x, paste_y))
        return new_image

    # If no padding is needed, just return the cropped image
    return cropped_image


def resize_image(image: Union[Image.Image, str], size: tuple[int, int], keep_aspect_ratio: bool = False) -> Image.Image:
    """
    Resizes an image to the specified size. If keep_aspect_ratio is True, the image
    will be resized while maintaining its aspect ratio, and any extra space will be filled
    with the background color (transparent pixels if RGBA, black if RGB or grayscale).

    :param image: Either a PIL Image object or a file path to an image.
    :param size: A tuple (width, height) specifying the target size.
    :param keep_aspect_ratio: Boolean to decide whether to maintain the original aspect ratio. Default is False.
    :returns: A new PIL Image object that is the resized version of the original image.
    """
    image = _load_or_return_image(image)
    original_mode = image.mode  # Save the original mode of the image

    if keep_aspect_ratio:
        original_width, original_height = image.size
        target_width, target_height = size

        # Calculate the new size while keeping the aspect ratio
        aspect_ratio = original_width / original_height
        if target_width / target_height > aspect_ratio:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)

        # Resize the image with the new dimensions
        resized_image = image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)

        # Create a new image with the original mode and the target size
        if original_mode in ("RGBA", "LA"):
            # Transparent for RGBA or LA
            new_image = Image.new(original_mode, size, (0, 0, 0, 0))
        elif original_mode == "RGB":
            # Black background for RGB
            new_image = Image.new(original_mode, size, (0, 0, 0))
        else:
            # Black for grayscale or other modes
            new_image = Image.new(original_mode, size, 0)

        # Paste the resized image onto the new image
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        new_image.paste(resized_image, (paste_x, paste_y))

        return new_image
    else:
        # Resize directly to the target size without keeping aspect ratio
        return image.resize(size, Image.Resampling.LANCZOS)


def thumbnail(image: Union[Image.Image, str], size: tuple[int, int]) -> Image.Image:
    """
    Creates a thumbnail of the specified size by first resizing the image while
    maintaining the aspect ratio, then cropping it to fit the exact size.

    :param image: Either a PIL Image object or a file path to an image.
    :param size: A tuple (width, height) specifying the size of the thumbnail.
    :returns: A new PIL Image object that is the thumbnail version of the original image.
    """
    image = _load_or_return_image(image)

    # Step 1: Resize the image while maintaining aspect ratio
    resized_image = resize_image(image, size, keep_aspect_ratio=True)

    # Step 2: Crop the resized image to the exact size
    cropped_thumbnail = crop_image(resized_image, size)

    return cropped_thumbnail


def thumbnail_fill(image: Union[Image.Image, str], size: tuple[int, int]) -> Image.Image:
    """
    Resizes the image to ensure it fills the target dimensions by making the smaller
    dimension match the target size, while maintaining aspect ratio, and then crops
    any excess from the larger dimension to fit the target size.

    :param image: Either a PIL Image object or a file path to an image.
    :param size: A tuple (width, height) specifying the target size.
    :returns: A new PIL Image object that fills and crops to the specified size.
    """
    image = _load_or_return_image(image)

    # Step 1: Get original dimensions
    original_width, original_height = image.size
    target_width, target_height = size

    # Step 2: Calculate aspect ratio of the image and target
    original_aspect = original_width / original_height
    target_aspect = target_width / target_height

    # Step 3: Resize while maintaining aspect ratio so that the image fills the space
    if original_aspect > target_aspect:
        # Image is wider than target (crop sides)
        new_height = target_height
        new_width = int(new_height * original_aspect)
    else:
        # Image is taller or same aspect ratio as target (crop top/bottom)
        new_width = target_width
        new_height = int(new_width / original_aspect)

    # Resize the image to fill the target area
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Step 4: Crop the image to the exact size
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2

    cropped_image = resized_image.crop((left, top, right, bottom))

    return cropped_image


def get_image_files(folder_path: str) -> Generator[str, None, None]:
    """
    Generator function that yields file paths to images in a given folder.

    :param folder_path: The path to the folder to search for image files.
    :yields: The full path to each image file found in the folder.
    """
    # Define valid image extensions
    valid_extensions = {".jpg", ".jpeg", ".png",
                        ".gif", ".bmp", ".tiff", ".webp"}

    # Iterate over all files in the directory
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is an image by its extension
        if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() in valid_extensions:
            yield file_path


def flip_image(image: Union[Image.Image, str], direction: str) -> Image.Image:
    """
    Flips an image vertically or horizontally.

    :param image: Either a PIL Image object or a file path to an image.
    :param direction: 'v' for vertical flip, 'h' for horizontal flip.
    :returns: A new PIL Image object that is the flipped version of the original image.
    :raises ValueError: If the direction is not 'v' or 'h'.
    """
    # Load the image if a path is provided
    image = _load_or_return_image(image)

    direction = direction.lower()

    if direction == 'v':
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif direction == 'h':
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    else:
        raise ValueError(
            "Invalid direction: must be 'v' for vertical or 'h' for horizontal")


def rotate_image(image: Union[Image.Image, str], angle: float, expand: bool = False) -> Image.Image:
    """
    Rotates an image by a specified angle.

    :param image: Either a PIL Image object or a file path to an image.
    :param angle: The angle in degrees to rotate the image. Positive values rotate counterclockwise, negative values rotate clockwise.
    :param expand: Optional. If True, expands the output image to hold the entire rotated image. Default is False.
    :returns: A new PIL Image object that is the rotated version of the original image.
    """
    # Load the image if a path is provided
    image = _load_or_return_image(image)

    # Rotate the image
    rotated_image = image.rotate(angle, expand=expand)

    return rotated_image


def color_range_mask(
    image: Union[Image.Image, str],
    target_color: tuple[int, int, int],
    min_threshold: float = 0.0,
    max_threshold: float = 0.1,
    gradient: bool = False
) -> Image.Image:
    """
    Creates a mask based on the distance between each pixel color and the target color.

    :param image: Either a PIL Image object or a file path to an image.
    :param target_color: A tuple (R, G, B) representing the target color.
    :param min_threshold: Minimum threshold for the distance. Pixels with a distance lower than this will be white.
    :param max_threshold: Maximum threshold for the distance. Pixels with a distance higher than this will be black.
    :param gradient: If True, the mask will map distances between min_threshold and max_threshold to a gradient from white to black. 
                     If False, the mask will be binary (black and white).
    :returns: A new PIL Image object representing the mask.
    """
    # Load the image if a path is provided
    image = _load_or_return_image(image)

    # Convert image to RGB if not already in RGB mode
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Get the pixel data
    np_image = np.array(image)

    # Calculate the Euclidean distance between each pixel and the target color
    distances = np.sqrt(
        np.sum((np_image - np.array(target_color))**2, axis=-1)) / np.sqrt(3 * 255**2)

    # Create the mask
    if gradient:
        # Map distances within the threshold range to a 0-255 gradient
        normalized_distances = np.clip(
            (distances - min_threshold) / (max_threshold - min_threshold), 0, 1)
        mask = (normalized_distances * 255).astype(np.uint8)
    else:
        # Apply binary thresholding
        mask = np.where((distances >= min_threshold) & (
            distances <= max_threshold), 255, 0).astype(np.uint8)

    # Convert the mask to a PIL Image
    mask_image = Image.fromarray(mask, mode="L")

    return mask_image


def convert_image_format(image: Union[Image.Image, str], mode: str = "RGB") -> Image.Image:
    """
    Converts a PIL image to the specified mode (e.g., 'RGB', 'RGBA', 'L' for grayscale).

    :param image: Either a PIL Image object or a file path to an image.
    :param mode: The desired mode ('RGB', 'RGBA', 'L', etc.).
    :returns: A new PIL Image object in the specified mode.
    :raises ValueError: If the mode is not recognized.
    """
    # Load the image if a path is provided
    image = _load_or_return_image(image)

    # Validate the mode
    valid_modes = {'RGB', 'RGBA', 'L'}
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {
                         mode}. Supported modes are: {valid_modes}")

    # Convert the image to the desired mode
    if image.mode != mode:
        image = image.convert(mode)

    return image


def to_pil_image(tensor_image: torch.Tensor) -> list[Image.Image]:
    """
    Converts a tensor image or batch of tensor images to a PIL image or a list of PIL images.

    :param tensor_image: Tensor of shape (batch_size, 3, height, width) or (3, height, width)
    :returns: A PIL image or a list of PIL images
    """
    # Handle batched input
    if tensor_image.dim() == 4:
        images = []
        for img in tensor_image:
            img = img.squeeze(0).permute(1, 2, 0).detach().cpu().numpy()
            img = (img - img.min()) / (img.max() - img.min())
            img = (img * 255).astype(np.uint8)
            images.append(Image.fromarray(img))
        return images
    elif tensor_image.dim() == 3:
        img = tensor_image.permute(1, 2, 0).detach().cpu().numpy()
        img = (img - img.min()) / (img.max() - img.min())
        img = (img * 255).astype(np.uint8)
        return [Image.fromarray(img)]
    else:
        raise ValueError(
            "Unsupported tensor dimension. Expected 3 or 4 dimensions.")


def from_pil_image(pil_image: Union[Image.Image, list[Image.Image]]) -> torch.Tensor:
    """
    Converts a PIL image or a list of PIL images into a batched tensor.

    :param pil_image: A single PIL Image or a list of PIL Images
    :returns: A tensor of shape (batch_size, 3, height, width)
    """
    if isinstance(pil_image, list):
        tensors = []
        for img in pil_image:
            img_tensor = torch.from_numpy(
                np.array(img).astype(np.float32) / 255.0)
            # Change shape to (3, height, width)
            img_tensor = img_tensor.permute(2, 0, 1)
            tensors.append(img_tensor)
        batched_tensor = torch.stack(tensors)  # Combine into a batch
    else:
        img_tensor = torch.from_numpy(
            np.array(pil_image).astype(np.float32) / 255.0)
        # Change shape to (3, height, width)
        img_tensor = img_tensor.permute(2, 0, 1)
        batched_tensor = img_tensor.unsqueeze(0)  # Add a batch dimension

    return batched_tensor
