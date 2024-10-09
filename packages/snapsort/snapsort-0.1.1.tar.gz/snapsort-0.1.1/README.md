# snapsort

snapsort is a Python tool used to segregate individuals in group photos and compare their faces to a collection of images for matches using YOLO for detection and DeepFace for face verification.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install snapsort.

```bash
pip install snapsort
```

## Usage

```bash
snapsort <image_path> <group_dir> <output_dir>
```
### Arguments:

    image_path: Path to the input image containing people to be detected.
    group_dir: Directory containing group images for face comparison.
    output_dir: Directory where cropped images and matched group images will be saved.

## Example
```bash
snapsort /path/to/input.jpg /path/to/group_images /path/to/output_dir
```
## Description
Detects individuals in the input image using the YOLO model.
Crops each person and saves the cropped images in the specified output directory.
Compares each cropped person image with group images in the specified directory using DeepFace (Facenet model).
Copies matched group images to a subdirectory in the output directory.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
