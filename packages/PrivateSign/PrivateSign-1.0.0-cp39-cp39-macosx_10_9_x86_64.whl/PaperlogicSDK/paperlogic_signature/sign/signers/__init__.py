"""
This package houses the part of .paperlogic_signature that produces digital signatures.
It contains modules for creating ``SignedData`` CMS objects, embedding them
in PDF files, and for handling PDF-specific document signing needs.
"""

from .functions import async_sign_pdf, sign_pdf

from .pdf_cms import SimpleSigner
from .pdf_signer import PdfSignatureMetadata

from .constants import (
    DEFAULT_MD,
)

__all__ = [
    'SimpleSigner',
    'PdfSignatureMetadata',
    'sign_pdf',
    'async_sign_pdf',
    'DEFAULT_MD'
]