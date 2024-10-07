import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def generate_watercolor_paper_texture(
    width=1024,
    height=1024,
    scale=200,
    octaves=4,
    persistence=0.8,
    lacunarity=2.0,
    color_tint=(255, 250, 205)
):
    try:
        from noise import pnoise2
    except ImportError:
        raise ImportError("Please install the 'noise' library: pip install noise")

    # Create coordinate grids
    x = np.linspace(0, width, width, endpoint=False)
    y = np.linspace(0, height, height, endpoint=False)
    nx, ny = np.meshgrid(x / scale, y / scale)

    # Initialize noise array
    noise_array = np.zeros((height, width))
    frequency = 1
    amplitude = 1
    max_amplitude = 0

    for _ in range(octaves):
        # Generate noise using vectorized pnoise2
        noise = np.vectorize(pnoise2)(
            nx * frequency,
            ny * frequency,
            repeatx=width,
            repeaty=height,
            base=0
        )
        noise_array += noise * amplitude

        max_amplitude += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    # Normalize the noise
    noise_array /= max_amplitude
    min_val = noise_array.min()
    max_val = noise_array.max()
    if max_val - min_val == 0:
        normalized_noise = noise_array - min_val
    else:
        normalized_noise = (noise_array - min_val) / (max_val - min_val)

    # Adjust the normalized_noise to make it lighter
    normalized_noise = normalized_noise * 0.5 + 0.5  # Range from 0.5 to 1.0

    # Convert to 0-255 range
    noise_image_array = (normalized_noise * 255).astype(np.uint8)

    # Convert to PIL image
    texture_image = Image.fromarray(noise_image_array, mode='L')

    # Apply filters to enhance the texture
    texture_image = texture_image.filter(ImageFilter.SMOOTH)
    texture_image = texture_image.filter(ImageFilter.EMBOSS())
    enhancer = ImageEnhance.Contrast(texture_image)
    texture_image = enhancer.enhance(1.1)  # Slightly reduce contrast

    # Add color tint
    texture_image = add_color_tint(texture_image, tint_color=color_tint)

    return texture_image

def add_color_tint(image, tint_color=(255, 250, 205)):
    """
    Adds a color tint to a grayscale image.

    Parameters:
    - image: PIL.Image object in 'L' mode.
    - tint_color: Tuple representing the RGB color to tint the image.

    Returns:
    - Tinted PIL.Image object in 'RGB' mode.
    """
    if image.mode != 'L':
        image = image.convert('L')

    # Convert the grayscale image to RGB
    image_rgb = image.convert('RGB')

    # Create a solid color image with the tint color
    tint_layer = Image.new('RGB', image.size, tint_color)

    # Blend the grayscale image and the tint layer
    tinted_image = Image.blend(image_rgb, tint_layer, alpha=0.5)

    return tinted_image

