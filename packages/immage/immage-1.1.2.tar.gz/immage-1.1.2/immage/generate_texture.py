import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def generate_watercolor_paper_texture(
    width=1024,
    height=1024,
    scale=100,
    octaves=6,
    persistence=0.5,
    lacunarity=2.0,
    color_tint=(238, 232, 205)
):
    """
    Generates a procedural watercolor paper texture using Perlin noise.

    Parameters:
    - width: Width of the texture image.
    - height: Height of the texture image.
    - scale: Scale of the noise patterns.
    - octaves: Number of noise layers to combine.
    - persistence: Controls amplitude of each octave.
    - lacunarity: Controls frequency of each octave.
    - color_tint: RGB tuple for tinting the texture.

    Returns:
    - A PIL.Image object representing the watercolor paper texture.
    """
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
        # Avoid division by zero
        normalized_noise = noise_array - min_val
    else:
        normalized_noise = (noise_array - min_val) / (max_val - min_val)

    # Convert to 0-255 range
    noise_image_array = (normalized_noise * 255).astype(np.uint8)

    # Convert to PIL image
    texture_image = Image.fromarray(noise_image_array, mode='L')

    # Apply filters to enhance the texture
    texture_image = texture_image.filter(ImageFilter.SMOOTH_MORE)
    texture_image = texture_image.filter(ImageFilter.EMBOSS())
    enhancer = ImageEnhance.Contrast(texture_image)
    texture_image = enhancer.enhance(1.2)

    # Add color tint
    texture_image = add_color_tint(texture_image, tint_color=color_tint)

    return texture_image

def add_color_tint(image, tint_color=(238, 232, 205)):
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

    color_image = Image.new('RGB', image.size, tint_color)
    # Create an alpha mask based on the grayscale image
    alpha = image.point(lambda p: p / 255.0)
    # Convert alpha to 'L' mode if necessary
    if alpha.mode != 'L':
        alpha = alpha.convert('L')
    # Composite the tinted color and black image using the alpha mask
    tinted_image = Image.composite(color_image, Image.new('RGB', image.size, (0, 0, 0)), alpha)
    return tinted_image

