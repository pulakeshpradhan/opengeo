from PIL import Image, ImageDraw
import math
import os

# Create assets directory
os.makedirs('docs/assets', exist_ok=True)

# Create logo
img = Image.new('RGB', (400, 400), color='white')
draw = ImageDraw.Draw(img)

# Draw globe (teal circle)
draw.ellipse([50, 50, 350, 350], fill='#009688', outline='#00796B', width=8)

# Draw inner circle
draw.ellipse([120, 120, 280, 280], fill='white', outline='#00796B', width=4)

# Draw grid lines (latitude/longitude)
draw.line([200, 100, 200, 300], fill='#00796B', width=3)
draw.line([100, 200, 300, 200], fill='#00796B', width=3)

# Draw data points around the circle
for i in range(8):
    angle = i * 45
    x = 200 + 80 * math.cos(math.radians(angle))
    y = 200 + 80 * math.sin(math.radians(angle))
    draw.ellipse([x-5, y-5, x+5, y+5], fill='#FF5722')

# Save logo
img.save('docs/assets/logo.png')
print("Logo created: docs/assets/logo.png")

# Create favicon
favicon = img.resize((64, 64), Image.Resampling.LANCZOS)
favicon.save('docs/assets/favicon.ico')
print("Favicon created: docs/assets/favicon.ico")
