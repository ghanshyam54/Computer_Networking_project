import cgi

data = cgi.FieldStorage() 
print(data.getfirst('Fname'))
print(data.getfirst('gname'))
