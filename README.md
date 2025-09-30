# Phone Validator API

A Flask-based API for validating, normalizing, and processing phone numbers using the `phonenumbers` library.

## Endpoints

### GET /health

Health check endpoint.

**Response:**

```json
{
    "status": "healthy"
}
```

### POST /validate

Validates and processes a phone number with an optional country code.

**Request Body:**

```json
{
    "phone_number": "string",
    "country_code": "string (optional, e.g., 'US', 'CR')"
}
```

**Response:**

```json
{
    "is_valid": true,
    "is_possible": true,
    "country_code": 1,
    "country_code_alpha2": "US",
    "national_number": 1234567890,
    "formats": {
        "international": "+1 234-567-890",
        "national": "(234) 567-890",
        "e164": "+1234567890"
    },
    "location": "United States",
    "carrier": "T-Mobile",
    "timezones": ["America/New_York"]
}
```

### POST /normalize

Normalizes a phone number to a specified format.

**Request Body:**

```json
{
    "phone_number": "string",
    "country_code": "string (optional)",
    "format": "E164 | INTERNATIONAL | NATIONAL (default: E164)"
}
```

**Response:**

```json
{
    "original": "1234567890",
    "normalized": "+1234567890",
    "format": "E164"
}
```

### POST /phone-number

Processes a phone number by attempting to infer the country code from the number itself. Suitable for international numbers with + prefix.

**Request Body:**

```json
{
    "phone_number": "string"
}
```

**Response:** Same as `/validate` if successful.

**Error Response (if country code cannot be inferred):**

```json
{
    "error": "Unable to parse phone number without country code. Please provide a country code or use international format (+countrycode...)."
}
```

## Installation

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    python app.py
    ```

The API will be available at `http://localhost:5000`.

## Docker

Build and run with Docker:

```bash
docker build -t phone-validator-api .
docker run -p 5000:5000 phone-validator-api
```

## Usage Examples

### Validate with country code

```bash
curl -X POST http://localhost:5000/validate \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "234567890", "country_code": "US"}'
```

### Process phone number (infer country)

```bash
curl -X POST http://localhost:5000/phone-number \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+50612345678"}'
```
