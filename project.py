from pathlib import Path
from PIL import Image


def main():

    input_folder = Path(input("Enter input folder path: ").strip().strip('"'))
    if not input_folder.is_dir():
        print("Folder not found")
        return

    images = []

    for path in input_folder.iterdir():
        if path.is_file() and path.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            images.append(path)
    images = sorted(images)

    if not images:
        print("No images found")
        return
    output_folder = input_folder.parent / f"{input_folder.name}_edited"
    output_folder.mkdir(exist_ok=True)
    while True:
        print("Batch Image Editor")
        print("1. Uniform crop")
        print("2. Automatic crop")
        print("3. Rotate")
        print("4. Resize")
        print("5. Convert format")
        print("6. Exit")
        choice = input("Choose mode: ")

        if choice in ("1", "2", "3", "4", "5", "6"):
            break
        else:
            print("Invalid choice")
    if choice == "6":
        return
    elif choice == "1":
        uniform_crop(images, output_folder)
    elif choice == "2":
        automatic_crop(images, output_folder)
    elif choice == "3":
        while True:
            try:
                angle = int(input("Enter rotation angle (90, 180, 270): "))
            except ValueError:
                print("Invalid angle")
            else:
                if angle in (90, 180, 270):
                    break

                else:
                    print("Invalid angle")
        rotate_images(images, output_folder, angle)

    elif choice == "4":
        while True:
            try:
                width = int(input("Width: "))
                height = int(input("Height: "))
            except ValueError:
                print("Invalid Value")
            else:
                if width > 0 and height > 0:
                    break

                else:
                    print("Invalid dimensions")
        resize_images(images, output_folder, width, height)

    elif choice == "5":
        while True:
            extension = input("Extension (jpg, png, webp): ").strip().lower()

            if extension in ("jpg", "png", "webp"):
                break
            else:
                print("Invalid extension")
        convert_images(images, output_folder, extension)


def automatic_crop(images, output_folder):

    for image_path in images:
        with Image.open(image_path) as image:
            top, bottom, left, right = find_borders(image)

            cropped = image.crop((left, top, right, bottom))
            cropped.save(output_folder / image_path.name)


def uniform_crop(images, output_folder):
    with Image.open(images[0]) as first_image:
        top, bottom, left, right = find_borders(first_image)

    for image_path in images:
        with Image.open(image_path) as image:
            cropped = image.crop((left, top, right, bottom))
            cropped.save(output_folder / image_path.name)


def rotate_images(images, output_folder, angle):
    for image_path in images:
        with Image.open(image_path) as image:
            rotated = image.rotate(-angle, expand=True)
            rotated.save(output_folder / image_path.name)


def resize_images(images, output_folder, width, height):
    for image_path in images:
        with Image.open(image_path) as image:
            resized = image.resize((width, height))
            resized.save(output_folder / image_path.name)


def convert_images(images, output_folder, extension):
    for image_path in images:
        with Image.open(image_path) as image:
            output_path = output_folder / f"{image_path.stem}.{extension}"

            if extension == "jpg":
                rgba_image = image.convert("RGBA")
                background = Image.new("RGB", image.size, "white")
                background.paste(rgba_image, mask=rgba_image.getchannel("A"))
                background.save(output_path)

            else:
                image.save(output_path)


def find_borders(image):

    image = image.convert("RGB")
    width, height = image.size
    background = image.getpixel((0, 0))
    tolerance = 20

    def same_color(pixel):
        return all(abs(pixel[i] - background[i]) <= tolerance for i in range(3))

    top = 0
    bottom = height
    left = 0
    right = width

    for y in range(height):
        if not all(same_color(image.getpixel((x, y))) for x in range(width)):
            top = y
            break
    else:
        image.close()
        return 0, height, 0, width

    for y in range(height - 1, -1, -1):
        if not all(same_color(image.getpixel((x, y))) for x in range(width)):
            bottom = y + 1
            break

    for x in range(width):
        if not all(same_color(image.getpixel((x, y))) for y in range(top, bottom)):
            left = x
            break

    for x in range(width - 1, -1, -1):
        if not all(same_color(image.getpixel((x, y))) for y in range(top, bottom)):
            right = x + 1
            break

    image.close()

    return top, bottom, left, right


if __name__ == "__main__":
    main()
