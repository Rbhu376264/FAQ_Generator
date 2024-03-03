import csv
import requests
from bs4 import BeautifulSoup
import json
import certifi

def fetch_and_parse_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers, verify=False)
    paragraphs_text = []

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            paragraphs_text.append(paragraph.text)
    else:
        print(f"Failed to retrieve the webpage for URL: {url}")
    return paragraphs_text

def process_csv_and_extract_text(csv_file_path, output_json_path):
    data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Assuming the URLs are in a column named 'URL'
            univ_name = row.get('University')
            url = row.get('Graduate Admission Link')  # Using .get() for safer access
            faq_url = row.get('FAQ Link')
            if url:  # Check if URL is not None or empty
                paragraphs_text = fetch_and_parse_url(url)
                faq_texts = fetch_and_parse_url(faq_url)
                data.append({
                    "University" : univ_name,
                    "URL": url,
                    "Admission Content": paragraphs_text,
                    "FAQ Content" : faq_texts
                })

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    csv_file_path = 'List.csv'  # Adjust the path as needed
    output_json_path = 'universities_content.json'  # Output JSON file path
    process_csv_and_extract_text(csv_file_path, output_json_path)
    print(f"Data has been successfully extracted and saved to {output_json_path}")

if __name__ == "__main__":
    main()
