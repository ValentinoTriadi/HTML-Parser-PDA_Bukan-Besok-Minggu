class HTMLParser:
    current_state:str = ''
    state:list = []
    rule:dict = {
        '<': {
            'top': '',
            'next-stack':'',
            'push':''
        },
        'h': {
            'top': '',
            'next-stack':'',
            'push':''
        },
        'l': {
            'top': '',
            'next-stack':'',
            'push':''
        }
    }
    symbol:list = []


    def makeStateList(self, s):
        global state
        temp = ""
        for cc in s:
            if cc != ' ':
                temp += cc
            else:
                self.state.append(temp)
                temp = ''
        print(self.state)

    def makeSymbolList(self, s):
        global symbol
        temp = ""
        for cc in s:
            if cc != ' ':
                temp += cc
            else:
                self.symbol.append(temp)
                temp = ''
        print(self.symbol)

    def makeRuleDict(self, s):
        global rule, current_state
        temprule = []
        tempdict = {}
        temp = ""
        for cc in s:
            if cc != ' ':
                temp += cc
            else:
                temprule.append(temp)
                temp = ''
        if temprule[0] == current_state:
            tempdict['top'] = temprule[2]
            tempdict['next-state'] = temprule[3]
            tempdict['push'] = temprule[4]
        rule[temprule[1]] = tempdict
    # def checkInput(self,currentState,currentInput,)



    
    def parsePDA(self):
        f = open("PDA.txt")
        s = f.readlines()
        self.makeStateList(self, s)
        s = f.readlines()
        self.makeSymbolList(self, s)
        s = ''
        s = f.readlines()
        while not s:
            self.makeRuleDict(self,s)
            s = f.readlines()



    def __init__(self):
        states, self.rules, input_symbols = self.read_files('PDA.txt')
        self.current_state = 'MAIN'
        self.stack = ['Z']
    
    # def check_states(self, line):
    #     self.current_state = line[]

    def read_files(self, rules_file):
        with open(rules_file, 'r') as file:
            lines = file.readlines()
        states = lines[0].strip().split(' ')
        input_symbols = lines[1].strip().split(' ')
        rules = [line.strip() for line in lines[2:] if line.strip()]
        return states, rules, input_symbols

    # def apply_pda(self):
    #     self.current_state = 
    def apply_rule(self, rule, input_char):
        rule_parts = rule.split(' ')
        current_states = rule_parts[1]
        input_symbol = rule_parts[2]
        pop_symbol = rule_parts[3]
        next_states = rule_parts[4]
        push_symbols = ' '.join(rule_parts[5:])
        if self.current_state[0] in current_states and input_char == input_symbol:
            if pop_symbol != 'ε':
                self.stack.pop()
            self.current_state[0] = next_states
            if push_symbols != 'ε':
                self.stack.extend(push_symbols.split())

    def process_char(self, char):
        for rule in self.rules:
            self.apply_rule(rule, char)

    def parse_html(self, html_string):
        self.current_state[0] = 'MAIN'
        for char in html_string:
            self.process_char(char)



    # def parse(self, html):
    #     self.reset()
    #     index = 0
    #     _states = {'Z': 'HTML', 'H': 'HEAD', 'B': 'BODY'}
    #     _tags = {"html": 'HTML', "head": 'HEAD', "body": 'BODY'}
    #     _HeadTags = {'title': 'TITLE'}
    #     _HtmlTags = {'html': 'HTML', 'body': 'BODY', 'head': 'HEAD'}
    #     _tag_dict = {'_HeadTags': _HeadTags, '_HTMLTags': _HtmlTags}
    #     expected_tags = {'Z': ['HTML'], 'HTML': ['HEAD', 'BODY'], 'HEAD': ['TITLE'], 'BODY': []}


    #     while index < len(html):
    #         char = html[index]

    #         if char == '<':
    #             if index == 0:
    #                 self.stack.append('Z')
    #             tag, index = self.extract_tag(html, index + 1)

    #             if tag and tag[0] == '/':
    #                 self.handle_close_tag(tag[1:])
    #             elif tag and tag[-1] == '/':
    #                 self.handle_self_closing_tag(tag[:-1])
    #             elif tag:
    #                 current_state = self.stack[-1]
    #                 if tag not in expected_tags.get(current_state, []):
    #                     print(f"Unexpected tag '{tag}' in state '{current_state}'")
    #                     exit()

    #                 self.handle_open_tag(tag)
    #         else:
    #             self.handle_content(char)

    #         index += 1

    #     # Check if the stack is empty after parsing
    #     if not self.stack:
    #         print("HTML is well-formed.")
    #     else:
    #         print("HTML is not well-formed. Tags are not balanced.")

    # def handle_open_tag(self, tag):
    #     if self.stack:
    #         current_state = self.stack[-1]
    #         if tag not in expected_tags.get(current_state, []):
    #             print(f"Unexpected tag '{tag}' in state '{current_state}'")
    #             exit()
    #     self.stack.append(tag)


    # def handle_close_tag(self, tag):
    #     if self.stack and self.stack[-1] == tag:
    #         self.stack.pop()
    #     else:
    #         print(f"Error: Unexpected closing tag '{tag}'")
    #         exit()

    # def handle_self_closing_tag(self, tag):
    #     # Handle self-closing tags (e.g., <br/>)
    #     # Consider it as both opening and closing
    #     self.handle_open_tag(tag)
    #     self.handle_close_tag(tag)

    # def handle_content(self, char):
    #     # Handle content between tags
    #     pass

    # def reset(self):
    #     self.stack = []

    # def extract_tag(self, html, start_index):
    #     tag = ''
    #     index = start_index

    #     while index < len(html) and html[index] not in {'>', ' ', '\t', '\n', '\r'}:
    #         tag += html[index]
    #         index += 1

    #     return tag.strip(), index

# Example usage
html_parser = HTMLParser()
html_string = """<html>
<head>
</head>
<body>
</body>
</html>"""
html_parser.parse_html(html_string)

