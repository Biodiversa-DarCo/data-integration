import re


def parse_article(verbatim: str | None):
    if verbatim is None:
        return None
    regex = re.compile(r"^([^\d(]+)\s*\(?(\d{4})([\/\-]?\d{4})?\)?\.?")
    match = regex.match(verbatim)
    if match:
        authors = match.group(1).strip()
        year = match.group(2).strip()
        return {
            "authors": re.split(r"(?:, ?|(?<=\.) (?=[A-Za-z]{2,}))", authors),
            "year": int(year),
            "verbatim": verbatim,
        }
    else:
        return None
