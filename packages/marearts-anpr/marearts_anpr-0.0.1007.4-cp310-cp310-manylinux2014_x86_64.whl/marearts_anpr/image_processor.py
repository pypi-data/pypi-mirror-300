from PIL import Image
import numpy as np

class CustomImageProcessor:
    def __init__(self, cfg):
        # List of expected keys in the cfg
        self.expected_keys = ['crop_size', 'do_center_crop', 'do_normalize', 'do_rescale', 'do_resize', 
                              'feature_extractor_type', 'image_mean', 'image_processor_type', 'image_std', 
                              'resample', 'rescale_factor', 'size']
        self.cfg = cfg
        self.validate_cfg()

    def validate_cfg(self):
        # Check for unexpected keys
        for key in self.cfg:
            if key not in self.expected_keys:
                raise ValueError(f"Unexpected key '{key}' in cfg. Please remove or handle it.")
        
        # Validate expected keys
        if not isinstance(self.cfg.get('size', {}), dict) or 'height' not in self.cfg['size'] or 'width' not in self.cfg['size']:
            raise ValueError("Expected 'size' to be a dict with 'height' and 'width' keys in cfg.")

        if len(self.cfg.get('image_mean', [])) != 3 or len(self.cfg.get('image_std', [])) != 3:
            raise ValueError("Expected 'image_mean' and 'image_std' to be lists with 3 values each.")

    def validate_image(self, image):
        if not isinstance(image, Image.Image):
            raise ValueError(f"Expected input image to be a PIL.Image.Image instance. Got {type(image)} instead.")
        
        if image.mode != "RGB":
            raise ValueError(f"Expected image mode to be 'RGB'. Got '{image.mode}' instead.")

    
    def center_crop(self, image):
        w, h = image.size
        left = (w - self.cfg['crop_size'])/2
        top = (h - self.cfg['crop_size'])/2
        right = (w + self.cfg['crop_size'])/2
        bottom = (h + self.cfg['crop_size'])/2
        return image.crop((left, top, right, bottom))
    
    def resize(self, image):
        height, width = self.cfg['size']['height'], self.cfg['size']['width']
        return image.resize((width, height), resample=self.cfg['resample'])

    def normalize(self, image):
        mean = np.array(self.cfg['image_mean'])
        std = np.array(self.cfg['image_std'])
        image = image.astype(np.float64)  # Convert to float before performing arithmetic
        image -= mean.reshape((1,) * (image.ndim - 1) + (-1,))
        image /= std.reshape((1,) * (image.ndim - 1) + (-1,))
        return image

    def rescale(self, image):
        return image * self.cfg['rescale_factor']

    def __call__(self, image: Image.Image) -> dict:
        self.validate_image(image)
        
        if self.cfg['do_center_crop']:
            image = self.center_crop(image)
            
        if self.cfg['do_resize']:
            image = self.resize(image)

        image = np.array(image)  # Convert PIL Image to numpy array
        
        if self.cfg['do_normalize']:
            image = self.normalize(image)
            
        if self.cfg['do_rescale']:
            image = self.rescale(image)
        
        # Transpose to have channel-first format
        image = np.transpose(image, (2, 0, 1))
        image = image.astype(np.float32)  # Ensure image is float32


        return {'pixel_values': [image]}