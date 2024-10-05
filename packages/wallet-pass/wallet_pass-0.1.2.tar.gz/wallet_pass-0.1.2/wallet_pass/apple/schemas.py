from typing import Optional

from pydantic import BaseModel, Field
from wallet_pass.apple.constants import (
    Alignment,
    DateStyle,
    NumberStyle,
    BarcodeFormat
)


class FileSchema(BaseModel):
    file: bytes
    filename: str


class AppleField(BaseModel):
    key: str
    value: str
    label: Optional[str] = None
    changeMessage: Optional[str] = None
    textAlignment: Alignment = Alignment.LEFT
    dateStyle: Optional[DateStyle] = None
    numberStyle: Optional[NumberStyle] = None


class AppleBarcode(BaseModel):
    message: str
    format: BarcodeFormat = BarcodeFormat.QR
    altText: Optional[str] = None
    message_encoding: str = 'iso-8859-1'


class AppleGenericTemplate(BaseModel):
    headerFields: list[AppleField] = []
    primaryFields: list[AppleField] = []
    secondaryFields: list[AppleField] = []
    backFields: list[AppleField] = []
    auxiliaryFields: list[AppleField] = []


class ApplePassSchema(BaseModel):
    teamIdentifier: str
    passTypeIdentifier: str
    serialNumber: str
    organizationName: str
    description: str = ''
    formatVersion: int = 1
    webServiceURL: Optional[str] = None
    authenticationToken: Optional[str] = Field(
        default=None,
        min_length=16,
        description='Must be at least 16 characters long if provided'
    )
    expirationDate: Optional[str] = None

    backgroundColor: Optional[str] = None
    foregroundColor: Optional[str] = None
    labelColor: Optional[str] = None
    logoText: Optional[str] = None
    barcode: Optional[AppleBarcode] = None
    barcodes: Optional[list[AppleBarcode]] = []
    suppressStripShine: bool = False

    generic: Optional[AppleGenericTemplate] = None
