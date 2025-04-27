import os
import json
import glob
from config.settings import RAW_DIR, STRUCTURED_DIR, META_STRUCT, GEMINI_API_KEY, LLM_MODEL
from pipeline.extractor import extract_fields
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=GEMINI_API_KEY)


def call_llm(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(LLM_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[ERROR] Gemini API failed: {e}")
        raise

def organize_html(html: str) -> dict:
    prompt = (
        "You are a skilled data extraction expert specializing in parsing HTML to JSON structures.\n\n"
        "Your task is to extract restaurant information from the provided HTML into a STRICT JSON format.\n"
        "Mandatory fields:\n"
        "- name (string)\n"
        "- location (string)\n"
        "- menu_items (list of objects with item, price, description)\n"
        "- features (string)\n"
        "- hours (string)\n"
        "- contact (string)\n\n"
        "Important rules:\n"
        "- Always include ALL fields, even if the data is missing.\n"
        "- If a field cannot be found, set it as an EMPTY string \"\".\n"
        "- For menu_items, if no items are found, return an EMPTY list [].\n"
        "- Maintain correct JSON structure exactly as shown below.\n\n"
        "Output format:\n"
        "{\n"
        '  "name": "__________",\n'
        '  "location": "__________",\n'
        '  "menu_items": [\n'
        "    {\n"
        '      "item": "__________",\n'
        '      "price": "__________",\n'
        '      "description": "__________"\n'
        "    }\n"
        "  ],\n"
        '  "features": "__________",\n'
        '  "hours": "__________",\n'
        '  "contact": "__________"\n'
        "}\n\n"
        "Extract carefully from the following HTML content:\n\n"
        + html
    )

    try:
        result = call_llm(prompt)
        return json.loads(result)
    except Exception as e:
        print(f"[WARN] Falling back to local extractor for HTML due to error: {e}")
        return extract_fields(html)



def main():
    os.makedirs(STRUCTURED_DIR, exist_ok=True)
    entries = glob.glob(os.path.join(RAW_DIR, '*.html'))
    print(f"[INFO] Found {len(entries)} raw HTML files.")

    for entry in entries:
        fname = os.path.basename(entry)
        out_path = os.path.join(STRUCTURED_DIR, fname.replace('.html', '.json'))
        if os.path.exists(out_path):
            print(f"[SKIP] {fname} already processed.")
            continue

        print(f"[PROCESSING] Extracting data from {fname}")
        with open(entry, encoding='utf8') as f:
            html = f.read()
        data = organize_html(html)
        with open(out_path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2)

    meta = [{'file': f} for f in os.listdir(STRUCTURED_DIR) if f.endswith('.json')]
    with open(META_STRUCT, 'w', encoding='utf8') as f:
        json.dump(meta, f, indent=2)

    print(f"[DONE] Structured {len(meta)} files into {STRUCTURED_DIR}.")


if __name__ == '__main__':
    main()
