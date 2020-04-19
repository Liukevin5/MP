
infile = open('shoe.html', 'r')
firstLine = infile.readline()


start = firstLine.index("data-alt-image='")
newString = firstLine[start+16:]
i = newString.index('}')
newString = newString[:i+1]
