# Batch Image Editor

## Description

Batch Image Editor is a Python script which makes image processing for multiple images in a folder. It relies on the Pillow library to crop, rotate, resize and convert images without necessarily changing the original images.

The program takes a folder path as command argument, detects the supported image formats and processes them in alphabetic order. The results are stored in another output folder, while the original pictures have not been altered.

## Features

The program will deal with the following operations:

- Uniform Crop: Crop the first image content bounds and do the same for all images.
- Automatic Crop: Crops each image automatically and according to its content.
- **Rotate:** Rotates images by 90, 180, or 270 degrees.
- Resize: Resize images to a width and height.
- Convert Format: Convert images into JPG, PNG, and WebP. Transparency is converted to white background when turning to JPG.

The program accepts images as inputs in the following formats: JPG, JPEG, PNG, and WEBP. It also verifies input file and operation parameter validity, and points out missing folders, unsupported input file and parameter errors that the user made.

## Requirements

- Python 3
- Pillow
- pytest (to run tests)

## Installation

Install the necessary dependencies, with:

```bash
pip install -r requirements.txt
```

## Usage

You can run the program from the terminal:

```bash
python project.py
```

Type in the location of the folder that holds your images. The program will print a menu to select an operation, and enter any extra arguments it asks for.

The processed images are stored in a separate `<input_folder_name>_edited` folder next to the input folder.

## Testing

To run the test suite use:

```bash
pytest
```

The tests include image cropping, rotation, boundary detection, and format conversion.

## Project Structure

- `project.py` - This file contains the main program and image processing functions.
- `test_project.py`: A file that includes tests for the function of the program.
- `requirements.txt` — A list of Python dependency requirements.

## Design Decisions

The program breaks down the image-processing tasks into smaller functions, which are easier to test and maintain. Validating the input helps to avoid performing invalid operations and saving the results separately from the original files prevents the original files from being overwritten.

The project has been designed to provide training on the following topics in Python programming: Handling of files, Usage of external libraries, Input validation, Automated testing, and Construction of practical image processing tool.
