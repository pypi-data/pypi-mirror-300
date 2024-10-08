from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResizedImage:
    width: int
    height: int


@dataclass
class Response:
    total_tokens: int
    base_tokens: int
    tile_tokens: int
    total_tiles: int
    width_tiles: int
    height_tiles: int

    resized: ResizedImage | None = None
