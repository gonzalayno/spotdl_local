from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Crear una imagen de 512x512 píxeles
    size = 512
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Dibujar un círculo verde (color de Spotify)
    circle_color = (29, 185, 84)  # Color verde de Spotify
    draw.ellipse([0, 0, size-1, size-1], fill=circle_color)
    
    # Dibujar un círculo blanco en el centro
    white_circle_size = int(size * 0.8)
    white_circle_pos = (size - white_circle_size) // 2
    draw.ellipse([white_circle_pos, white_circle_pos, 
                  white_circle_pos + white_circle_size - 1, 
                  white_circle_pos + white_circle_size - 1], 
                 fill='white')
    
    # Dibujar las letras "SD" en verde
    try:
        # Intentar usar una fuente del sistema
        font_size = int(size * 0.5)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        # Si no se encuentra la fuente, usar la predeterminada
        font = ImageFont.load_default()
    
    text = "SD"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=circle_color, font=font)
    
    # Guardar el icono
    image.save('spotdl.png', 'PNG')

if __name__ == "__main__":
    create_icon() 