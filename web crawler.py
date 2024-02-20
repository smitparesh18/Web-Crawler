import requests
from bs4 import BeautifulSoup
import re

def get_links_and_info(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
            contact_numbers = re.findall(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b', response.text)
            return links, email_addresses, contact_numbers
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
    return [], [], []

def crawl_and_extract_info(starting_url, depth=2):
    visited_links = set()
    links_to_visit = [(starting_url, 0)]
    all_links = set()
    all_emails = set()
    all_contact_numbers = set()

    while links_to_visit:
        current_url, current_depth = links_to_visit.pop(0)

        if current_url in visited_links or current_depth > depth:
            continue

        visited_links.add(current_url)
        print(f"Crawling {current_url}")

        links_on_page, email_addresses, contact_numbers = get_links_and_info(current_url)
        all_links.update(links_on_page)
        all_emails.update(email_addresses)
        all_contact_numbers.update(contact_numbers)

        for link in links_on_page:
            if link.startswith('http'):
                links_to_visit.append((link, current_depth + 1))

    return all_links, all_emails, all_contact_numbers

def write_output_to_file(filename, links, emails, contact_numbers):
    with open(filename, 'w') as f:
        f.write("Links:\n")
        for link in links:
            f.write(link + '\n')

        f.write("\nEmail Addresses:\n")
        for email in emails:
            f.write(email + '\n')

        f.write("\nContact Numbers:\n")
        for number in contact_numbers:
            f.write(number + '\n')

if __name__ == "__main__":
    starting_url = "http://testphp.vulnweb.com/"  # Replace with the target website URL
    depth = 2  # Set the desired depth of crawling

    links, emails, contact_numbers = crawl_and_extract_info(starting_url, depth)

    output_filename = "recon_results.txt"
    write_output_to_file(output_filename, links, emails, contact_numbers)

    print(f"Results exported to {output_filename}")
