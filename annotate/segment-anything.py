# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import cv2  # type: ignore

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry, SamPredictor

import numpy as np
import argparse
import json
import os
from typing import Any, Dict, List
from readXML import collectBoxes
import torch

parser = argparse.ArgumentParser(
    description=(
        "Runs automatic mask generation on an input image or directory of images, "
        "and outputs masks as either PNGs or COCO-style RLEs. Requires open-cv, "
        "as well as pycocotools if saving in RLE format."
    )
)

parser.add_argument(
    "--input",
    type=str,
    required=True,
    help="Path to either a single input image or folder of images.",
)
parser.add_argument(
    "--label",
    type=str,
    help=(
        "Path to the directory where labels are put. "
    ),
)
parser.add_argument(
    "--output",
    type=str,
    required=True,
    help=(
        "Path to the directory where masks will be output. Output will be either a folder "
        "of PNGs per image or a single json with COCO-style masks."
    ),
)

def write_cattle_to_folder(masks, boxes, path: str, image) -> None:
    for i, mask in enumerate(masks):
        filename = f"{i}.png"
        mask = np.array(mask[0].tolist())
        mask = mask[:, :, np.newaxis]
        img = image * mask
        [x, y, x1, y1] = boxes[i]

        img = img[y: y1, x: x1, :]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(path, filename), img)
    return


def write_masks_to_folder(masks: List[Dict[str, Any]], path: str, image) -> None:
    #bbox (list(float)): The box around the mask, in XYWH format
    header = "id,area,bbox_x0,bbox_y0,bbox_w,bbox_h,point_input_x,point_input_y,predicted_iou,stability_score,crop_box_x0,crop_box_y0,crop_box_w,crop_box_h"  # noqa
    metadata = [header]
    for i, mask_data in enumerate(masks):
        mask = mask_data["segmentation"]
        filename = f"{i}.png"
        mask = mask[:, :, np.newaxis]
        img = image * mask
        x, y, w, h = mask_data["bbox"]

        img = img[y: (y + h), x: (x + w), :]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        print(f'cropped img {img.shape}')
        cv2.imwrite(os.path.join(path, filename), img)

        mask_metadata = [
            str(i),
            str(mask_data["area"]),
            *[str(x) for x in mask_data["bbox"]],
            *[str(x) for x in mask_data["point_coords"][0]],
            str(mask_data["predicted_iou"]),
            str(mask_data["stability_score"]),
            *[str(x) for x in mask_data["crop_box"]],
        ]
        row = ",".join(mask_metadata)
        metadata.append(row)
    metadata_path = os.path.join(path, "metadata.csv")
    with open(metadata_path, "w") as f:
        f.write("\n".join(metadata))

    return


def main(args: argparse.Namespace) -> None:
    print("Loading model...")

    sam_checkpoint = "sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    _ = sam.to(device="cuda")

    output_mode = "binary_mask"

    output = args.output
    #output = '/content/image15'
    #input = '/content/DJI_20230109105426_0030_Zenmuse-L1-mission.JPG'
    input = args.input
    label = args.label

    if not os.path.isdir(input):
        targets = [input]
    else:
        targets = [
            f for f in os.listdir(input) if not os.path.isdir(os.path.join(input, f))
        ]
        targets = [os.path.join(input, f) for f in targets]

    os.makedirs(output, exist_ok=True)

    if label:
      main_prompt(targets, output, label, sam)
      return

    generator = SamAutomaticMaskGenerator(sam, output_mode=output_mode)

    for t in targets:
        print(f"Processing '{t}'...")
        image = cv2.imread(t)
        if image is None:
            print(f"Could not load '{t}' as an image, skipping...")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # GPU 不足降低分辨率 或者考虑 分图片？
        image = cv2.resize(image, dsize=None, fx=0.5, fy=0.5)

        base = os.path.basename(t)
        base = os.path.splitext(base)[0]
        save_base = os.path.join(output, base)

        masks = generator.generate(image)

        os.makedirs(save_base, exist_ok=False)
        
        write_masks_to_folder(masks, save_base, image)
    print("Done!")

def main_prompt(targets, output, label, sam) -> None:
    print("Prompt: Loading model...")

    mask_predictor = SamPredictor(sam)

    for t in targets:
        print(f"Processing '{t}'...")
        image = cv2.imread(t)

        if image is None:
            print(f"Could not load '{t}' as an image, skipping...")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        base = os.path.basename(t)
        base = os.path.splitext(base)[0]
        save_base = os.path.join(output, base)

        boxes = collectBoxes(t, label)

        mask_predictor = SamPredictor(sam)
        mask_predictor.set_image(image)

        input_boxes = torch.tensor(boxes, device=mask_predictor.device)  
        transformed_boxes = mask_predictor.transform.apply_boxes_torch(input_boxes, image.shape[:2])

        masks, iou_predictions, low_res_masks = mask_predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=transformed_boxes,
            multimask_output=False
        )

        os.makedirs(save_base, exist_ok=False)
        
        write_cattle_to_folder(masks, boxes, save_base, image)
    print("Done!")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
