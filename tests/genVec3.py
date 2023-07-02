#!/usr/bin/python
import sys

verts = open(sys.argv[1])
contents = list(filter(len, verts.read().split('\n')))
verts.close()


out = open(sys.argv[2], "w")

out.write("{\n\t")

for i in range(len(contents)):
    floats = contents[i].split()
    
    out.write("vec4(")
    
    for j in range(len(floats)):
        if j:
            out.write(", ")
        out.write(floats[j])
    
    out.write(")")
    
    if i != len(contents) - 1:
        out.write(",")
    out.write("\n\t")

out.write("}")
