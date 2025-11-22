from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw shield background
    shield_color = (59, 130, 246)  # Blue
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill=shield_color)
    
    # Draw shield symbol
    center = size // 2
    shield_size = size // 3
    points = [
        (center, margin + shield_size//4),
        (center - shield_size//2, center),
        (center, size - margin - shield_size//4),
        (center + shield_size//2, center)
    ]
    draw.polygon(points, fill='white')
    
    # Save
    img.save(filename, 'PNG')

# Create icons
os.makedirs('dist', exist_ok=True)
create_icon(16, 'dist/icon16.png')
create_icon(48, 'dist/icon48.png')
create_icon(128, 'dist/icon128.png')
print("Icons created successfully!")