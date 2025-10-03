import re
import pdfplumber
import docx
import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load('en_core_web_sm')
SKILLS = [
    'python', 'java', 'c++', 'sql', 'docker', 'kubernetes', 'aws', 'flask', 'django', 'react', 'node.js'
]
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
matcher.add('SKILLS', [nlp.make_doc(s) for s in SKILLS])
EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_RE = re.compile(r'(?:(?:\+?\d{1,3})?[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}')
EXP_RE = re.compile(r'(\d+(?:\.\d+)?)\s+years?')
EDU_RE = re.compile(
    r"(B\.?[A-Za-z]{1,4}|M\.?[A-Za-z]{1,4}|Bachelor|Master|Bachelors|MBA|B\.Tech|M\.Tech)",
    re.I
)

def extract_text_from_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text)

def parse_resume(path):
    # choose extractor by file extension (or use python-magic)
    if path.lower().endswith('.pdf'):
        raw = extract_text_from_pdf(path)
    else:
        raw = extract_text_from_docx(path)
    doc = nlp(raw[:10000])  # run on a slice first for speed to get name/entity hints

    # email, phone
    email = EMAIL_RE.search(raw)
    phone = PHONE_RE.search(raw)
    email = email.group(0) if email else None
    phone = phone.group(0) if phone else None

    # name heuristic: first PERSON entity in the first 120 tokens
    name = None
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            name = ent.text.strip()
            break

    # experience
    exps = [float(m.group(1)) for m in EXP_RE.finditer(raw.lower())]
    experience_years = max(exps) if exps else None

    # education
    edus = set(m.group(0) for m in EDU_RE.finditer(raw))

    # skills via PhraseMatcher
    doc2 = nlp(raw)
    matches = matcher(doc2)
    skills = sorted({doc2[start:end].text.strip().lower() for _, start, end in matches})

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'education': list(edus),
        'skills': skills,
        'experience_years': experience_years,
        'full_text': raw
    }
 