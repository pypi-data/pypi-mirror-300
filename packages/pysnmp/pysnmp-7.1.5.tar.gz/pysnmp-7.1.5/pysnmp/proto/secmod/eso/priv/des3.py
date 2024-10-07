#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
import random
from hashlib import md5, sha1

from pyasn1.type import univ

from pysnmp.proto import errind, error
from pysnmp.proto.secmod.rfc3414 import localkey
from pysnmp.proto.secmod.rfc3414.auth import hmacmd5, hmacsha
from pysnmp.proto.secmod.rfc3414.priv import base
from pysnmp.proto.secmod.rfc7860.auth import hmacsha2

PysnmpCryptoError = False
try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.decrepit.ciphers import algorithms
    from cryptography.hazmat.primitives.ciphers import Cipher, modes
except ImportError:
    PysnmpCryptoError = True

random.seed()


# 5.1.1


class Des3(base.AbstractEncryptionService):
    """Reeder 3DES-EDE for USM (Internet draft).

    https://tools.ietf.org/html/draft-reeder-snmpv3-usm-3desede-00
    """

    SERVICE_ID = (1, 3, 6, 1, 6, 3, 10, 1, 2, 3)  # usm3DESEDEPrivProtocol
    KEY_SIZE = 32
    local_int = random.randrange(0, 0xFFFFFFFF)

    def hashPassphrase(self, authProtocol, privKey):
        if authProtocol == hmacmd5.HmacMd5.SERVICE_ID:
            hashAlgo = md5
        elif authProtocol == hmacsha.HmacSha.SERVICE_ID:
            hashAlgo = sha1
        elif authProtocol in hmacsha2.HmacSha2.HASH_ALGORITHM:
            hashAlgo = hmacsha2.HmacSha2.HASH_ALGORITHM[authProtocol]
        else:
            raise error.ProtocolError(f"Unknown auth protocol {authProtocol}")
        return localkey.hashPassphrase(privKey, hashAlgo)

    # 2.1
    def localizeKey(self, authProtocol, privKey, snmpEngineID):
        if authProtocol == hmacmd5.HmacMd5.SERVICE_ID:
            hashAlgo = md5
        elif authProtocol == hmacsha.HmacSha.SERVICE_ID:
            hashAlgo = sha1
        elif authProtocol in hmacsha2.HmacSha2.HASH_ALGORITHM:
            hashAlgo = hmacsha2.HmacSha2.HASH_ALGORITHM[authProtocol]
        else:
            raise error.ProtocolError(f"Unknown auth protocol {authProtocol}")
        localPrivKey = localkey.localizeKey(privKey, snmpEngineID, hashAlgo)

        # now extend this key if too short by repeating steps that includes the hashPassphrase step
        while len(localPrivKey) < self.KEY_SIZE:
            # this is the difference between reeder and bluementhal
            newKey = localkey.hashPassphrase(localPrivKey, hashAlgo)
            localPrivKey += localkey.localizeKey(newKey, snmpEngineID, hashAlgo)

        return localPrivKey[: self.KEY_SIZE]

    # 5.1.1.1
    def __getEncryptionKey(self, privKey, snmpEngineBoots):
        # 5.1.1.1.1
        des3Key = privKey[:24]
        preIV = privKey[24:32]

        securityEngineBoots = int(snmpEngineBoots)

        salt = [
            securityEngineBoots >> 24 & 0xFF,
            securityEngineBoots >> 16 & 0xFF,
            securityEngineBoots >> 8 & 0xFF,
            securityEngineBoots & 0xFF,
            self.local_int >> 24 & 0xFF,
            self.local_int >> 16 & 0xFF,
            self.local_int >> 8 & 0xFF,
            self.local_int & 0xFF,
        ]
        if self.local_int == 0xFFFFFFFF:
            self.local_int = 0
        else:
            self.local_int += 1

        # salt not yet hashed XXX

        return (
            des3Key.asOctets(),
            univ.OctetString(salt).asOctets(),
            univ.OctetString(
                map(lambda x, y: x ^ y, salt, preIV.asNumbers())
            ).asOctets(),
        )

    @staticmethod
    def __getDecryptionKey(privKey, salt):
        return (
            privKey[:24].asOctets(),
            univ.OctetString(
                map(lambda x, y: x ^ y, salt.asNumbers(), privKey[24:32].asNumbers())
            ).asOctets(),
        )

    # 5.1.1.2
    def encryptData(self, encryptKey, privParameters, dataToEncrypt):
        if PysnmpCryptoError:
            raise error.StatusInformation(errorIndication=errind.encryptionError)

        snmpEngineBoots, snmpEngineTime, salt = privParameters

        des3Key, salt, iv = self.__getEncryptionKey(encryptKey, snmpEngineBoots)

        privParameters = univ.OctetString(salt)

        plaintext = (
            dataToEncrypt
            + univ.OctetString((0,) * (8 - len(dataToEncrypt) % 8)).asOctets()
        )

        try:
            des3 = _cryptography_cipher(des3Key, iv).encryptor()
            ciphertext = des3.update(plaintext) + des3.finalize()

        except AttributeError:
            raise error.StatusInformation(
                errorIndication=errind.unsupportedPrivProtocol
            )

        return univ.OctetString(ciphertext), privParameters

    # 5.1.1.3
    def decryptData(self, decryptKey, privParameters, encryptedData):
        if PysnmpCryptoError:
            raise error.StatusInformation(errorIndication=errind.decryptionError)
        snmpEngineBoots, snmpEngineTime, salt = privParameters

        if len(salt) != 8:
            raise error.StatusInformation(errorIndication=errind.decryptionError)

        des3Key, iv = self.__getDecryptionKey(decryptKey, salt)

        if len(encryptedData) % 8 != 0:
            raise error.StatusInformation(errorIndication=errind.decryptionError)

        ciphertext = encryptedData.asOctets()

        try:
            des3 = _cryptography_cipher(des3Key, iv).decryptor()
            plaintext = des3.update(ciphertext) + des3.finalize()

        except AttributeError:
            raise error.StatusInformation(
                errorIndication=errind.unsupportedPrivProtocol
            )

        return plaintext


def _cryptography_cipher(key, iv):
    """Build a cryptography TripleDES Cipher object.

    :param bytes key: Encryption key
    :param bytesiv iv: Initialization vector
    :returns: TripleDES Cipher instance
    :rtype: cryptography.hazmat.primitives.ciphers.Cipher
    """
    return Cipher(
        algorithm=algorithms.TripleDES(key),
        mode=modes.CBC(iv),
        backend=default_backend(),
    )
