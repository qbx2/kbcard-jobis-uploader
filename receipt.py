from PIL import Image, ImageDraw, ImageFont


def generate_image(entity):
    img = Image.new('RGB', (500, 400))
    draw = ImageDraw.Draw(img, 'RGB')
    text = '\n'.join(f'{k}: {v}' for k, v in entity.items())
    font = ImageFont.truetype(font='AppleGothic', size=20)
    draw.text((20, 20), text, font=font)
    return img
