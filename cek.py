class HTMLParser:
    def __init__(self):
        self.current_state = 'MAIN'
        self.stack = ['Z']
        self.state = []
        self.symbol = []
        self.rule = {}
        self.parsePDA()
        print(self.symbol)
        print(self.state)

        # current_state:str = ''
        # state:list = []
        # rule:dict = {
        #     'current-state': {
        #         '<': {
        #             'top': '',
        #             'next-state':'',
        #             'push':''
        #         },
        #         'h': {
        #             'top': '',
        #             'next-stack':'',
        #             'push':''
        #         },
        #         'l': {
        #             'top': '',
        #             'next-stack':'',
        #             'push':''
        #         }
        #     }
        # }
        # symbol:list = []


    def makeStateList(self, s):
        global state
        temp = s.rstrip().split(" ")
        self.state = temp

    def makeSymbolList(self, s):
        global symbol
        temp = s.rstrip().split(" ")
        self.symbol = temp

    def makeRuleDict(self, s):
        global rule, current_state
        tempdict = {}
        fixdict = {}
        temprule = s.rstrip().split(' ')
        tempdict['top'] = temprule[2]
        tempdict['next-state'] = temprule[3]
        tempdict['push'] = temprule[4]
        fixdict[temprule[1]] = tempdict
        if temprule[0] in self.rule.keys():
            self.rule[temprule[0]].update(fixdict)
        else:
            self.rule[temprule[0]] = fixdict

    def parsePDA(self):
        f = open("PDA.txt")
        s = f.readlines()
        self.makeStateList(s[0])
        self.makeSymbolList(s[1])
        for i in range(2,len(s)):
            self.makeRuleDict(s[i])

    def checkSymbol(self,s):
        if not s in self.symbol:
            print("Unexpected Symbol")
            return False
        else:
            if not s in self.rule[self.current_state].keys():
                print("Symbol is not an input of current state")
                return False
        return True
    
    def modifyStack(self, cc):
        top = self.stack[-1]
        if (self.rule[self.current_state][cc]['top'] == top):
            self.stack.pop()
            push = self.rule[self.current_state][cc]['push']
            self.current_state = self.rule[self.current_state][cc]['next-state']
            for c in push:
                if c != '@':
                    self.stack.append(c)
        
    def parseHTML(self, namafile):
        f = open(namafile, 'r')
        s = f.read()
        f.close()
        s = s.replace('\n', '')
        print(s)

        for cc in s:
            if not self.checkSymbol(cc):
                return False
            self.modifyStack(cc)
            print(cc, self.stack)
            
        return True

html_parser = HTMLParser()
status = html_parser.parseHTML("html.txt")
if not status:
    print("FAIL")
else:
    print("SUCCESS")