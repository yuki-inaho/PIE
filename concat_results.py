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
    parser.add_argument("--raw-input-dir", "-r", type=str, default=f"{SCRIPT_DIR}/images")
    parser.add_argument("--processed-input-dir", "-p", type=str, default=f"{SCRIPT_DIR}/output")
    parser.add_argument("--output-dir", "-o", type=str, default=f"{SCRIPT_DIR}/concat")
    return parser.parse_args()


def get_image_pathes(input_data_dir: str) -> List[str]:
    exts = [".jpg", ".png"]
    image_pathes = sorted([path for path in Path(input_data_dir).glob("*") if path.suffix.lower() in exts])
    image_path_list = [str(image_path) for image_path in image_pathes]
    return image_path_list


if __name__ == "__main__":
    args = parse_args()
    raw_image_path_list = get_image_pathes(args.raw_input_dir)
    processed_image_path_list = get_image_pathes(args.processed_input_dir)

    output_dir_pathlib = Path(args.output_dir)
    if output_dir_pathlib.exists():
        shutil.rmtree(str(output_dir_pathlib))
    output_dir_pathlib.mkdir()

    for raw_image_path, processed_image_path in zip(tqdm(raw_image_path_list), processed_image_path_list):
        image_raw = cv2.imread(raw_image_path)
        image_processed = cv2.imread(processed_image_path)
        out = cv2.hconcat([image_raw, image_processed])
        image_name = Path(raw_image_path).name
        cv2.imwrite(str(output_dir_pathlib.joinpath(image_name)), out)
        cv2.waitKey(10)