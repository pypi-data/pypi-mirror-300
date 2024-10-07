import re
import os
import logging
import tempfile
import plistlib
import requests
import subprocess
import contextlib
from datetime import datetime
from cryptography import x509
from .errors import InvalidCertificateError
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization, hashes
from .entitlements import entitlements_mapping, revocation_reason_mapping
from .country_flags import country_flags

logger = logging.getLogger(__name__)

def format_datetime(date_str):
    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%d %B %Y, %I:%M %p (UTC)")

def get_country_flag(country_code):
    return country_flags.get(country_code, '🏳️')

class Checker:
    APPLE_ISSUER_CERT_URL = 'https://www.apple.com/certificateauthority/AppleWWDRCAG3.cer'
    _last_checked: datetime = None
    _default_cert_chain = b''

    @property
    def path(self) -> str:
        path = os.path.join(os.getcwd(), "temp_certs")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @property
    def default_cert_chain(self) -> bytes:
        cls = self.__class__
        if not cls._default_cert_chain or (datetime.now() - cls._last_checked).total_seconds() > 60 * 60 * 2: 
            cls._default_cert_chain = requests.get(cls.APPLE_ISSUER_CERT_URL).content
            cls._last_checked = datetime.now()
        return cls._default_cert_chain

    def get_ocsp_url(self, cert: x509.Certificate) -> str:
        with contextlib.suppress(x509.ExtensionNotFound):
            aia = cert.extensions.get_extension_for_class(x509.AuthorityInformationAccess)
            for desc in aia.value:
                if desc.access_method == x509.OID_OCSP:
                    return desc.access_location.value
        return None

    def get_revocation_reason_description(self, reason_code: str) -> str:
        return revocation_reason_mapping.get(reason_code, "Unknown reason")

    def extract_cert_from_p12(self, p12_data: bytes, password: str = "") -> tuple:
        p12 = pkcs12.load_key_and_certificates(p12_data, password.encode('utf-8'))
        if p12 is None:
            raise ValueError("Incorrect password or unable to load the p12 file.")
        return p12[1], p12[2]

    def process_name(self, name):
        value = name.value
        return {"original": value, "truncated": value[:61] + "..."} if len(value) > 64 else value
    
    def get_certificate_info(self, cert):
        subject_details = {name.oid._name: self.process_name(name) for name in cert.subject}
        issuer_details = {name.oid._name: self.process_name(name) for name in cert.issuer}
    
        country_code = subject_details.get("countryName")
        country_flag = get_country_flag(country_code) if country_code else '🏳️'
    
        subject_details["countryFlag"] = country_flag
    
        cert_info = {
            "subject": {k: v["truncated"] if isinstance(v, dict) else v for k, v in subject_details.items()},
            "issuer": {k: v["truncated"] if isinstance(v, dict) else v for k, v in issuer_details.items()},
            "serial_number": str(cert.serial_number),
            "signature_algorithm": cert.signature_algorithm_oid._name,
            "validity_period": {
                "valid_from": format_datetime(cert.not_valid_before_utc.isoformat()),
                "valid_to": format_datetime(cert.not_valid_after_utc.isoformat())
            },
            "public_key_size": cert.public_key().key_size,
            "fingerprints": {
                "sha256": cert.fingerprint(hashes.SHA256()).hex(),
                "md5": cert.fingerprint(hashes.MD5()).hex(),
                "sha1": cert.fingerprint(hashes.SHA1()).hex(),
            },
            "ocsp_url": self.get_ocsp_url(cert),
            "public_key_algorithm": cert.public_bytes(
                encoding=serialization.Encoding.PEM
            ).decode('utf-8'),
        }
    
        return cert_info
    
    def create_cert_files(self, cert: x509.Certificate, cert_chain: list = None):
        p12_cert = cert.public_bytes(serialization.Encoding.PEM)
        if cert_chain and cert_chain[0]:
            full_chain_cert = cert_chain[0].public_bytes(serialization.Encoding.PEM)
        else:
            full_chain_cert = self.default_cert_chain
        return p12_cert, full_chain_cert
    
    def _ocsp_check_with_openssl(self, cert_data: bytes, issuer_data: bytes, ocsp_url: str) -> dict:
        try:
            with tempfile.TemporaryDirectory(dir=self.path) as temp_dir:
                with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as cert_file, \
                     tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as issuer_file:
                    
                    cert_file.write(cert_data)
                    issuer_file.write(issuer_data)
                    cert_file.flush()
                    issuer_file.flush()
                    
                    cert_file_path = cert_file.name
                    issuer_file_path = issuer_file.name
                    
                    result = subprocess.run(
                        ['openssl', 'ocsp', '-issuer', issuer_file_path, '-cert', cert_file_path, '-url', ocsp_url, '-noverify', '-resp_text'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    output = result.stdout
                    ocsp_status = {"status": "Unknown"}
            
                    if "revoked" in output:
                        ocsp_status["status"] = "Revoked"
                        ocsp_status["revocation_time"] = re.search(r'Revocation Time: (.+)', output).group(1) or "Unknown"
                        reason_match = re.search(r'Reason: (.+)', output)
                        ocsp_status["reason"] = reason_match.group(1) if reason_match else "Reason not provided"
                    elif "good" in output:
                        ocsp_status["status"] = "Signed"
            
                    return ocsp_status
        except subprocess.CalledProcessError as e:
            return {"status": f"OCSP check failed with error: {str(e)}"}

        
    def extract_cert_from_mobileprovision(self, mobileprovision_data: bytes) -> tuple:
        plist_match = re.search(rb'<\?xml.*?\</plist\>', mobileprovision_data, re.DOTALL) or re.search(rb'bplist00.*', mobileprovision_data, re.DOTALL)
        if not plist_match:
            raise ValueError("Plist data not found in the .mobileprovision file.")
        plist_data = plist_match.group()
        plist = plistlib.loads(plist_data)
        cert_data = plist['DeveloperCertificates'][0]
        cert = x509.load_der_x509_certificate(cert_data)
        entitlements = plist.get('Entitlements', {})
        cert_type = "Enterprise Certificate" if plist.get("ProvisionsAllDevices", False) else "Personal Certificate"
        return cert, entitlements, cert_type        
        
    def check_entitlements(self, entitlements: dict) -> dict:
        return {entitlements_mapping[key]: {"status": "active"} for key in entitlements if key in entitlements_mapping}

    def check_p12(self, p12_data: bytes, password: str = ""):
        try:
            cert, cert_chain = self.extract_cert_from_p12(p12_data, password)
            
            if cert is None:
                raise InvalidCertificateError("Invalid certificate: No private certificate found in the P12 file.")
            
            cert_info = self.get_certificate_info(cert)
            p12_cert, full_chain_cert = self.create_cert_files(cert, cert_chain)
        except ValueError:
            raise InvalidCertificateError("Invalid certificate: Incorrect password or unable to process the P12 file.")
    
        private_key = None
        try:
            p12 = pkcs12.load_key_and_certificates(p12_data, password.encode('utf-8'))
            if p12[0]:
                private_key = p12[0].private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode('utf-8')
            else:
                return {"certificate_status": "Valid certificate: Public certificate is present but the private key is missing."}
        except Exception:
            return {"certificate_status": "Error: Unable to read the private key from the P12 file."}
    
        ocsp_url = cert_info.get("ocsp_url")
        ocsp_status = {"status": "OCSP URL not available"} if not ocsp_url else self._ocsp_check_with_openssl(p12_cert, full_chain_cert, ocsp_url)
        
        if ocsp_status.get("status") == "Revoked" and "reason" in ocsp_status:
            reason_code = ocsp_status["reason"].split('(')[-1].strip(')')
            ocsp_status["reason_details"] = self.get_revocation_reason_description(reason_code)
    
        result = {
            "certificate_info": cert_info,
            "certificate_status": ocsp_status,
            "private_key": private_key
        }

        return result



    def check_provision(self, provision_data: bytes):
        cert, entitlements, cert_type = self.extract_cert_from_mobileprovision(provision_data)
        cert_info = self.get_certificate_info(cert)
        p12_file, full_chain_file = self.create_cert_files(cert)
        ocsp_url = cert_info.get("ocsp_url")
        ocsp_status = {"status": "OCSP URL not available"} if not ocsp_url else self._ocsp_check_with_openssl(p12_file, full_chain_file, ocsp_url)
        if ocsp_status.get("status") == "Revoked" and "reason" in ocsp_status:
            reason_code = ocsp_status["reason"].split('(')[-1].strip(')')
            ocsp_status["reason_details"] = self.get_revocation_reason_description(reason_code)
        result = {
            "certificate_info": cert_info,
            "certificate_status": ocsp_status,
            "entitlements": self.check_entitlements(entitlements),
            "type": cert_type
        }
        return result
