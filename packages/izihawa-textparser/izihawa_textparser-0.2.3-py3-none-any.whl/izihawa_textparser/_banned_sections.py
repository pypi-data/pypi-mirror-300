import re

BANNED_SECTION_PREFIXES = [
    "bibliography of",
    "\d+ index\s*$"
]
_BANNED_SECTION_PREFIXES_REGEXP_PART = "|".join(BANNED_SECTION_PREFIXES)


BANNED_SECTIONS = {
    "contents",
    "index",
    "table of content",
    "author contribution",
    "data availability statement",
    "data availability",
    "declaration of competing interest",
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
    "Authors": "Authors",
    "AUTHORS": "Authors",
    "Abstract": "Abstract",
    "ABSTRACT": "Abstract",
    "Date": "Date",
    "DATE": "Date",
    "acknowledgements": "Acknowledgements",
    "INTRODUCTION": "Introduction",
    "MATERIALS AND METHODS": "Methods",
    "Materials and methods": "Methods",
    "METHODS": "Methods",
    "RESULTS": "Results",
    "CONCLUSIONS": "Conclusions",
    "CONCLUSIONS AND FUTURE APPLICATIONS": "Conclusions",
    "DISCUSSION": "Discussion",
    "ACKNOWLEDGMENTS": "Acknowledgements",
    "TABLES": "Tables",
    "Tabnles": "Tables",
    "DISCLOSURE": "Disclosure",
    "CONFLICT OF INTEREST": "Disclosure",
    "Declaration of conflicting interests": "Disclosure",
    "Declaration of competing interest": "Disclosure",
    "Acknowledgement": "Acknowledgements",
    "Acknowledgments": "Acknowledgements",
    "conflictofintereststatement": "Disclosure",
    "FUNDING": "Funding",
    "fundinginformation": "Funding",
    "BIOGRAPHIES": "Biographies",
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
