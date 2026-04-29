import os
import random
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

IMAGES_FOLDER = "images"
OUTPUT_FOLDER = "output"


def pick_random_image():
    files = [
        f for f in os.listdir(IMAGES_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ]
    if not files:
        raise ValueError("No images found in images folder.")
    return os.path.join(IMAGES_FOLDER, random.choice(files))


def generate_meme_caption():
    prompt = """
    Write 1 short funny meme caption.
    Keep it very short.
    No explanation.
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text.strip()


def add_caption_to_image(image_path, caption, output_path):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    width, height = image.size

    try:
        font = ImageFont.truetype("arial.ttf", size=max(40, width // 12))
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), caption, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (width - text_width) // 2
    text_y = height - text_height - 40

    draw.text(
        (text_x, text_y),
        caption,
        font=font,
        fill="white",
        stroke_width=3,
        stroke_fill="black"
    )

    image.save(output_path)


def generate_meme():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    image_path = pick_random_image()
    caption = generate_meme_caption()
    output_path = os.path.join(OUTPUT_FOLDER, "meme.jpg")

    add_caption_to_image(image_path, caption, output_path)

    return image_path, caption, output_path


def chat_with_bot(user_message):
    response = client.responses.create(
        model="gpt-5-mini",
        input=user_message
    )
    return response.output_text.strip()


def main():
    print("Chatbot started.")
    print("Type 'meme' to generate a meme.")
    print("Type 'exit' to quit.")

    while True:
        user_message = input("\nYou: ").strip()

        if user_message.lower() == "exit":
            print("Bot: Goodbye.")
            break

        elif user_message.lower() == "meme":
            print("Bot: Generating meme...")
            image_path, caption, output_path = generate_meme()
            print("Bot: Meme created.")
            print("Chosen image:", image_path)
            print("Caption:", caption)
            print("Saved to:", output_path)

        else:
            bot_reply = chat_with_bot(user_message)
            print("Bot:", bot_reply)


if __name__ == "__main__":
    main()