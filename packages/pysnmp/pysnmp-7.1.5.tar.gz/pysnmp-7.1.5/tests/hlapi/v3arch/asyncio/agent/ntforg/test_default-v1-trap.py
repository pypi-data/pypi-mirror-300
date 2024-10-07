import asyncio
import pytest


from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.proto.api import v2c
from tests.manager_context import MANAGER_PORT, ManagerContextManager


@pytest.mark.asyncio
async def test_send_trap_enterprise_specific():
    async with ManagerContextManager() as (_, message_count):
        snmpEngine = SnmpEngine()
        errorIndication, errorStatus, errorIndex, varBinds = await sendNotification(
            snmpEngine,
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("localhost", MANAGER_PORT)),
            ContextData(),
            "trap",
            NotificationType(
                ObjectIdentity("1.3.6.1.4.1.20408.4.1.1.2.432")
            ).addVarBinds(
                (v2c.apiTrapPDU.sysUpTime, TimeTicks(12345)),
                ("1.3.6.1.2.1.1.1.0", OctetString("my system")),
                (v2c.apiTrapPDU.snmpTrapAddress, IpAddress("127.0.0.1")),
                (
                    ObjectIdentity("SNMPv2-MIB", "snmpTrapOID", 0),
                    ObjectIdentifier("1.3.6.1.4.1.20408.4.1.1.2.432"),
                ),
            ),
        )

        snmpEngine.closeDispatcher()
        await asyncio.sleep(1)
        assert message_count == [1]


@pytest.mark.asyncio
async def test_send_trap_generic():
    async with ManagerContextManager() as (_, message_count):
        snmpEngine = SnmpEngine()
        errorIndication, errorStatus, errorIndex, varBinds = await sendNotification(
            snmpEngine,
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("localhost", MANAGER_PORT)),
            ContextData(),
            "trap",
            NotificationType(ObjectIdentity("1.3.6.1.6.3.1.1.5.2"))
            .loadMibs("SNMPv2-MIB")
            .addVarBinds(
                (
                    "1.3.6.1.6.3.1.1.4.3.0",
                    "1.3.6.1.4.1.20408.4.1.1.2",
                ),  # IMPORTANT: MIB is needed to resolve str to correct type.
                ("1.3.6.1.2.1.1.1.0", OctetString("my system")),
            ),
        )

        snmpEngine.closeDispatcher()
        await asyncio.sleep(1)
        assert message_count == [1]


@pytest.mark.asyncio
async def test_send_trap_custom_mib():
    async with ManagerContextManager() as (_, message_count):
        snmpEngine = SnmpEngine()
        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        (sysUpTime,) = mibBuilder.importSymbols("__SNMPv2-MIB", "sysUpTime")
        sysUpTime.syntax = TimeTicks(12345)

        errorIndication, errorStatus, errorIndex, varBinds = await sendNotification(
            snmpEngine,
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("localhost", MANAGER_PORT)),
            ContextData(),
            "trap",
            NotificationType(
                ObjectIdentity("NET-SNMP-EXAMPLES-MIB", "netSnmpExampleNotification")
            ).addVarBinds(
                ObjectType(
                    ObjectIdentity(
                        "NET-SNMP-EXAMPLES-MIB", "netSnmpExampleHeartbeatRate"
                    ),
                    1,
                )
            ),
        )

        snmpEngine.closeDispatcher()
        await asyncio.sleep(1)
        assert message_count == [1]
