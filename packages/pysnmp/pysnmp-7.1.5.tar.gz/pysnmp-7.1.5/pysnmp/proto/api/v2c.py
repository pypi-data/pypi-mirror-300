#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
from pyasn1.type import constraint, univ

from pysnmp.proto import errind, rfc1901, rfc1902, rfc1905
from pysnmp.proto.api import v1

# Shortcuts to SNMP types
Null = univ.Null
null = Null("")
ObjectIdentifier = univ.ObjectIdentifier

Integer = rfc1902.Integer
Integer32 = rfc1902.Integer32
OctetString = rfc1902.OctetString
IpAddress = rfc1902.IpAddress
Counter32 = rfc1902.Counter32
Gauge32 = rfc1902.Gauge32
Unsigned32 = rfc1902.Unsigned32
TimeTicks = rfc1902.TimeTicks
Opaque = rfc1902.Opaque
Counter64 = rfc1902.Counter64
Bits = rfc1902.Bits

NoSuchObject = rfc1905.NoSuchObject
NoSuchInstance = rfc1905.NoSuchInstance
EndOfMibView = rfc1905.EndOfMibView

VarBind = rfc1905.VarBind
VarBindList = rfc1905.VarBindList
GetRequestPDU = rfc1905.GetRequestPDU
GetNextRequestPDU = rfc1905.GetNextRequestPDU
ResponsePDU = GetResponsePDU = rfc1905.ResponsePDU
SetRequestPDU = rfc1905.SetRequestPDU
GetBulkRequestPDU = rfc1905.GetBulkRequestPDU
InformRequestPDU = rfc1905.InformRequestPDU
SNMPv2TrapPDU = TrapPDU = rfc1905.SNMPv2TrapPDU
ReportPDU = rfc1905.ReportPDU

Message = rfc1901.Message

getNextRequestID = v1.getNextRequestID  # noqa: N816

apiVarBind = v1.apiVarBind  # noqa: N816


class PDUAPI(v1.PDUAPI):
    _errorStatus = rfc1905.errorStatus.clone(0)
    _errorIndex = univ.Integer(0).subtype(
        subtypeSpec=constraint.ValueRangeConstraint(0, rfc1905.max_bindings)
    )

    def getResponse(self, reqPDU):
        rspPDU = ResponsePDU()
        self.setDefaults(rspPDU)
        self.setRequestID(rspPDU, self.getRequestID(reqPDU))
        return rspPDU

    def getVarBindTable(self, reqPDU, rspPDU):
        return [apiPDU.getVarBinds(rspPDU)]

    def getNextVarBinds(self, varBinds, origVarBinds=None):
        errorIndication = None
        idx = nonNulls = len(varBinds)
        rspVarBinds = []
        while idx:
            idx -= 1
            if varBinds[idx][1].tagSet in (
                rfc1905.NoSuchObject.tagSet,
                rfc1905.NoSuchInstance.tagSet,
                rfc1905.EndOfMibView.tagSet,
            ):
                nonNulls -= 1
            elif origVarBinds is not None:
                seed = ObjectIdentifier(origVarBinds[idx][0]).asTuple()
                found = varBinds[idx][0].asTuple()
                if seed >= found:
                    errorIndication = errind.oidNotIncreasing

            rspVarBinds.insert(0, (varBinds[idx][0], null))

        if not nonNulls:
            rspVarBinds = []

        return errorIndication, rspVarBinds

    def setEndOfMibError(self, pdu, errorIndex):
        varBindList = self.getVarBindList(pdu)
        varBindList[errorIndex - 1].setComponentByPosition(
            1,
            rfc1905.endOfMibView,
            verifyConstraints=False,
            matchTags=False,
            matchConstraints=False,
        )

    def setNoSuchInstanceError(self, pdu, errorIndex):
        varBindList = self.getVarBindList(pdu)
        varBindList[errorIndex - 1].setComponentByPosition(
            1,
            rfc1905.noSuchInstance,
            verifyConstraints=False,
            matchTags=False,
            matchConstraints=False,
        )


apiPDU = PDUAPI()  # noqa: N816


class BulkPDUAPI(PDUAPI):
    _nonRepeaters = rfc1905.nonRepeaters.clone(0)
    _maxRepetitions = rfc1905.maxRepetitions.clone(10)

    def setDefaults(self, pdu):
        PDUAPI.setDefaults(self, pdu)
        pdu.setComponentByPosition(
            0,
            getNextRequestID(),
            verifyConstraints=False,
            matchTags=False,
            matchConstraints=False,
        )
        pdu.setComponentByPosition(
            1,
            self._nonRepeaters,
            verifyConstraints=False,
            matchTags=False,
            matchConstraints=False,
        )
        pdu.setComponentByPosition(
            2,
            self._maxRepetitions,
            verifyConstraints=False,
            matchTags=False,
            matchConstraints=False,
        )
        varBindList = pdu.setComponentByPosition(3).getComponentByPosition(3)
        varBindList.clear()

    @staticmethod
    def getNonRepeaters(pdu):
        return pdu.getComponentByPosition(1)

    @staticmethod
    def setNonRepeaters(pdu, value):
        pdu.setComponentByPosition(1, value)

    @staticmethod
    def getMaxRepetitions(pdu):
        return pdu.getComponentByPosition(2)

    @staticmethod
    def setMaxRepetitions(pdu, value):
        pdu.setComponentByPosition(2, value)

    def getVarBindTable(self, reqPDU, rspPDU):
        nonRepeaters = self.getNonRepeaters(reqPDU)

        reqVarBinds = self.getVarBinds(reqPDU)

        N = min(int(nonRepeaters), len(reqVarBinds))

        rspVarBinds = self.getVarBinds(rspPDU)

        # shortcut for the most trivial case
        if N == 0 and len(reqVarBinds) == 1:
            return [[vb] for vb in rspVarBinds]

        R = max(len(reqVarBinds) - N, 0)

        varBindTable = []

        if R:
            for i in range(0, len(rspVarBinds) - N, R):
                varBindRow = rspVarBinds[:N] + rspVarBinds[N + i : N + R + i]
                # ignore stray OIDs / non-rectangular table
                if len(varBindRow) == N + R:
                    varBindTable.append(varBindRow)
        elif N:
            varBindTable.append(rspVarBinds[:N])

        return varBindTable


apiBulkPDU = BulkPDUAPI()  # noqa: N816


class TrapPDUAPI(v1.PDUAPI):
    sysUpTime = (1, 3, 6, 1, 2, 1, 1, 3, 0)
    snmpTrapAddress = (1, 3, 6, 1, 6, 3, 18, 1, 3, 0)
    snmpTrapCommunity = (1, 3, 6, 1, 6, 3, 18, 1, 4, 0)
    snmpTrapOID = (1, 3, 6, 1, 6, 3, 1, 1, 4, 1, 0)
    snmpTrapEnterprise = (1, 3, 6, 1, 6, 3, 1, 1, 4, 3, 0)
    _zeroTime = TimeTicks(0)
    _genTrap = ObjectIdentifier((1, 3, 6, 1, 6, 3, 1, 1, 5, 1))

    def setDefaults(self, pdu):
        v1.PDUAPI.setDefaults(self, pdu)
        varBinds = [
            (self.sysUpTime, self._zeroTime),
            # generic trap
            (self.snmpTrapOID, self._genTrap),
        ]
        self.setVarBinds(pdu, varBinds)


apiTrapPDU = TrapPDUAPI()  # noqa: N816


class MessageAPI(v1.MessageAPI):
    _version = rfc1901.version.clone(1)

    def setDefaults(self, msg):
        msg.setComponentByPosition(
            0,
            self._version,
            verifyConstraints=False,
            matchTags=False,
            matchConstraints=False,
        )
        msg.setComponentByPosition(
            1,
            self._community,
            verifyConstraints=False,
            matchTags=False,
            matchConstraints=False,
        )
        return msg

    def getResponse(self, reqMsg):
        rspMsg = Message()
        self.setDefaults(rspMsg)
        self.setVersion(rspMsg, self.getVersion(reqMsg))
        self.setCommunity(rspMsg, self.getCommunity(reqMsg))
        self.setPDU(rspMsg, apiPDU.getResponse(self.getPDU(reqMsg)))
        return rspMsg


apiMessage = MessageAPI()  # noqa: N816
