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
    first_image = Image.open(images[0])
    top, bottom, left, right = find_borders(first_image)
    first_image.close()

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
                background = Image.new("RGB", image.size, "white")

                if image.mode == "RGBA":
                    background.paste(image, mask=image.getchannel("A"))
                else:
                    background.paste(image)

                background.save(output_path)

            else:
                image.save(output_path)


def find_borders(image):

    width, height = image.size

    for y in range(height):
        black = True
        for x in range(width):
            pixel = image.getpixel((x, y))
            r, g, b = pixel[:3]
            if not (0 <= r <= 25 and 0 <= g <= 25 and 0 <= b <= 30):
                black = False
                break
        if not black:
            top = y
            break

    for y in range(height - 1, -1, -1):
        black = True
        for x in range(width):
            pixel = image.getpixel((x, y))
            r, g, b = pixel[:3]
            if not (0 <= r <= 25 and 0 <= g <= 25 and 0 <= b <= 30):
                black = False
                break
        if not black:
            bottom = y + 1
            break

    for x in range(width):
        black = True
        for y in range(height):
            pixel = image.getpixel((x, y))
            r, g, b = pixel[:3]
            if not (0 <= r <= 25 and 0 <= g <= 25 and 0 <= b <= 30):
                black = False
                break
        if not black:
            left = x
            break

    for x in range(width - 1, -1, -1):
        black = True
        for y in range(height):
            pixel = image.getpixel((x, y))
            r, g, b = pixel[:3]
            if not (0 <= r <= 25 and 0 <= g <= 25 and 0 <= b <= 30):
                black = False
                break
        if not black:
            right = x + 1
            break

    return top, bottom, left, right

if __name__=="__main__":
    main()
