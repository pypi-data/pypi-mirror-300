import requests
from requests.auth import HTTPBasicAuth
import base64
import json
import os

from .aurora_signature.sign import signers, timestamps
from .aurora_signature.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from .aurora_certvalidator import ValidationContext
from .aurora_signature.keys import decrypt_data
from .aurora_signature.pdf_utils.format import format_date

def pplg_request(api_token, tenant_id, cert_type):
    url = 'http://127.0.0.1:5000/api/openapi/sdk-sign-info.json'
    params = {
        'tenant_id': tenant_id,
        'cert_type': cert_type
    }
    headers = {
        'X-Paperlogic-Authorization': api_token,
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return True, data['result']
    else:
        print("Error:", response.status_code, response.text)
        return False, response.text


def sign(input_file, output_file, api_token, tenant_id, cert_type = 0):
    print('Starting sign...')
    
    cert_file_pem = 'certificate.pem'
    private_key_pem = 'private_key.pem'
    try:
        res_check, res_data = pplg_request(api_token, tenant_id, cert_type)

        cert_bytes = base64.b64decode(res_data['_c'])
        private_key_bytes = decrypt_data(res_data['_k'], api_token)
        
        # cms_signer = signers.SimpleSigner.load_bytes(private_key_bytes, cert_bytes)

        

        with open(cert_file_pem, 'wb') as f:
            f.write(cert_bytes)

        with open(private_key_pem, 'wb') as f:
            f.write(private_key_bytes)

        cms_signer = signers.SimpleSigner.load(private_key_pem, cert_file_pem)

        timestamp_info = json.loads(decrypt_data(res_data['_t'], api_token).decode('utf-8'))
        tst_client = timestamps.HTTPTimeStamper(
            timestamp_info['ts_url'], auth=HTTPBasicAuth(timestamp_info['ts_username'], timestamp_info['ts_password'])
        )

        vc = ValidationContext(
            allow_fetching=True
        )

        pdf_buffer = open(input_file, 'rb')
        w = IncrementalPdfFileWriter(pdf_buffer)

        sig_field_name = 'Signature1'
        user_info = res_data['user_info']
        formatted_datetime_str = format_date()
        reason = [
            'Date Time: %s' % formatted_datetime_str,
            'Signer Name: %s' % user_info['user_full_name'],
            'Company Name: %s' % user_info['user_company_name'],
            'Division: %s' % (user_info['division'] if user_info['division'] is not None else ''),
            'Email: %s' % user_info['user_email'],
        ]
        reason_text = ', '.join(reason)
        signature_metadata = signers.PdfSignatureMetadata(
            field_name=sig_field_name,
            reason=reason_text,
            embed_validation_info=True,
            validation_context=vc
        )

        with open(output_file, 'wb') as outf:
            signers.sign_pdf(
                w, 
                signature_metadata,
                signer=cms_signer, 
                # timestamper=tst_client,
                output=outf
            )
    except Exception as ex:
        print('Exception', ex)

    finally:
        print('done')
        if os.path.exists(cert_file_pem):
            os.remove(cert_file_pem)
        if os.path.exists(private_key_pem):
            os.remove(private_key_pem)