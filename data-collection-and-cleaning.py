import requests
from bs4 import BeautifulSoup
import re
import os

# List of loan products with their URLs and key info highlights
loan_products = [
    {
        "Loan Type": "Home Loan",
        "URL": "https://bankofmaharashtra.in/personal-banking/loans/home-loan",
        "Key Info Highlights": "Interest rate, tenure, concessions, prepayment info"
    },
    {
        "Loan Type": "Flexi Housing Loan",
        "URL": "https://bankofmaharashtra.in/maha-super-flexi-housing-loan-scheme",
        "Key Info Highlights": "Flexi savings-linked structure"
    },
    {
        "Loan Type": "Top-Up Home Loan",
        "URL": "https://bankofmaharashtra.in/topup-home-loan",
        "Key Info Highlights": "Loan amount, processing fee, eligibility"
    },
    {
        "Loan Type": "Education Loan",
        "URL": "https://bankofmaharashtra.in/educational-loans",
        "Key Info Highlights": "Concession, tenure, collateral policy"
    },
    {
        "Loan Type": "Model Education Loan",
        "URL": "https://bankofmaharashtra.in/model-education-loan-scheme",
        "Key Info Highlights": "Loan ceilings, margins, repayment terms"
    },
    {
        "Loan Type": "Personal Loan",
        "URL": "https://bankofmaharashtra.in/personal-banking/loans/personal-loan",
        "Key Info Highlights": "Interest rate, tenure, eligibility"
    }
]


# Function to scrape data from a URL
def scrape_webpage(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove irrelevant elements (scripts, styles, navigation, footer)
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.extract()

        # Extract text from relevant sections (e.g., main content)
        main_content = soup.find('main') or soup.find('div', class_=re.compile('content|main|loan'))
        text = main_content.get_text(separator=' ') if main_content else soup.get_text(separator=' ')

        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""


# Function to clean extracted text
def clean_text(text):
    if not text:
        return ""

    # Remove excessive whitespace and newlines
    text = re.sub(r'\s+', ' ', text)

    # Remove non-printable characters
    text = ''.join(c for c in text if c.isprintable())

    # Remove common navigation/footer keywords
    text = re.sub(
        r'(Home|About Us|Locate Us|Careers|Contact Us|Menu|Login|Apply Now|Know More|Accessibility|Cookies Policy|Disclaimer|Sitemap)',
        '', text, flags=re.IGNORECASE)

    # Remove redundant SEO phrases (e.g., repeated "Bank of Maharashtra")
    text = re.sub(r'(Bank of Maharashtra\s*)+', 'Bank of Maharashtra ', text)

    return text.strip()


# Function to consolidate and save data to a text file
def save_to_txt(data, filename="bom_loan_products.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Bank of Maharashtra Loan Products\n\n")
            for item in data:
                file.write(f"{item['Loan Type']}\n")
                file.write(f"URL: {item['URL']}\n")
                file.write(f"Key Info Highlights: {item['Key Info Highlights']}\n")
                file.write(f"Details: {item['Cleaned Text']}\n\n")
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")


# Main execution
if __name__ == "__main__":
    consolidated_data = []

    for loan in loan_products:
        print(f"Scraping {loan['Loan Type']} from {loan['URL']}...")
        raw_text = scrape_webpage(loan['URL'])
        cleaned_text = clean_text(raw_text)

        consolidated_data.append({
            "Loan Type": loan['Loan Type'],
            "URL": loan['URL'],
            "Key Info Highlights": loan['Key Info Highlights'],
            "Cleaned Text": cleaned_text if cleaned_text else "Data not available due to scraping limitations."
        })

    # Save consolidated data to a text file
    save_to_txt(consolidated_data)