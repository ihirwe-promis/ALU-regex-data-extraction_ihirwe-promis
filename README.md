# ALU Regex Data Extraction

## Project Description

This project extracts structured information from messy, untrusted text using Python regular expressions. The program identifies valid email addresses, credit card numbers, Rwandan phone numbers, and URLs.

Sensitive information is validated and masked before being written to the output file.

## Data Types Extracted

The program extracts four types of data:

1. **Email addresses**
2. **Credit card numbers**
3. **Rwandan phone numbers**
4. **URLs**

### Email Classification

ALU email addresses are classified into three categories:

* `@alueducation.com` → official
* `@alumni.alueducation.com` → alumni
* `@si.alueducation.com` → si

Emails from other domains are classified as `non-ALU`.

## Validation

The program uses regular expressions to identify candidate values and validation functions to reject malformed data.

Credit card numbers are additionally checked using the **Luhn algorithm**.

Phone numbers are validated as Rwandan numbers using the `+250` country code and nine following digits.

URLs are restricted to HTTP and HTTPS schemes.

## Security and Privacy

The input data is treated as untrusted.

Sensitive information is not stored in its original form in the output:

* Email addresses are partially masked.
* Credit card numbers are masked except for the last four digits.
* Phone numbers are partially masked.

Invalid or malformed values are rejected instead of being included in the output.

The project uses only fake test data and does not require real personal or payment information.

## Project Structure

```text
ALU-regex-data-extraction_ihirwe-promis/
├── input/
│   └── raw-text.txt
├── src/
│   └── main.py
├── output/
│   └── sample-output.json
└── README.md
```

## How to Run

Make sure you are in the project root directory:

```bash
cd ALU-regex-data-extraction_ihirwe-promis
```

Run the program with:

```bash
python3 src/main.py
```

The extracted and validated results are saved to:

```text
output/sample-output.json
```

## Technologies Used

* Python 3
* Regular Expressions (`re`)
* JSON (`json`)
* GitHub

