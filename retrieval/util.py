from PIL import Image


def create_overlapping_images(images: list[Image.Image], overlap: int = 20):
    """
    Creates a list of images with a specified percentage of overlap from the input image list.

    Args:
        images: List of same-sized PIL images.
        overlap: The percentage of overlap between consecutive images (default is 20).

    Returns:
        List of images with the specified overlap.
    """

    if overlap < 0 or overlap > 100:
        raise ValueError("Overlap must be between 0 and 100.")

    if not images:
        raise ValueError("The image list is empty.")

    # Check that all images are the same size
    width, height = images[0].size
    for img in images:
        if img.size != (width, height):
            raise ValueError("All images must have the same dimensions.")

    current = Image.new("RGB", (width, height))
    output = []

    location = 0
    while True:
        idx = location // 100
        if idx >= len(images) - 1:
            output.append(images[-1].copy())
            break

        # Calculate the offset for the current image
        offset = -int(height * location / 100)
        current.paste(images[idx], (0, offset))
        current.paste(images[idx+1], (0, offset + height))

        output.append(current.copy())
        location += (100 - overlap)

    return output