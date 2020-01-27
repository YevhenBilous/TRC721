import smartpy as sp

class ITRC721(sp.Contract):

    @sp.entryPoint
    def balanceOf(self, params):
        return 0

    @sp.entryPoint
    def ownerOf(self, params):
        return 0

    @sp.entryPoint
    def safeTransferFrom(self, params):
        return payable

    @sp.entryPoint
    def transferFrom(self, params):
        return payable

    @sp.entryPoint
    def approve(self, params):
        return payable

    @sp.entryPoint
    def setApprovalForAll(self, params):
        return ""

    @sp.entryPoint
    def getApproved(self, params):
        return address

    @sp.entryPoint
    def isApprovedForAll(self, params):
        return true