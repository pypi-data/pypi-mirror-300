
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageChops
from PIL import ImageOps


class Immage:
    def __init__(self, image):
        self.image = image.convert('RGB')  # Ensure image is in RGB mode

    @classmethod
    def open(cls, image_path):
        """
        Opens an image from the given path and returns an ImageProcessor instance.

        Parameters:
        - image_path: Path to the image file.

        Returns:
        - ImageProcessor instance.
        """
        image = Image.open(image_path)
        return cls(image)

    # Basic Filters
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        return self

    def contour(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        return self

    def detail(self):
        self.image = self.image.filter(ImageFilter.DETAIL)
        return self

    def edge_enhance(self):
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        return self

    def edge_enhance_more(self):
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return self

    def emboss(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        return self

    def find_edges(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        return self

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        return self

    def smooth(self):
        self.image = self.image.filter(ImageFilter.SMOOTH)
        return self

    def smooth_more(self):
        self.image = self.image.filter(ImageFilter.SMOOTH_MORE)
        return self

    # Advanced Filters with Parameters
    def gaussian_blur(self, radius=2):
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        return self

    def unsharp_mask(self, radius=2, percent=150, threshold=3):
        self.image = self.image.filter(
            ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold)
        )
        return self

    def rank_filter(self, size=3, rank=0):
        self.image = self.image.filter(ImageFilter.RankFilter(size, rank))
        return self

    def median_filter(self, size=3):
        self.image = self.image.filter(ImageFilter.MedianFilter(size))
        return self

    def min_filter(self, size=3):
        self.image = self.image.filter(ImageFilter.MinFilter(size))
        return self

    def max_filter(self, size=3):
        self.image = self.image.filter(ImageFilter.MaxFilter(size))
        return self

    def mode_filter(self, size=3):
        self.image = self.image.filter(ImageFilter.ModeFilter(size))
        return self

    def custom_filter(self, kernel, size, scale=None, offset=0):
        custom_kernel = ImageFilter.Kernel(size, kernel, scale=scale, offset=offset)
        self.image = self.image.filter(custom_kernel)
        return self

    # Image Enhancements
    def enhance_color(self, factor=1.0):
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def enhance_contrast(self, factor=1.0):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def enhance_brightness(self, factor=1.0):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def enhance_sharpness(self, factor=1.0):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(factor)
        return self

    # Texture Application
    def apply_texture(self, texture_image):
        """
        Modulates the brightness of the current image using the brightness of the texture image.

        Parameters:
        - texture_image: PIL.Image object representing the texture image.

        Returns:
        - self: Allows for method chaining.
        """
        # Ensure the texture image is the same size as the current image
        texture_image = texture_image.resize(self.image.size).convert('L')

        # Convert the texture image to a brightness mask (grayscale)
        texture_brightness = texture_image.point(lambda p: p / 255.0)

        # Split the normal image into RGB channels
        r, g, b = self.image.split()

        # Apply the brightness mask to each channel
        r = ImageChops.multiply(r, texture_brightness)
        g = ImageChops.multiply(g, texture_brightness)
        b = ImageChops.multiply(b, texture_brightness)

        # Merge the channels back
        self.image = Image.merge('RGB', (r, g, b))
        return self

    # Procedural Texture Generation
    @staticmethod
    def generate_watercolor_paper_texture(width=1024, height=1024, scale=100, octaves=6, persistence=0.5, lacunarity=2.0, color_tint=(238, 232, 205)):
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
        - ImageProcessor instance with the generated texture image.
        """
        try:
            from noise import pnoise2
        except ImportError:
            raise ImportError("Please install the 'noise' library: pip install noise")

        noise_array = np.zeros((height, width))

        for y in range(height):
            for x in range(width):
                nx = x / scale
                ny = y / scale
                noise_value = 0
                frequency = 1
                amplitude = 1
                max_value = 0

                for _ in range(octaves):
                    noise_value += amplitude * pnoise2(nx * frequency, ny * frequency, repeatx=width, repeaty=height, base=0)
                    max_value += amplitude
                    amplitude *= persistence
                    frequency *= lacunarity

                noise_array[y][x] = noise_value / max_value

        min_val = noise_array.min()
        max_val = noise_array.max()
        normalized_noise = (noise_array - min_val) / (max_val - min_val)
        noise_image_array = (normalized_noise * 255).astype(np.uint8)

        texture_image = Image.fromarray(noise_image_array, mode='L')
        texture_image = texture_image.filter(ImageFilter.SMOOTH_MORE)
        texture_image = texture_image.filter(ImageFilter.EMBOSS())
        enhancer = ImageEnhance.Contrast(texture_image)
        texture_image = enhancer.enhance(1.2)

        # Add color tint
        texture_image = ImageProcessor.add_color_tint(texture_image, tint_color=color_tint)

        return ImageProcessor(texture_image)

    @staticmethod
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
        tinted_image = Image.composite(color_image, Image.new('RGB', image.size, (0, 0, 0)), image)
        return tinted_image

    # Fractal-Based Upscaling
    def fractal_upscale(self, scale_factor=2, octaves=5):
        """
        Upscales an image and enhances it with fractal noise.

        Parameters:
        - scale_factor: Factor by which to upscale the image.
        - octaves: Number of octaves for fractal noise generation.

        Returns:
        - self: Allows for method chaining.
        """
        original_width, original_height = self.image.size
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        upscaled_image = self.image.resize((new_width, new_height), resample=Image.BICUBIC)

        # Generate fractal noise
        fractal_noise = self.generate_fractal_noise(new_width, new_height, scale=1.0, octaves=octaves)
        fractal_noise_image = Image.fromarray(fractal_noise)

        # Adjust the fractal noise intensity
        enhancer = ImageEnhance.Brightness(fractal_noise_image)
        fractal_noise_image = enhancer.enhance(0.5)  # Adjust the factor as needed

        # Blend the upscaled image with the fractal noise
        upscaled_image = upscaled_image.convert('RGB')
        fractal_noise_image = fractal_noise_image.convert('RGB')
        blended_image = ImageChops.add(upscaled_image, fractal_noise_image, scale=1.0, offset=0)

        # Enhance the contrast
        enhancer = ImageEnhance.Contrast(blended_image)
        final_image = enhancer.enhance(1.2)  # Adjust the factor as needed

        self.image = final_image
        return self

    @staticmethod
    def generate_fractal_noise(width, height, scale=1.0, octaves=5, persistence=0.5, lacunarity=2.0):
        """
        Generates fractal noise using the Perlin noise algorithm.

        Parameters:
        - width, height: Dimensions of the output noise image.
        - scale: Controls the granularity of the noise.
        - octaves: Number of layers of noise to add complexity.
        - persistence: Controls the amplitude decrease between octaves.
        - lacunarity: Controls the frequency increase between octaves.

        Returns:
        - A NumPy array of the fractal noise.
        """
        try:
            from noise import pnoise2
        except ImportError:
            raise ImportError("Please install the 'noise' library: pip install noise")

        noise = np.zeros((height, width))
        frequency = 1 / scale
        amplitude = 1.0
        max_amplitude = 0.0

        for _ in range(octaves):
            for y in range(height):
                for x in range(width):
                    nx = x / width * frequency
                    ny = y / height * frequency
                    noise[y][x] += amplitude * pnoise2(nx, ny, repeatx=width, repeaty=height, base=0)
            max_amplitude += amplitude
            amplitude *= persistence
            frequency *= lacunarity

        # Normalize the noise to 0 - 255
        noise = noise / max_amplitude
        noise_normalized = ((noise - noise.min()) / (noise.max() - noise.min())) * 255.0
        noise_normalized = noise_normalized.astype(np.uint8)

        return noise_normalized

    # Save and Show Methods
    def save(self, output_path, format=None):
        self.image.save(output_path, format=format)
        return self

    def show(self):
        self.image.show()
        return self

    # Overload the pipe operator for chaining with |
    def __or__(self, other):
        if callable(other):
            return other(self)
        else:
            raise TypeError("Right operand must be a callable")

