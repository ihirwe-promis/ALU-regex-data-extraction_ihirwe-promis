import re 
import json

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
card_pattern = r"\b(?:\d{4}[- ]?){3}\d{4}\b"
phone_pattern = r"\+250(?:[- ]?\d{3}){3}"
url_pattern = r"https?://[a-zA-Z0-9.-]+(?:/[^\s]*)?"

def validate_email(email):
    return bool(re.fullmatch(email_pattern,email))

def classify_alu_email(email):
    domain= email.split("@",1) [1].lower()

    if domain =="alumni.alueducation.com":
        return "alumni"
    if domain =="si.alueducation.com":
        return "si"
    if domain =="alueducation.com":
        return "official"
    return "non-official"

def masked_email(email):
    username, domain = email.split("@",1)
    return username[0]+ "*" * (len(username) -1) +"@" + domain

def process_email(email):
    if not validate_email(email):
        return None
    return {
        "data":masked_email(email),
        "type":"email",
        "valid":True,
        "group":classify_alu_email(email)
    }

def normalize_card(card):
    return re.sub (r"[- ]", "",card)

def luhn_check(card):
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
    card = normalize_card(card)
    return len(card) ==16 and card.isdigit() and luhn_check(card)

def process_card(card):
    if not validate_card(card):
        return None 
    card = normalize_card(card)
    return {
        "data":"*" * 12 + card[-4:],
        "type":"credit card",
        "valid": True
    }

def normalize_phone(phone):
    return re.sub(r"[- ]", "",phone)

def process_phone(phone):
    phone =normalize_phone(phone)
    if not re.fullmatch(r"\+250\d{9}",phone):
        return None 
    return {
        "data":phone[:4]+"******"+phone[-3:],
        "type":"phonenumber",
        "valid":True
    }

def process_url(url):
    if not re.fullmatch(url_pattern,url):
        return None 
    return {
        "data":url,
        "type":"url",
        "valid":True
    }

with open ("input/raw-text.txt", encoding="utf-8") as file:
    text =file.read()

patterns =[
    (r"\S+@\S+\.\S+", process_email),
    (card_pattern, process_card),
    (phone_pattern, process_phone),
    (url_pattern, process_url)
]
results =[]

for pattern, processor in patterns:
    for value in re.findall(pattern, text):
        result = processor(value)
        if result:
            results.append(result)

with open ("output/sample-output.json", "w", encoding="utf-8") as file:
    json.dump(results,file,indent=2)

print("extraction completed successfully")
print("results saved to output/sample-output.json")
