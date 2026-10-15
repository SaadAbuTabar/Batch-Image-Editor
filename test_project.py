from PIL import Image
from project import (
    find_borders,
    resize_images,
    rotate_images,
    convert_images,
    automatic_crop,
    uniform_crop,
)


def test_resize_images(tmp_path):
    image1_path = tmp_path / "first.png"
    image2_path = tmp_path / "second.png"
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    Image.new("RGB", (100, 100), "red").save(image1_path)
    Image.new("RGB", (200, 150), "blue").save(image2_path)

    resize_images([image1_path, image2_path], output_folder, 50, 30)

    for name in ("first.png", "second.png"):
        with Image.open(output_folder / name) as image:
            assert image.size == (50, 30)


def test_rotate_images(tmp_path):
    image1_path = tmp_path / "first.png"
    image2_path = tmp_path / "second.png"
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    Image.new("RGB", (100, 50), "red").save(image1_path)
    Image.new("RGB", (200, 150), "blue").save(image2_path)

    rotate_images([image1_path, image2_path], output_folder, 90)

    expected_sizes = {
        "first.png": (50, 100),
        "second.png": (150, 200),
    }

    for name, expected_size in expected_sizes.items():
        with Image.open(output_folder / name) as image:
            assert image.size == expected_size


def test_convert_images(tmp_path):
    image1_path = tmp_path / "first.png"
    image2_path = tmp_path / "second.png"
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    Image.new("RGBA", (100, 50), (255, 0, 0, 128)).save(image1_path)
    Image.new("RGBA", (200, 150), (0, 0, 255, 128)).save(image2_path)

    convert_images([image1_path, image2_path], output_folder, "jpg")

    expected_sizes = {
        "first.jpg": (100, 50),
        "second.jpg": (200, 150),
    }

    for name, expected_size in expected_sizes.items():
        with Image.open(output_folder / name) as image:
            assert image.format == "JPEG"
            assert image.mode == "RGB"
            assert image.size == expected_size


def test_automatic_crop(tmp_path):
    image1_path = tmp_path / "first.png"
    image2_path = tmp_path / "second.png"
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    image1 = Image.new("RGB", (10, 10), "black")
    image2 = Image.new("RGB", (12, 12), "black")

    for y in range(2, 8):
        for x in range(3, 7):
            image1.putpixel((x, y), (255, 255, 255))

    for y in range(4, 10):
        for x in range(5, 9):
            image2.putpixel((x, y), (255, 255, 255))

    image1.save(image1_path)
    image2.save(image2_path)

    automatic_crop([image1_path, image2_path], output_folder)

    expected_sizes = {
        "first.png": (4, 6),
        "second.png": (4, 6),
    }

    for name, expected_size in expected_sizes.items():
        with Image.open(output_folder / name) as image:
            assert image.size == expected_size


def test_uniform_crop(tmp_path):
    image1_path = tmp_path / "first.png"
    image2_path = tmp_path / "second.png"
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    image1 = Image.new("RGB", (10, 10), "black")
    image2 = Image.new("RGB", (10, 10), "black")

    for y in range(2, 8):
        for x in range(3, 7):
            image1.putpixel((x, y), (255, 255, 255))
            image2.putpixel((x, y), (255, 255, 255))

    image1.save(image1_path)
    image2.save(image2_path)

    uniform_crop([image1_path, image2_path], output_folder)

    for name in ("first.png", "second.png"):
        with Image.open(output_folder / name) as cropped:
            assert cropped.size == (4, 6)