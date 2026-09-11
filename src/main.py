import re 
import json
import os

email_validate_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
email_extra_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{2,}"
card_pattern = r"\b(?:\d{4}[- ]?){3}\d{4}\b"
phone_pattern = r"\+250(?:[- ]?\d{3}){3}"
url_pattern = r"https?://[a-zA-Z0-9.-]+(?:/[^\s()<>\[\]\"']*)?"

MAX_FILE_SIZE = 5 * 1024 *1024
def is_suspicious(value):
    "reject valuees containing script tags or javascript"
    return bool(re.search(r"<\s*script|javascript\s*:|[<>]",value,re.IGNORECASE))
#----------------
# email handling
#---------------

def validate_email(email):
    "return true if email full matches the email pattern"
    return bool(re.fullmatch(email_validate_pattern,email))

def classify_alu_email(email):
    "classify an ALU related email by its domain"
    domain= email.split("@",1) [1].lower()

    if domain =="alumni.alueducation.com":
        return "alumni"
    if domain =="si.alueducation.com":
        return "si"
    if domain =="alueducation.com":
        return "official"
    return "non-official"

def masked_email(email):
    "mask the email username while keeping the first character visible"
    username, domain = email.split("@",1)
    return username[0]+ "*" * (len(username) -1) +"@" + domain

def process_email(email):
    "validate,classify and mask the email candidate"
    if  is_suspicious(email) or not validate_email(email):
        return None
    return {
        "data":masked_email(email),
        "type":"email",
        "valid":True,
        "group":classify_alu_email(email)
    }

#-----------------
# credit card handling
#-----------------

def normalize_card(card):
    "remove spaces and dashes from a card number"
    return re.sub (r"[- ]", "",card)

def luhn_check(card):
    "return true if card passes luhn checksum"
    total =0
    for i, digit in enumerate(card[::-1]):
        n = int(digit)
        if i%2:
            n*=2 
            if n>9:
                n-=9
        total +=n
    return total %10 ==0

def validate_card(card):
    "return true if a normalized card number is 16 digits and passes luhn"
    card = normalize_card(card)
    return len(card) ==16 and card.isdigit() and luhn_check(card)

def process_card(card):
    "validate and mask the candidate card number"
    if not validate_card(card):
        return None 
    card = normalize_card(card)
    return {
        "data":"*" * 12 + card[-4:],
        "type":"credit card",
        "valid": True
    }

#--------------------------
#phone number handling
# #-------------------------
#  
def normalize_phone(phone):
    "remove spaces and dashes form phone number"
    return re.sub(r"[- ]", "",phone)

def process_phone(phone):
    "validate and mask rwandan phone number"
    phone =normalize_phone(phone)
    if not re.fullmatch(r"\+250\d{9}",phone):
        return None 
    return {
        "data":phone[:4]+"******"+phone[-3:],
        "type":"phonenumber",
        "valid":True
    }

#---------------------------
#url handling 
#---------------------------

def process_url(url):
    "validate a candidate url"
    if is_suspicious(url) or not re.fullmatch(url_pattern,url):
        return None 
    return {
        "data":url,
        "type":"url",
        "valid":True
    }

#---------------------------
#file i/o helper
#---------------------------
"read the input file safely"
try:
    if os.path.getsize("input/raw-text.txt") > MAX_FILE_SIZE:
        raise ValueError("input file too large")
    with open ("input/raw-text.txt", encoding="utf-8") as file:
        text =file.read()
except (FileNotFoundError, ValueError) as error:
    print(f"error reading input file:{error}")
    text = ""

#---------------------------
#main extraction pipeline
#----------------------------
"find and process all supported data type"

patterns =[
    (email_extra_pattern, process_email),
    (card_pattern, process_card),
    (phone_pattern, process_phone),
    (url_pattern, process_url)
]
candidates =[]

for pattern, processor in patterns:
    for match in re.finditer(pattern, text):
        candidates.append((match.start(), match.group(), processor))
candidates.sort(key=lambda c: c[0])

results =[]

for _, value, processor in candidates:
        result = processor(value)
        if result:
            results.append(result)

os.makedirs("output", exist_ok=True)
with open ("output/sample-output.json", "w", encoding="utf-8") as file:
    json.dump(results,file,indent=2)

print("extraction completed successfully")
print("results saved to output/sample-output.json")
