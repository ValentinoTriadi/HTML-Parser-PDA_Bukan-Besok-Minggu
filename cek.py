import sys


class HTMLParser:
    def __init__(self):
        self.current_state = 'MAIN'
        self.stack = ['Z']
        self.state = []
        self.symbol = []
        self.rule = {}
        self.parsePDA()
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
        temp = s.rstrip().split(" ")
        self.state = temp

    def makeSymbolList(self, s):
        temp = s.rstrip().split(" ")
        self.symbol = temp

    def makeRuleDict(self, s):
        tempdict = {}
        fixdict = {}
        temprule = s.rstrip().split(' ')
        tempdict['top'] = temprule[2]
        tempdict['next-state'] = temprule[3]
        #print(temprule[3])
        tempdict['push'] = temprule[4]
        fixdict[temprule[1]] = tempdict
        if temprule[0] in self.rule.keys():
            self.rule[temprule[0]].update(fixdict)
        else:
            self.rule[temprule[0]] = fixdict

    def parsePDA(self):
        f = open(sys.argv[1])
        s = f.readlines()
        self.makeStateList(s[0])
        self.makeSymbolList(s[1])
        for i in range(2,len(s)):
            self.makeRuleDict(s[i])

    def checkSymbol(self, s):
        if not s in self.symbol and s != ' ':
            print(f"\x1b[91mSyntax Error!\x1b[0m")
            print("\x1b[93mUnexpected Symbol\x1b[0m\033[94m",s,'\033[0m\033[93m!\033[0m')
            return False
        else:
            if ('@' in self.rule[self.current_state].keys()):
                c = self.rule[self.current_state].keys()
                for i in c:
                    if (s != i and i != '@'):
                        return True
            elif not s in self.rule[self.current_state].keys():
                print(f"\x1b[91mSyntax Error!\x1b[0m")
                print(f"\x1b[93mSymbol \033[94m{s}\033[93m is not an input of current state\x1b[0m")
                return False

        return True
    
    def modifyStack(self, cc):
        top = self.stack[-1]
        if ('@' in self.rule[self.current_state].keys()):
            c = self.rule[self.current_state].keys()
            for i in c:
                if (cc != i and i != '@'):
                    self.current_state = self.rule[self.current_state]['@']['next-state']
                    return True
        if (self.rule[self.current_state][cc]['top'] == top):
            self.stack.pop()
            push = self.rule[self.current_state][cc]['push']
            self.current_state = self.rule[self.current_state][cc]['next-state']
            for c in push:
                if c != '@':
                    self.stack.append(c)
            return True
        elif (self.rule[self.current_state][cc]['top'] == '@'):
            push = self.rule[self.current_state][cc]['push']
            self.current_state = self.rule[self.current_state][cc]['next-state']
            for c in push:
                if c != '@':
                    self.stack.append(c)
            return True
        else:
            return False
        
    def reversestack(self, stack):
        bro = stack
        newstack = []
        for i in range(len(bro)):
            newstack.append(bro[-i-1])
        return newstack
        
    def parseHTML(self, namafile):
        f = open(namafile, 'r')
        s = f.read()
        f.close()
        # s = s.replace('\n', '')
        line = 1
        char = 0
        temp = ""
        ignoreSpace = True
        for cc in s:
            if cc == '\n':
                line += 1
                char = 0
                ignoreSpace = True
            elif cc == ' ' and ignoreSpace:
                char+=1
                continue
            else:
                temp+=cc
                char+=1
                ignoreSpace = False
                if (cc == ' '):
                    cc = '+'
                if not self.checkSymbol(cc):
                    return line, char
                if (not self.modifyStack(cc)):
                    if (cc == '+'):
                        cc = "Space"
                    print("\033[91mSyntax Error!\033[0m")
                    print("Tag Salah!",'Symbol\033[95m',cc + '\x1b[0m'+ " seharusnya adalah symbol\033[95m", self.stack[-1], '\033[0m')
                    return line, char 
                newstack = self.reversestack(self.stack)
                print('\x1b[41m',cc, newstack, self.current_state,'\x1b[0m')
        return -1, -1

html_parser = HTMLParser()
status = html_parser.parseHTML(sys.argv[2])

if status[0] != -1:
    print('\033[96m'+"FAIL"+'\033[0m'+" on line", '\033[93m', status[0],'\033[0m', "char ke", '\033[93m', status[1],'\033[0m', "On state",'\033[94m', html_parser.current_state, '\033[0m')
    f = open(sys.argv[2])
    lines = ""
    for i in range(status[0]):
        lines = f.readline()
    count = 0
    ignoreBlank = True
    print('\033[97mError: \033[0m', end='')
    for c in lines:
        count+=1
        if (c == ' ' and ignoreBlank):
            continue
        else:
            ignoreBlank = False
            if (count != status[1]):
                print(c,end='')
            else:
                if (c != ' '):
                    print('\033[91m'+c+'\033[0m', end='')
                else:
                    print('\033[91m'+'_'+'\033[0m', end='')
else:
    if (html_parser.stack[-1] == 'Z'):
        print('\033[92m'+"Accepted"+'\033[0m')
    else:
        print('\033[93m'+"Stack is not empty!"+'\033[0m')

    