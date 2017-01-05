
filename=['a.txt','b.txt','c.txt','d.txt','e.txt','f.txt','g.txt','h.txt','i.txt','j.txt','k.txt','l.txt']
for f in filename:
   with open('/tmp/bar/{}'.format(f),'w`') as FH:
      size=1073741824
      FH.write("ABC"*size)
