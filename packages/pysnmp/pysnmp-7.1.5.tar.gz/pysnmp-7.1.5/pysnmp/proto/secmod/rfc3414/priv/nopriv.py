#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
from pysnmp.proto import errind, error
from pysnmp.proto.secmod.rfc3414.priv import base


class NoPriv(base.AbstractEncryptionService):
    SERVICE_ID = (1, 3, 6, 1, 6, 3, 10, 1, 2, 1)  # usmNoPrivProtocol

    def hashPassphrase(self, authProtocol, privKey):
        return

    def localizeKey(self, authProtocol, privKey, snmpEngineID):
        return

    def encryptData(self, encryptKey, privParameters, dataToEncrypt):
        raise error.StatusInformation(errorIndication=errind.noEncryption)

    def decryptData(self, decryptKey, privParameters, encryptedData):
        raise error.StatusInformation(errorIndication=errind.noEncryption)
