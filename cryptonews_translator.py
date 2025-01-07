# -*- coding: utf-8 -*-
"""CryptoNews_Translator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w_hiCELjwbo-3ZY0w0AzjD8Dm2bTYq-o
"""



# Import required libraries
import requests
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# Function to fetch news from CryptoPanic
def fetch_news(api_key):
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        # Extract relevant headlines and construct "click" URLs
        news_list = []
        for news in news_data.get("results", []):
            # Construct the "click" URL
            click_url = f"https://cryptopanic.com/news/click/{news['id']}/"
            news_list.append({"title": news["title"], "url": click_url})
        return news_list
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return []

# Function to set up the M2M100 model
def setup_translation_model():
    model_name = "facebook/m2m100_418M"
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name)
    model.to("cpu")  # Ensure the model runs on CPU
    tokenizer.src_lang = "en"  # Set source language
    return tokenizer, model

# Function to translate text using M2M100
def translate_text(text, tokenizer, model, target_lang="ms"):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id(target_lang))
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Main script
def main():
    # Set your CryptoPanic API Key
    API_KEY = "b07d7003878406ba6c40ccd64b044855e2e96c8b"

    # Step 1: Fetch news
    print("Fetching news from CryptoPanic...")
    news_list = fetch_news(API_KEY)

    if not news_list:
        print("No news fetched. Exiting.")
        return

    # Step 2: Set up the translation model
    print("Setting up the translation model...")
    tokenizer, model = setup_translation_model()

    # Step 3: Translate news titles and prepare the final list
    print("Translating news titles...")
    translated_news = []
    for news in news_list:
        malay_title = translate_text(news["title"], tokenizer, model)
        translated_news.append({"title": malay_title, "url": news["url"]})

    # Step 4: Print translated news
    print("\nTranslated News:")
    for news in translated_news:
        print(f"Title: {news['title']}\nURL: {news['url']}\n")

# Run the main script
if __name__ == "__main__":
    main()
