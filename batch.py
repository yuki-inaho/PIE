# coding=utf-8


import cv2
import shutil
import argparse
import numpy as np
from tqdm import tqdm
from pathlib import Path
from typing import List
import pie


SCRIPT_DIR = str(Path().parent)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--input-dir", "-i", type=str, default=f"{SCRIPT_DIR}/images")
    parser.add_argument("--output-dir", "-o", type=str, default=f"{SCRIPT_DIR}/output")
    return parser.parse_args()


def get_image_pathes(input_data_dir: str) -> List[str]:
    exts = [".jpg", ".png"]
    image_pathes = sorted([path for path in Path(input_data_dir).glob("*") if path.suffix.lower() in exts])
    image_path_list = [str(image_path) for image_path in image_pathes]
    return image_path_list


def main(image_path: str) -> np.ndarray:
    print(image_path)
    rim = cv2.imread(image_path)
    out = pie.PIE(rim)
    return out


if __name__ == "__main__":
    args = parse_args()
    image_path_list = get_image_pathes(args.input_dir)
    output_dir_pathlib = Path(args.output_dir)
    if output_dir_pathlib.exists():
        shutil.rmtree(str(output_dir_pathlib))
    output_dir_pathlib.mkdir()

    for image_path in tqdm(image_path_list):
        out = main(image_path)
        image_name = Path(image_path).name
        cv2.imwrite(str(output_dir_pathlib.joinpath(image_name)), out)
        cv2.waitKey(10)