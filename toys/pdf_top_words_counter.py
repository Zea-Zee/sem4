import PyPDF2
import pandas as pd
from collections import Counter
import re


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def clean_text(text):
    cleaned_text = re.sub(r'[^A-Za-z\s]', '', text)  # Оставляем только буквы и пробелы
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Удаляем лишние пробелы
    cleaned_text = cleaned_text.lower()  # Приводим к нижнему регистру
    return cleaned_text

def filter_words_by_length(words, min_length=4):
    return [word for word in words if len(word) >= min_length]

def calculate_word_statistics(text):
    words = clean_text(text).split()
    filtered_words = filter_words_by_length(words)
    word_counts = Counter(filtered_words)
    total_words = sum(word_counts.values())
    word_statistics = []
    for word, count in word_counts.most_common(10_000):
        percentage = (count / total_words) * 100
        word_statistics.append({'word': word, 'percentage': round(percentage, 3)})
    return word_statistics

def save_to_csv(word_statistics, csv_path):
    df = pd.DataFrame(word_statistics)
    df.to_csv(csv_path, index=False)

def main(pdf_path, csv_path):
    text = extract_text_from_pdf(pdf_path)
    word_statistics = calculate_word_statistics(text)
    save_to_csv(word_statistics, csv_path)

if __name__ == "__main__":
    pdf_path = "text.pdf"  # Укажите путь к вашему PDF-файлу
    csv_path = "out.csv"  # Укажите путь для сохранения CSV
    main(pdf_path, csv_path)
