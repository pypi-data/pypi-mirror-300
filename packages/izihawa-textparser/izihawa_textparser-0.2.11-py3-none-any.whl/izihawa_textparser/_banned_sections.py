import re

BANNED_SECTION_PREFIXES = [
    "bibliography of",
    "\\d+ index\\s*$"
]
_BANNED_SECTION_PREFIXES_REGEXP_PART = "|".join(BANNED_SECTION_PREFIXES)
BANNED_SECTION_PREFIXES_REGEXP = re.compile(rf"^({_BANNED_SECTION_PREFIXES_REGEXP_PART})", flags=re.IGNORECASE)

BANNED_SECTIONS = {
    "contents",
    "index",
    "table of content",
    "author contribution",
    "data availability statement",
    "data availability",
    "declaration of competing interest",
    "declarations",
    "disclosure",
    "acknowledgment",
    "acknowledgments",
    "acknowledgements",
    "supporting information",
    "conflict of interest disclosures",
    "conflict of interest",
    "conflict of interest statement",
    "ethics statement",
    "references",
    "external links",
    "further reading",
    "works cited",
    "bibliography",
    "notes",
    "sources",
    "footnotes",
    "suggested readings",
    "academic journal articles",
    "academic books",
    "table of contents",
    "keywords",
    "full citations can be found in the bibliography",
    "supplementary information",
    "содержание",
    "список литературы",
    "источники",
    "ссылки",
    "благодарность",
    "благодарности",
    "литература",
    "оглавление",
    "примечания",
    "обратная связь",
    "сборники документов",
    "рекомендуемая литература",
}

SECTIONS_MAPS = {
    "authors": "Authors",
    "abstract": "Abstract",
    "date": "Date",
    "acknowledgements": "Acknowledgements",
    "introduction": "Introduction",
    "materials and methods": "Methods",
    "methods": "Methods",
    "results": "Results",
    "conclusions": "Conclusions",
    "conclusions and future applications": "Conclusions",
    "discussion": "Discussion",
    "tables": "Tables",
    "tabnles": "Tables",
    "disclosure": "Disclosure",
    "conflict of interest": "Disclosure",
    "declaration of conflicting interests": "Disclosure",
    "acknowledgement": "Acknowledgements",
    "acknowledgments": "Acknowledgements",
    "conflictofintereststatement": "Disclosure",
    "funding": "Funding",
    "fundinginformation": "Funding",
    "biographies": "Biographies",
    "disclaimer": "Disclosure",
    "referencesfigure": "References Figure",
    "declaration of competing interest": "Disclosure",
    "conflict of interest disclosures": "Disclosure",
    "conflict of interest statement": "Disclosure",
    "authors' contributions": "Author Contribution",
}


def is_banned_section(text: str):
    text = text.lower()
    stripped_text = re.sub(r"^\d+\s*\.\s*", "", text).strip()
    return (
        text in BANNED_SECTIONS
        or stripped_text in BANNED_SECTIONS
        or BANNED_SECTION_PREFIXES_REGEXP.match(text)
        or BANNED_SECTION_PREFIXES_REGEXP.match(stripped_text)
    )
