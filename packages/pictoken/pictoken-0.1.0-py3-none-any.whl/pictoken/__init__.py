# This is the public API of tiktoken

from .enums import ImageDetail as ImageDetail
from .enums import Model as Model
from .utils import calculate_image_tokens_by_image as calculate_image_tokens_by_image
from .utils import (
    calculate_image_tokens_by_image_dimensions as calculate_image_tokens_by_image_dimensions,
)
