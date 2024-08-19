from sys import exit
from WLAN_DOT11_CONSTANTS import *

def customresize(array, new_size):
    return (array._type_*new_size).from_address(addressof(array))

ERROR_SUCCESS = 0

def get_BSSID():

    BSSID_Values={}

    NegotiatedVersion = DWORD()
    ClientHandle = HANDLE()
    ret = WlanOpenHandle(1, None, byref(NegotiatedVersion), byref(ClientHandle))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
    pInterfaceList = pointer(WLAN_INTERFACE_INFO_LIST())
    ret = WlanEnumInterfaces(ClientHandle, None, byref(pInterfaceList))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
    try:
        ifaces = customresize(pInterfaceList.contents.InterfaceInfo,
                              pInterfaceList.contents.NumberOfItems)
        for iface in ifaces:

            pAvailableNetworkList2 = pointer(WLAN_BSS_LIST())


            ret2 = WlanGetNetworkBssList(ClientHandle,
                                         byref(iface.InterfaceGuid),
                                         None,
                                         None,True,None,
                                         byref(pAvailableNetworkList2))
            if ret2 != ERROR_SUCCESS:
                exit(FormatError(ret2))
            try:
                retScan = WlanScan(ClientHandle,byref(iface.InterfaceGuid),None,None,None)
                if retScan != ERROR_SUCCESS:
                    exit(FormatError(retScan))
                avail_net_list2 = pAvailableNetworkList2.contents
                networks2 = customresize(avail_net_list2.NetworkBSS,
                                         avail_net_list2.NumberOfItems)

                for network in networks2:
                    SSID = str(network.dot11Ssid.SSID[:network.dot11Ssid.SSIDLength])
                    Center_Freq= network.ulChCenterFrequency
                    BSSID = ':'.join('%02x' % b for b in network.dot11Bssid).upper()
                    signal_strength = str(network.lRssi)
                    BSSID_Values[BSSID] = [SSID, Center_Freq/1000, signal_strength]
            finally:
                WlanFreeMemory(pAvailableNetworkList2)
                WlanCloseHandle(ClientHandle,None)
    finally:
        WlanFreeMemory(pInterfaceList)
    return BSSID_Values