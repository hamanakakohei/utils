#!/usr/bin/env python3

import sys
from PIL import Image
from pathlib import Path
from typing import Sequence, Union
import os


def get_api_key(cli_key: str | None) -> str:
    if cli_key:
        return cli_key
    env_key = os.getenv("ALPHAGENOME_API_KEY")
    if env_key:
        return env_key
    sys.exit("Error: APIキーを、--api_keyで与えるか、ALPHAGENOME_API_KEY環境変数に入れて。")


def merge_images_and_save(
    image_files: Sequence[Union[str, Path]],
    output_path: Union[str, Path],
    cols: int
) -> None:
    """
    複数の画像を指定列数でタイル状に結合し、保存する。
    
    Args:
        image_files: 画像ファイルのパスのリスト
        cols: 横に並べる列数
    """
    image_paths = [Path(p) for p in image_files]
    images = [Image.open(p) for p in image_paths]

    # 最初の画像サイズを基準とする
    img_width, img_height = images[0].size
    resized_images = [img.resize((img_width, img_height)) for img in images]

    # 必要な行数（切り上げ）
    rows = -(-len(resized_images) // cols)  # ceil(len / cols)

    # 新しいキャンバスの作成
    merged_image = Image.new("RGB", (cols * img_width, rows * img_height))
    for idx, img in enumerate(resized_images):
        x = (idx % cols) * img_width
        y = (idx // cols) * img_height
        merged_image.paste(img, (x, y))

    # 保存
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    merged_image.save(Path(output_path))
