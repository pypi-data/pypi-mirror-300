"""Utilities provided by pictoken"""

from __future__ import annotations

import base64
import io
from math import ceil

from PIL import Image

from .const import (
    BASE_IMAGE_TOKENS_GPT_4O,
    BASE_IMAGE_TOKENS_GPT_4O_MINI,
    TILE_SIZE_GPT_4O,
    TILE_SIZE_GPT_4O_MINI,
    TOKENS_PER_TILE_GPT_4O,
    TOKENS_PER_TILE_GPT_4O_MINI,
)
from .enums import ImageDetail, Model
from .models import ResizedImage, Response


def calculate_image_tokens_by_image(
    image: str | bytes, model: Model, detail: ImageDetail = ImageDetail.AUTO
) -> Response:
    """Calculate the number of image tokens by base64 image, image url or image"""

    if not isinstance(image, str) and not isinstance(image, bytes):
        raise TypeError("Image must be a string or bytes")

    if not isinstance(model, Model):
        raise ValueError("Unsupported model type")

    # Handle streaming files
    if isinstance(image, bytes):
        pil_image = Image.open(io.BytesIO(image))
        width, height = pil_image.size

        return calculate_image_tokens_by_image_dimensions(width, height, model, detail)

    if isinstance(image, str):
        # Handle image urls
        if image.startswith("https"):
            # Download image
            raise NotImplementedError("This function is not implemented yet")

        # Handle base64 encoded images (data url)
        elif image.startswith("data:image/"):
            # Decode base64 image and remove data_url prefix
            image_as_base64 = base64.b64decode(image.split(",")[1])
            pil_image = Image.open(io.BytesIO(image_as_base64))
            width, height = pil_image.size

            return calculate_image_tokens_by_image_dimensions(
                width, height, model, detail
            )

    raise NotImplementedError("This function is not implemented yet")


def calculate_image_tokens_by_image_dimensions(
    width: int, height: int, model: Model, detail: ImageDetail = ImageDetail.AUTO
) -> Response:
    """Calculate the number of image tokens"""

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers")

    if not isinstance(model, Model):
        raise ValueError("Unsupported model type")

    if model in [
        Model.GPT_4O,
        Model.GPT_4O_2024_05_13,
        Model.GPT_4O_2024_08_06,
        Model.CHATGPT_4O_LATEST,
    ]:
        return _openai_calculate_image_tokens_by_image_dimensions(
            width=width,
            height=height,
            detail=detail,
            base_image_tokens=BASE_IMAGE_TOKENS_GPT_4O,
            tile_size=TILE_SIZE_GPT_4O,
            tokens_per_tile=TOKENS_PER_TILE_GPT_4O,
        )
    elif model in [Model.GPT_4O_MINI, Model.GPT_4O_MINI_2024_07_18]:
        return _openai_calculate_image_tokens_by_image_dimensions(
            width=width,
            height=height,
            detail=detail,
            base_image_tokens=BASE_IMAGE_TOKENS_GPT_4O_MINI,
            tile_size=TILE_SIZE_GPT_4O_MINI,
            tokens_per_tile=TOKENS_PER_TILE_GPT_4O_MINI,
        )

    raise Exception("Unsupported model")


def _openai_calculate_image_tokens_by_image_dimensions(
    width: int,
    height: int,
    detail: ImageDetail,
    base_image_tokens: int,
    tile_size: int,
    tokens_per_tile: int,
) -> Response:
    """
    Calculate the number of tokens required for OpenAI models for an image based on its resolution.

    The token cost of a given image is determined by two factors: its size, and the detail option on each image_url block. All images with detail: low cost 85 tokens each.
    detail: high images are first scaled to fit within a 2048 x 2048 square, maintaining their aspect ratio. Then, they are scaled such that the shortest side of the image is 768px long.
    Finally, we count how many 512px squares the image consists of. Each of those squares costs 170 tokens. Another 85 tokens are always added to the final total.
    """
    if detail == ImageDetail.LOW:
        return Response(
            total_tokens=base_image_tokens,
            base_tokens=base_image_tokens,
            tile_tokens=0,
            total_tiles=0,
            width_tiles=0,
            height_tiles=0,
        )

    original_width = width
    original_height = height
    resized = None

    # Scale to fit within a 2048 x 2048 square
    if width > 2048 or height > 2048:
        aspect_ratio = width / height

        # Maintain aspect ratio while scaling to fit within 2048 x 2048
        if aspect_ratio > 1:
            width = 2048
            height = round(2048 / aspect_ratio)
        else:
            width = round(2048 * aspect_ratio)
            height = 2048

    # Scale such that the shortest side of the image is 768px long
    # Don't scale the image if one side is already smaller than 768px
    if height > 768 and width >= height:
        width = round((768 / height) * width)
        height = 768
    elif width > 768 and height > width:
        width = 768
        height = round((768 / width) * height)

    # Add a resized image if the image was scaled
    if width != original_width or height != original_height:
        resized = ResizedImage(width=width, height=height)

    # Calculate the number of 512px squares
    width_tiles = ceil(width / tile_size)
    height_tiles = ceil(height / tile_size)

    num_tiles = ceil(width / tile_size) * ceil(height / tile_size)
    tile_tokens = tokens_per_tile * num_tiles

    return Response(
        total_tokens=tile_tokens + base_image_tokens,
        base_tokens=base_image_tokens,
        tile_tokens=tile_tokens,
        total_tiles=num_tiles,
        width_tiles=width_tiles,
        height_tiles=height_tiles,
        resized=resized,
    )
