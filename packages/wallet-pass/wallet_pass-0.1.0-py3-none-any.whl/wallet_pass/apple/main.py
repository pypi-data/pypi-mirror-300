import hashlib
import io
import json
import zipfile

from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import pkcs7

from apple.schemas import ApplePassSchema, FileSchema


class ApplePass:
    def __init__(
            self,
            signature_cert: bytes,
            signature_key: bytes,
            signature_key_password: str,
            signature_wwdr_cert: bytes,
            apple_pass: ApplePassSchema,
            files: list[FileSchema] = []
    ):
        self.signature_cert = signature_cert
        self.signature_key = signature_key
        self.signature_key_password = signature_key_password
        self.signature_wwdr_cert = signature_wwdr_cert

        self.apple_pass = apple_pass
        self.files = files

    def get_pkpass_file(self) -> bytes:
        pass_json = json.dumps(self.apple_pass.model_dump(mode='json', exclude_none=True))
        manifest = self.create_manifest(pass_json)
        signature = self.create_signature_crypto(manifest)
        return self.create_zip(pass_json, manifest, signature)

    def create_manifest(self, pass_json: str) -> str:
        file_hashes = {'pass.json': hashlib.sha1(pass_json.encode()).hexdigest()}
        for file in self.files:
            file_hashes[file.filename] = hashlib.sha1(file.file).hexdigest()
        return json.dumps(file_hashes)

    def create_signature_crypto(self, manifest: str) -> bytes:
        cert = x509.load_pem_x509_certificate(self.signature_cert)
        private_key = serialization.load_pem_private_key(
            self.signature_key, password=self.signature_key_password.encode()
        )
        wwdr_cert = x509.load_pem_x509_certificate(
            self.signature_wwdr_cert
        )

        options = [pkcs7.PKCS7Options.DetachedSignature]
        return pkcs7.PKCS7SignatureBuilder().set_data(
            manifest.encode()
        ).add_signer(
            cert, private_key, hashes.SHA256()
        ).add_certificate(
            wwdr_cert
        ).sign(serialization.Encoding.DER, options)

    def create_zip(self, pass_json: str, manifest: str, signature: bytes) -> bytes:
        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zf:
            zf.writestr('signature', signature)
            zf.writestr('manifest.json', manifest)
            zf.writestr('pass.json', pass_json)
            for file in self.files:
                zf.writestr(file.filename, file.file)
        zip_file.seek(0)
        return zip_file.read()
