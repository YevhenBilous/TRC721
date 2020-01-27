import smartpy as sp

class TRC721(sp.Contract):
    def __init__(self):
        self.init(
                  _TRC721_RECEIVED = 432,
                  _INTERFACE_ID_TRC721 = 1234,
                  _tokenOwner = sp.Map(),
                  _tokenApprovals = sp.Map(),
                  _ownedTokensCount = sp.Map(),
                  _operatorApprovals = sp.Map() )
    
    @sp.entryPoint
    def balanceOf(self, params):
        sp.verify(params.owner != sp.address(0))
        return self.data._ownedTokensCount[params.owner].current
        
    @sp.entryPoint 
    def ownerOf(self, params):
        owner = self.data._tokenOwner[params.tokenId]
        sp.verify(owner != sp.address(0))
        return owner
      
    @sp.entryPoint 
    def approve(self, params): 
        owner = self.data._tokenOwner[params.tokenId]
        sp.verify(owner != sp.address(0))
        sp.verify(params.to != owner)
        sp.verify(sp.sender == owner)
        self.data._tokenApprovals[params.tokenId] = params.to
    
    def isApprovedForAll(self, params):
        return self.data._operatorApprovals[params.owner][params.operator]

    def getApproved(self, params):       
        sp.verify(self._exists(params.tokenId))
        return self.data._tokenApprovals[params.tokenId]

    @sp.entryPoint
    def _transferfromm(self, params):
        sp.verify(params.to != sp.address(0))
        self.data._ownedTokensCount[params.fromm] = self.data._ownedTokensCount[params.fromm] + 1
        self.data._ownedTokensCount[params.to] = self.data._ownedTokensCount[params.to] + 1
        self.data._tokenOwner[params.tokenId] = params.to
        
    def _isApprovedOrOwner(self, params):
        sp.verify(self._exists(params.tokenId))
        owner = self.ownerOf(params.tokenId)
        return (sp.spender == owner or self.getApproved(params.tokenId) == sp.spender or self.isApprovedForAll(owner, sp.spender))
      
    @sp.entryPoint   
    def _clearApproval(self, params):
        sp.if (self.data._tokenApprovals[params.tokenId] != sp.address(0)):
            self.data._tokenApprovals[params.tokenId] = sp.address(0)

    @sp.entryPoint
    def _exists(self, params):
        owner = self.data._tokenOwner[params.tokenId]
        return owner == sp.address(0)
    
    @sp.entryPoint
    def register(self, params):
        self.data._ownedTokensCount[sp.sender] = 0    

    @sp.entryPoint
    def _mint(self, params):
        sp.verify(params.to != sp.address(0))
        self.data._tokenOwner[params.tokenId] = params.to
        self.data._ownedTokensCount[params.to] = self.data._ownedTokensCount[params.to] + 1    
@addTest(name = "First test")
def test():
    sc = sp.testScenario()
    _tokenOwner = {}
    c1 = TRC721()
    sc += c1
    sender = sp.address(1)

    sc.h3("Balance Of")
    sc += c1.balanceOf(owner = sp.address("KT1AkvDHuXn2o6DVfprmS4XYDpNW3gt77157"))
    
    sc += c1.register().run(sender = "1")
    
    sc += c1.register().run(sender = "2")
    
    sc.h3("Mint")
    sc += c1._mint(to = sender, tokenId = 123)
    
    sc.h3("Owner Of")
    sc += c1.ownerOf(tokenId=123)
    
    sc.h3("Approve")
    sc += c1.approve(to = sp.address("dn1XPZsRJF9UuNZXbmEHq6TepSud8Xuumx4v"), tokenId = 123).run(sender = "1")
    
    sc.h3("_transferfrom")
    sc += c1._transferfromm(tokenId=123, fromm = sp.address(1), to = sp.address(2))
    
    sc.h3("clearApproval")
    sc += c1._clearApproval(tokenId=123)
