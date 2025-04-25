from bs4 import BeautifulSoup

def extract_fields(html: str) -> dict:
    """Fallback extractor if LLM fails."""
    soup = BeautifulSoup(html, 'html.parser')
    name = (soup.find('h1') or soup.find('title'))
    contact = soup.find(string=lambda s: s and ('contact' in s.lower() or 'phone' in s.lower()))
    address = soup.find(string=lambda s: s and 'address' in s.lower())
    hours = soup.find(string=lambda s: s and ('hours' in s.lower() or 'open' in s.lower()))

    menu_items = []
    sections = soup.find_all(['ul','div','table'], string=lambda s: s and 'menu' in s.lower())
    for sec in sections:
        for item in sec.find_all(['li','td']):
            text = item.get_text(strip=True)
            if text:
                menu_items.append({'item': text, 'price': '', 'desc': ''})

    return {
        'name': name.get_text(strip=True) if name else '',
        'location': '',
        'menu': menu_items,
        'features': [],
        'hours': hours.strip() if hours else '',
        'contact': contact.strip() if contact else '',
        'address': address.strip() if address else ''
    }