import re
import json


# The quick brown fox jumps over the lazy dog


# ==========================================
# EMAIL
# ==========================================

EMAIL_PATTERN = (
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


def validate_email(email):
    """Check whether an email has a valid format."""
    return bool(re.fullmatch(EMAIL_PATTERN, email))


def classify_alu_email(email):
    """Classify an email according to its ALU domain."""
    domain = email.split("@", 1)[1].lower()

    if domain == "alumni.alueducation.com":
        return "alumni"
    elif domain == "si.alueducation.com":
        return "si"
    elif domain == "alueducation.com":
        return "official"
    else:
        return "non-ALU"


def mask_email(email):
    """Hide most of the username of an email."""
    username, domain = email.split("@", 1)

    if len(username) <= 1:
        masked_username = "*"
    else:
        masked_username = (
            username[0] + "*" * (len(username) - 1)
        )

    return masked_username + "@" + domain


def process_email(email):
    """Validate, classify, and mask an email."""
    if not validate_email(email):
        return None

    return {
        "value": mask_email(email),
        "type": "email",
        "valid": True,
        "category": classify_alu_email(email)
    }


# ==========================================
# CREDIT CARD
# ==========================================

CARD_PATTERN = r"\b(?:\d{4}[- ]?){3}\d{4}\b"


def normalize_card(card):
    """Remove spaces and hyphens from a card number."""
    return re.sub(r"[- ]", "", card)


def luhn_check(card):
    """Validate a card number using the Luhn algorithm."""
    total = 0
    reverse_digits = card[::-1]

    for position, digit in enumerate(reverse_digits):
        number = int(digit)

        if position % 2 == 1:
            number *= 2

            if number > 9:
                number -= 9

        total += number

    return total % 10 == 0


def validate_card(card):
    """Check card length and Luhn validity."""
    normalized = normalize_card(card)

    if len(normalized) != 16 or not normalized.isdigit():
        return False

    return luhn_check(normalized)


def mask_card(card):
    """Hide all but the last four digits."""
    normalized = normalize_card(card)

    return "*" * 12 + normalized[-4:]


def process_card(card):
    """Validate and safely process a card number."""
    if not validate_card(card):
        return None

    return {
        "value": mask_card(card),
        "type": "credit_card",
        "valid": True
    }


# ==========================================
# PHONE NUMBER
# ==========================================

PHONE_PATTERN = r"\+250(?:[- ]?\d{3}){3}"


def normalize_phone(phone):
    """Remove spaces and hyphens from a phone number."""
    return re.sub(r"[- ]", "", phone)


def validate_phone(phone):
    """Validate a Rwandan phone number."""
    normalized = normalize_phone(phone)

    return bool(
        re.fullmatch(r"\+250\d{9}", normalized)
    )


def mask_phone(phone):
    """Hide the middle digits of a phone number."""
    normalized = normalize_phone(phone)

    return normalized[:4] + "******" + normalized[-3:]


def process_phone(phone):
    """Validate and safely process a phone number."""
    if not validate_phone(phone):
        return None

    return {
        "value": mask_phone(phone),
        "type": "phone",
        "valid": True
    }


# ==========================================
# URL
# ==========================================

URL_PATTERN = (
    r"https?://[a-zA-Z0-9.-]+(?:/[^\s]*)?"
)


def validate_url(url):
    """Validate an HTTP or HTTPS URL."""
    pattern = (
        r"^https?://[a-zA-Z0-9.-]+(?:/[^\s]*)?$"
    )

    return bool(re.fullmatch(pattern, url))


def process_url(url):
    """Validate and process a URL."""
    if not validate_url(url):
        return None

    return {
        "value": url,
        "type": "url",
        "valid": True
    }


# ==========================================
# READ INPUT FILE
# ==========================================

with open(
    "input/raw-text.txt",
    "r",
    encoding="utf-8"
) as file:
    text = file.read()


# ==========================================
# EXTRACT EMAILS
# ==========================================

email_candidates = re.findall(
    r"\S+@\S+\.\S+",
    text
)

email_results = []

for email in email_candidates:
    result = process_email(email)

    if result is not None:
        email_results.append(result)


# ==========================================
# EXTRACT CREDIT CARDS
# ==========================================

card_candidates = re.findall(
    CARD_PATTERN,
    text
)

card_results = []

for card in card_candidates:
    result = process_card(card)

    if result is not None:
        card_results.append(result)


# ==========================================
# EXTRACT PHONE NUMBERS
# ==========================================

phone_candidates = re.findall(
    PHONE_PATTERN,
    text
)

phone_results = []

for phone in phone_candidates:
    result = process_phone(phone)

    if result is not None:
        phone_results.append(result)


# ==========================================
# EXTRACT URLS
# ==========================================

url_candidates = re.findall(
    URL_PATTERN,
    text
)

url_results = []

for url in url_candidates:
    result = process_url(url)

    if result is not None:
        url_results.append(result)


# ==========================================
# COMBINE ALL RESULTS
# ==========================================

all_results = []

all_results.extend(email_results)
all_results.extend(card_results)
all_results.extend(phone_results)
all_results.extend(url_results)


# ==========================================
# SAVE RESULTS AS JSON
# ==========================================

with open(
    "output/sample-output.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        all_results,
        file,
        indent=2
    )


print("Extraction completed successfully.")
print(
    "Results saved to output/sample-output.json"
)
