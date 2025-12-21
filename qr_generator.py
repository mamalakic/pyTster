"""QR code generation for Spotify song URLs."""

import qrcode
from PIL import Image
from io import BytesIO
import config


class QRGenerator:
    """Generator for QR codes linking to Spotify songs."""
    
    def __init__(self, qr_size: int = None):
        """
        Initialize QR code generator.
        
        Args:
            qr_size: Size of QR code in pixels
        """
        self.qr_size = qr_size or config.QR_SIZE
    
    def generate_qr_code(self, url: str) -> Image.Image:
        """
        Generate a QR code for a given URL.
        
        Args:
            url: URL to encode in QR code
            
        Returns:
            PIL Image object containing the QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Resize to desired size
        img = img.resize((self.qr_size, self.qr_size), Image.Resampling.LANCZOS)
        
        return img
    
    def generate_qr_bytes(self, url: str) -> bytes:
        """
        Generate QR code and return as bytes.
        
        Args:
            url: URL to encode in QR code
            
        Returns:
            QR code image as bytes
        """
        img = self.generate_qr_code(url)
        
        # Convert to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes.getvalue()

