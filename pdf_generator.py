from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import config
from qr_generator import QRGenerator


class PDFGenerator:
    def __init__(self):
        self.qr_generator = QRGenerator()
        self.page_width = config.PAGE_WIDTH
        self.page_height = config.PAGE_HEIGHT
        self.margin = config.MARGIN
        self.cards_per_page = config.CARDS_PER_PAGE
        
        # Calculate card dimensions (2 columns x 3 rows)
        self.cols = 2
        self.rows = 3
        self.card_width = (self.page_width - 2 * self.margin) / self.cols
        self.card_height = (self.page_height - 2 * self.margin) / self.rows
        
        # Corner mark settings (for ink-saving borders)
        self.corner_length = 12  # Length of corner marks in points
        self.border_line_width = 1.5  # Thicker lines for visibility
        self.corner_inset = 8  # Distance from edge to corner marks (makes them closer to card content)
    
    def _get_card_position(self, card_index):
        col = card_index % self.cols
        row = card_index // self.cols
        x = self.margin + col * self.card_width
        # Y coordinate is from bottom, so need to invert the row
        y = self.page_height - self.margin - (row + 1) * self.card_height
        return x, y
    
    def _get_year_color(self, year_str: str) -> tuple:
        """
        Gradient RGB color based on year (1900 to 2025+)
        
        Args:
            year_str: Year as string
            
        Returns:
            RGB tuple (r, g, b) with values 0-1
        """
        try:
            year = max(1900, min(2025, int(year_str)))
        except (ValueError, TypeError):
            return (0, 0, 0)
        
        t = (year - 1900) / 125
        
        # Normalize to 0-1 range
        normalized = (year - 1900) / (2025 - 1900)
        
        # Color gradient from dark blue (old) to dark red (new)
        if normalized < 0.5:
            # 1900-1962: Dark blue to purple
            t = normalized * 2
            r = 0.2 + (0.4 * t)  # 0.2 to 0.6
            g = 0.0 + (0.1 * t)  # 0.0 to 0.1
            b = 0.5 + (0.2 * t)  # 0.5 to 0.7
        else:
            # 1963-2025: Purple to dark red
            t = (normalized - 0.5) * 2
            r = 0.6 + (0.3 * t)  # 0.6 to 0.9
            g = 0.1 - (0.1 * t)  # 0.1 to 0.0
            b = 0.7 - (0.5 * t)  # 0.7 to 0.2
        
        return (r, g, b)
    
    def _wrap_text(self, c: canvas.Canvas, text: str, font_name: str, 
                   font_size: float, max_width: float) -> list:
        """
        Wrap text into multiple lines to fit within max width.
        If text is longer than 50 characters, ellipsizes instead of wrapping.
        
        Args:
            c: ReportLab canvas
            text: Text to wrap
            font_name: Font name
            font_size: Font size
            max_width: Maximum width in points
            
        Returns:
            List of text lines
        """
        # If text is longer than 50 characters, ellipsize it
        if len(text) > 50:
            truncated = text
            while c.stringWidth(truncated + "...", font_name, font_size) > max_width and len(truncated) > 10:
                truncated = truncated[:-1]
            return [truncated + "..."]
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, font_name, font_size) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines or [text]
    
    def _draw_corner_marks(self, c, x, y, w, h):
        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.setLineWidth(self.border_line_width)
        
        i = self.corner_inset
        cl = self.corner_length
        
        # Bottom-left corner (inset from edges)
        c.line(x + inset, y + inset, x + inset + self.corner_length, y + inset)  # Horizontal
        c.line(x + inset, y + inset, x + inset, y + inset + self.corner_length)  # Vertical
        
        # Bottom-right corner (inset from edges)
        c.line(x + width - inset - self.corner_length, y + inset, x + width - inset, y + inset)  # Horizontal
        c.line(x + width - inset, y + inset, x + width - inset, y + inset + self.corner_length)  # Vertical
        
        # Top-left corner (inset from edges)
        c.line(x + inset, y + height - inset - self.corner_length, x + inset, y + height - inset)  # Vertical
        c.line(x + inset, y + height - inset, x + inset + self.corner_length, y + height - inset)  # Horizontal
        
        # Top-right corner (inset from edges)
        c.line(x + width - inset, y + height - inset - self.corner_length, x + width - inset, y + height - inset)  # Vertical
        c.line(x + width - inset - self.corner_length, y + height - inset, x + width - inset, y + height - inset)  # Horizontal
    
    def _draw_cutting_guides(self, c, x, y, w, h):
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.5)
        c.setDash(3, 3)
        
        i = self.corner_inset
        cl = self.corner_length
        
        c.line(x+i+cl, y+i, x+w-i-cl, y+i)
        c.line(x+w-i, y+i+cl, x+w-i, y+h-i-cl)
        c.line(x+w-i-cl, y+h-i, x+i+cl, y+h-i)
        c.line(x+i, y+h-i-cl, x+i, y+i+cl)
        
        c.setDash()
    
    def _draw_centered_lines(self, c, lines, center_x, start_y, font_name, font_size, line_height):
        for i, line in enumerate(lines):
            line_width = c.stringWidth(line, font_name, font_size)
            c.drawString(center_x - line_width/2, start_y - i*line_height, line)
    
    def _draw_qr_card(self, c, song, card_index):
        x, y = self._get_card_position(card_index)
        
        qr_bytes = self.qr_generator.generate_qr_bytes(song['url'])
        qr_image = ImageReader(BytesIO(qr_bytes))
        
        qr_size = min(self.card_width, self.card_height) * 0.85
        qr_x = x + (self.card_width - qr_size) / 2
        qr_y = y + (self.card_height - qr_size) / 2
        
        c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)
        self._draw_corner_marks(c, x, y, self.card_width, self.card_height)
        self._draw_cutting_guides(c, x, y, self.card_width, self.card_height)
    
    def _draw_info_card(self, c, song, card_index):
        x, y = self._get_card_position(card_index)
        center_x = x + self.card_width / 2
        center_y = y + self.card_height / 2
        max_width = self.card_width - 16
        
        # Year
        year_color = self._get_year_color(song['year'])
        c.setFillColorRGB(*year_color)
        c.setFont("Helvetica-Bold", 40)
        year_width = c.stringWidth(song['year'], "Helvetica-Bold", 40)
        c.drawString(center_x - year_width/2, center_y + 45, song['year'])
        
        # Title
        title_lines = self._wrap_text(c, song['title'], "Helvetica-Bold", 20, max_width)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 20)
        
        line_height = 24
        title_start_y = center_y + (len(title_lines) * line_height) / 2 - line_height / 2
        self._draw_centered_lines(c, title_lines, center_x, title_start_y, "Helvetica-Bold", 20, line_height)
        
        # Artists
        artist_lines = self._wrap_text(c, song['artists'], "Helvetica", 16, max_width)
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.setFont("Helvetica", 16)
        
        artist_line_height = 19
        artist_start_y = center_y - 30 - ((len(artist_lines) - 1) * artist_line_height / 2)
        self._draw_centered_lines(c, artist_lines, center_x, artist_start_y, "Helvetica", 16, artist_line_height)
        
        self._draw_corner_marks(c, x, y, self.card_width, self.card_height)
        self._draw_cutting_guides(c, x, y, self.card_width, self.card_height)
    
    def generate_pdf(self, songs, output_file):
        c = canvas.Canvas(output_file, pagesize=letter)
        
        total_songs = len(songs)
        total_pages = (total_songs + self.cards_per_page - 1) // self.cards_per_page * 2
        
        print(f"\nGenerating PDF with {total_songs} songs...")
        print(f"Total pages: {total_pages} ({total_pages // 2} front, {total_pages // 2} back)")
        
        for page_num in range(0, total_pages, 2):
            page_index = page_num // 2
            start_idx = page_index * self.cards_per_page
            end_idx = min(start_idx + self.cards_per_page, total_songs)
            page_songs = songs[start_idx:end_idx]
            
            print(f"Creating page {page_num + 1}/{total_pages} (QR codes)...")
            for i, song in enumerate(page_songs):
                self._draw_qr_card(c, song, i)
            c.showPage()
            
            print(f"Creating page {page_num + 2}/{total_pages} (song info)...")
            for i, song in enumerate(page_songs):
                mirrored_i = (i // self.cols) * self.cols + (self.cols - 1 - (i % self.cols))
                self._draw_info_card(c, song, mirrored_i)
            c.showPage()
        
        c.save()
        print(f"\nPDF saved to: {output_file}")
        print("\nPrinting instructions:")
        print("1. Print odd pages (QR codes)")
        print("2. Flip paper stack")
        print("3. Print even pages (song info)")
        print("4. Cut along borders")
