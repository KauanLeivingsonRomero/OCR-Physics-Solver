import os
import cv2
import pytesseract
from ollama import chat

IMAGES_FOLDER = "images"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

def get_latest_image(folder):
    if not os.path.exists(folder):
        return None

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not files:
        return None

    return max(files, key=os.path.getctime)

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    return thresh

def extract_text(image_path):
    processed = preprocess_image(image_path)

    if processed is None:
        return ""

    custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'

    text = pytesseract.image_to_string(
        processed,
        lang="por+eng",
        config=custom_config
    )

    return text.strip()

def ask_gemma(text):

    if len(text) < 20:
        return f"{RED}OCR failed or text too small."

    prompt = f"""
                Você é um professor universitário especialista em física.

                Para cada questão:
                1) Reescreva o enunciado corretamente
                2) Liste os dados
                3) Escolha as fórmulas
                4) Resolva passo a passo
                5) Apresente o resultado final com unidade

                Texto:
                {text}
              """

    try:
        response = chat(
            model="gemma3:4b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.message.content

    except Exception as e:
        return f"{RED}Error communicating with Ollama: {e}"

def main():
    image_path = get_latest_image(IMAGES_FOLDER)

    if not image_path:
        print(f"{RED}No images found at /images.")
        return

    print(f"\nReading: {image_path}")

    extracted_text = extract_text(image_path)

    print(f"{CYAN}\n========== EXTRACTED TEXT ==========\n{RESET}")
    print(YELLOW + extracted_text + RESET)

    print(f"{BLUE}\n[!] SENDING TO GEMMA 3\n{RESET}")
    answer = ask_gemma(extracted_text)

    print(f"{GREEN}\n========== FINAL ANSWER ==========\n{RESET}")
    print(GREEN + answer + RESET)

if __name__ == "__main__":
    main()