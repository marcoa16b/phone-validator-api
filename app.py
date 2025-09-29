from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from phonenumbers.phonenumberutil import NumberParseException

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/validate', methods=['POST'])
def validate_phone():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        country_code = data.get('country_code', None)  # Opcional, ej: 'BE', 'NL', 'FR'
        
        if not phone_number:
            return jsonify({"error": "phone_number is required"}), 400
        
        # Parsear el número
        parsed_number = phonenumbers.parse(phone_number, country_code)
        
        # Validar
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        # Normalizar
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        # Información adicional
        country = geocoder.description_for_number(parsed_number, "es")
        carrier_name = carrier.name_for_number(parsed_number, "es")
        timezones = timezone.time_zones_for_number(parsed_number)
        
        return jsonify({
            "is_valid": is_valid,
            "is_possible": is_possible,
            "country_code": parsed_number.country_code,
            "national_number": parsed_number.national_number,
            "formats": {
                "international": international_format,
                "national": national_format,
                "e164": e164_format
            },
            "location": country,
            "carrier": carrier_name,
            "timezones": list(timezones)
        })
        
    except NumberParseException as e:
        return jsonify({"error": f"Invalid phone number: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/normalize', methods=['POST'])
def normalize_phone():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        country_code = data.get('country_code', None)
        format_type = data.get('format', 'E164').upper()
        
        if not phone_number:
            return jsonify({"error": "phone_number is required"}), 400
        
        parsed_number = phonenumbers.parse(phone_number, country_code)

        if not phonenumbers.is_possible_number(parsed_number):
            return jsonify({"error": "Invalid phone number"}), 400
        
        format_map = {
            'E164': phonenumbers.PhoneNumberFormat.E164,
            'INTERNATIONAL': phonenumbers.PhoneNumberFormat.INTERNATIONAL,
            'NATIONAL': phonenumbers.PhoneNumberFormat.NATIONAL
        }
        
        formatted_number = phonenumbers.format_number(
            parsed_number, 
            format_map.get(format_type, phonenumbers.PhoneNumberFormat.E164)
        )
        
        return jsonify({
            "original": phone_number,
            "normalized": formatted_number,
            "format": format_type
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)