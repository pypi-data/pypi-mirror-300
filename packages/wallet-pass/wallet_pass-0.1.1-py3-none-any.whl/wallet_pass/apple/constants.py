from enum import StrEnum


class Alignment(StrEnum):
    LEFT = 'PKTextAlignmentLeft'
    CENTER = 'PKTextAlignmentCenter'
    RIGHT = 'PKTextAlignmentRight'
    JUSTIFIED = 'PKTextAlignmentJustified'
    NATURAL = 'PKTextAlignmentNatural'


class BarcodeFormat(StrEnum):
    PDF417 = 'PKBarcodeFormatPDF417'
    QR = 'PKBarcodeFormatQR'
    AZTEC = 'PKBarcodeFormatAztec'
    CODE128 = 'PKBarcodeFormatCode128'


class TransitType(StrEnum):
    AIR = 'PKTransitTypeAir'
    TRAIN = 'PKTransitTypeTrain'
    BUS = 'PKTransitTypeBus'
    BOAT = 'PKTransitTypeBoat'
    GENERIC = 'PKTransitTypeGeneric'


class DateStyle(StrEnum):
    NONE = 'PKDateStyleNone'
    SHORT = 'PKDateStyleShort'
    MEDIUM = 'PKDateStyleMedium'
    LONG = 'PKDateStyleLong'
    FULL = 'PKDateStyleFull'


class NumberStyle(StrEnum):
    DECIMAL = 'PKNumberStyleDecimal'
    PERCENT = 'PKNumberStylePercent'
    SCIENTIFIC = 'PKNumberStyleScientific'
    SPELLOUT = 'PKNumberStyleSpellOut'
