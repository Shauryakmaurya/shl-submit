import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import time
import json
import io
from PyPDF2 import PdfReader

TEST_TYPE_MAPPING = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}


BASE_URL = "https://www.shl.com"
BASE_CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/?start={}&type=1&type=1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_product_links(catalog_url):
    res = requests.get(catalog_url, headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")
    product_data = []

    rows = soup.select("table tr")
    for row in rows:
        link_tag = row.find("a", href=True)
        if not link_tag or not link_tag['href'].startswith("/solutions/products/product-catalog/view/"):
            continue

        full_link = urljoin(BASE_URL, link_tag['href'])

        cells = row.find_all("td")
        remote_testing = False
        adaptive_irt = False

        if len(cells) >= 3:
            if cells[1].find("span", class_="catalogue__circle -yes"):
                remote_testing = True
            if cells[2].find("span", class_="catalogue__circle -yes"):
                adaptive_irt = True

        product_data.append({
            "url": full_link,
            "title": link_tag.get_text(strip=True),
            "remote_testing": remote_testing,
            "adaptive_irt": adaptive_irt
        })

    return product_data


def extract_pdf_text(pdf_url):
    try:
        response = requests.get(pdf_url, headers=HEADERS)
        reader = PdfReader(io.BytesIO(response.content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip() if text else "Empty PDF content"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def scrape_product_page(entry):
    url = entry["url"]
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")

    # Title
    title = soup.find("h1")
    title_text = title.get_text(strip=True) if title else entry.get("title", "No Title")

    # Extract main content
    content_sections = []
    for section in soup.select("div.component-content, div.text, div.rich-text"):
        text = section.get_text(separator="\n", strip=True)
        if text:
            content_sections.append(text)

    if not content_sections:
        for p in soup.find_all("p"):
            text = p.get_text(separator="\n", strip=True)
            if text:
                content_sections.append(text)

    full_content = "\n\n".join(content_sections).strip()

    # ✅ Extract PDF content
    pdf_link_tag = soup.find("a", string=lambda t: t and "Fact Sheet" in t)
    pdf_url = urljoin(BASE_URL, pdf_link_tag['href']) if pdf_link_tag and pdf_link_tag.get("href", "").endswith(".pdf") else None
    pdf_content = extract_pdf_text(pdf_url) if pdf_url else "No Fact Sheet PDF found"

    # ✅ Extract Test Type code from detail block
    test_type_code = ""
    test_type_full = "Not found"

    # Look for the actual label + value pair on the product page
    labels = soup.select(".catalogue-detail__label")
    for label in labels:
        if "Test Type" in label.get_text(strip=True):
            value = label.find_next_sibling("div", class_="catalogue-detail__value")
            if value:
                code = value.get_text(strip=True).upper()
                if len(code) == 1 and code in TEST_TYPE_MAPPING:
                    test_type_code = code
                    test_type_full = TEST_TYPE_MAPPING[code]
            break  # Exit after finding Test Type

    return {
        "url": url,
        "title": title_text,
        "test_type_code": test_type_code,
        "test_type_full": test_type_full,
        "content": full_content if full_content else "No meaningful content found",
        "remote_testing": entry.get("remote_testing", False),
        "adaptive_irt": entry.get("adaptive_irt", False),
        "pdf_url": pdf_url,
        "pdf_content": pdf_content
    }

def main():
    all_products = []
    for start in tqdm(range(0, 373, 12), desc="Scraping Catalog Pages"):
        catalog_url = BASE_CATALOG_URL.format(start)
        try:
            product_links = get_product_links(catalog_url)
            time.sleep(1)

            for entry in tqdm(product_links, desc=f"Scraping Products from start={start}", leave=False):
                try:
                    product_data = scrape_product_page(entry)
                    all_products.append(product_data)
                    time.sleep(0.5)
                except Exception as e:
                    print(f"[!] Failed to scrape product page {entry['url']}: {e}")
        except Exception as e:
            print(f"[!] Failed to load catalog page {catalog_url}: {e}")

    with open("shl_product_data.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print("✅ Scraping complete! Data saved to shl_product_data.json")


if __name__ == "__main__":
    main()
