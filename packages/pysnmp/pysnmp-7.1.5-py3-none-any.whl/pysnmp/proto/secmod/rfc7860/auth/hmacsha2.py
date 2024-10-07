#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2018, Olivier Verriest <verri@x25.pm>
# License: https://www.pysnmp.com/pysnmp/license.html
#
import hmac
import sys
from hashlib import sha224, sha256, sha384, sha512

from pyasn1.type import univ

from pysnmp.proto import errind, error
from pysnmp.proto.secmod.rfc3414 import localkey
from pysnmp.proto.secmod.rfc3414.auth import base


# 7.2.4


class HmacSha2(base.AbstractAuthenticationService):
    SHA224_SERVICE_ID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 4)  # usmHMAC128SHA224AuthProtocol
    SHA256_SERVICE_ID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 5)  # usmHMAC192SHA256AuthProtocol
    SAH384_SERVICE_ID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 6)  # usmHMAC256SHA384AuthProtocol
    SHA512_SERVICE_ID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 7)  # usmHMAC384SHA512AuthProtocol
    KEY_LENGTH = {
        SHA224_SERVICE_ID: 28,
        SHA256_SERVICE_ID: 32,
        SAH384_SERVICE_ID: 48,
        SHA512_SERVICE_ID: 64,
    }
    DIGEST_LENGTH = {
        SHA224_SERVICE_ID: 16,
        SHA256_SERVICE_ID: 24,
        SAH384_SERVICE_ID: 32,
        SHA512_SERVICE_ID: 48,
    }
    HASH_ALGORITHM = {
        SHA224_SERVICE_ID: sha224,
        SHA256_SERVICE_ID: sha256,
        SAH384_SERVICE_ID: sha384,
        SHA512_SERVICE_ID: sha512,
    }

    IPAD = [0x36] * 64
    OPAD = [0x5C] * 64

    def __init__(self, oid):
        if oid not in self.HASH_ALGORITHM:
            raise error.ProtocolError(
                f"No SHA-2 authentication algorithm {oid} available"
            )
        self.__hashAlgo = self.HASH_ALGORITHM[oid]
        self.__digestLength = self.DIGEST_LENGTH[oid]
        self.__placeHolder = univ.OctetString((0,) * self.__digestLength).asOctets()

    def hashPassphrase(self, authKey):
        return localkey.hashPassphrase(authKey, self.__hashAlgo)

    def localizeKey(self, authKey, snmpEngineID):
        return localkey.localizeKey(authKey, snmpEngineID, self.__hashAlgo)

    @property
    def digestLength(self):
        return self.__digestLength

    # 7.3.1
    def authenticateOutgoingMsg(self, authKey, wholeMsg):
        # 7.3.1.1
        location = wholeMsg.find(self.__placeHolder)
        if location == -1:
            raise error.ProtocolError("Can't locate digest placeholder")
        wholeHead = wholeMsg[:location]
        wholeTail = wholeMsg[location + self.__digestLength :]

        # 7.3.1.2, 7.3.1.3
        try:
            mac = hmac.new(authKey.asOctets(), wholeMsg, self.__hashAlgo)

        except errind.ErrorIndication:
            raise error.StatusInformation(errorIndication=sys.exc_info()[1])

        # 7.3.1.4
        mac = mac.digest()[: self.__digestLength]

        # 7.3.1.5 & 6
        return wholeHead + mac + wholeTail

    # 7.3.2
    def authenticateIncomingMsg(self, authKey, authParameters, wholeMsg):
        # 7.3.2.1 & 2
        if len(authParameters) != self.__digestLength:
            raise error.StatusInformation(errorIndication=errind.authenticationError)

        # 7.3.2.3
        location = wholeMsg.find(authParameters.asOctets())
        if location == -1:
            raise error.ProtocolError("Can't locate digest in wholeMsg")
        wholeHead = wholeMsg[:location]
        wholeTail = wholeMsg[location + self.__digestLength :]
        authenticatedWholeMsg = wholeHead + self.__placeHolder + wholeTail

        # 7.3.2.4
        try:
            mac = hmac.new(authKey.asOctets(), authenticatedWholeMsg, self.__hashAlgo)

        except errind.ErrorIndication:
            raise error.StatusInformation(errorIndication=sys.exc_info()[1])

        # 7.3.2.5
        mac = mac.digest()[: self.__digestLength]

        # 7.3.2.6
        if mac != authParameters:
            raise error.StatusInformation(errorIndication=errind.authenticationFailure)

        return authenticatedWholeMsg
