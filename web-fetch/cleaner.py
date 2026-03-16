from bs4 import BeautifulSoup

def clean_text(html: str) -> str:
    """
    Strip scripts, styles, navigation, footer, header and aside tags
    and return a single‑line clean text string.
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in ["script", "style", "nav", "footer", "header", "aside"]:
        for match in soup.find_all(tag):
            match.decompose()
    text = soup.get_text(separator=" ")
    return " ".join(text.split())