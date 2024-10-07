"""
Walk Agent MIB (SNMPv1)
+++++++++++++++++++++++

Perform SNMP GETNEXT operation with the following options:

* with SNMPv1, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for OID in tuple form

This script performs similar to the following Net-SNMP command:

| $ snmpwalk -v1 -c public -ObentU demo.pysnmp.com 1.3.6

"""  #
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api

# Protocol version to use
pMod = api.protoModules[api.protoVersion1]
# pMod = api.protoModules[api.protoVersion2c]

# SNMP table header
headVars = [pMod.ObjectIdentifier((1, 3, 6))]

# Build PDU
reqPDU = pMod.GetNextRequestPDU()
pMod.apiPDU.setDefaults(reqPDU)
pMod.apiPDU.setVarBinds(reqPDU, [(x, pMod.null) for x in headVars])

# Build message
reqMsg = pMod.Message()
pMod.apiMessage.setDefaults(reqMsg)
pMod.apiMessage.setCommunity(reqMsg, "public")
pMod.apiMessage.setPDU(reqMsg, reqPDU)


# noinspection PyUnusedLocal
def cbRecvFun(
    transportDispatcher,
    transportDomain,
    transportAddress,
    wholeMsg,
    reqPDU=reqPDU,
    headVars=headVars,
):
    while wholeMsg:
        rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message())
        rspPDU = pMod.apiMessage.getPDU(rspMsg)

        # Match response to request
        if pMod.apiPDU.getRequestID(reqPDU) == pMod.apiPDU.getRequestID(rspPDU):
            # Check for SNMP errors reported
            errorStatus = pMod.apiPDU.getErrorStatus(rspPDU)
            if errorStatus and errorStatus != 2:
                raise Exception(errorStatus)

            # Format var-binds table
            varBindTable = pMod.apiPDU.getVarBindTable(reqPDU, rspPDU)

            # Report SNMP table
            for tableRow in varBindTable:
                for name, val in tableRow:
                    print(
                        "from: {}, {} = {}".format(
                            transportAddress, name.prettyPrint(), val.prettyPrint()
                        )
                    )

            # Stop on EOM
            for oid, val in varBindTable[-1]:
                if not isinstance(val, pMod.Null):
                    break

            else:
                transportDispatcher.jobFinished(1)
                continue

            # Generate request for next row
            pMod.apiPDU.setVarBinds(
                reqPDU, [(x, pMod.null) for x, y in varBindTable[-1]]
            )

            pMod.apiPDU.setRequestID(reqPDU, pMod.getNextRequestID())

            transportDispatcher.sendMessage(
                encoder.encode(reqMsg), transportDomain, transportAddress
            )

    return wholeMsg


transportDispatcher = AsyncioDispatcher()

transportDispatcher.registerRecvCbFun(cbRecvFun)

transportDispatcher.registerTransport(
    udp.domainName, udp.UdpAsyncioTransport().openClientMode()
)

transportDispatcher.sendMessage(
    encoder.encode(reqMsg), udp.domainName, ("demo.pysnmp.com", 161)
)

transportDispatcher.jobStarted(1)

transportDispatcher.runDispatcher(3)

transportDispatcher.closeDispatcher()
