import datetime

file2=open('data2.txt','w')
with open('data.txt','r') as file:
    for line in file:
        line=line.strip()
        if line=='' or line==None: continue
        try:
            date=datetime.datetime.strptime(line, '%Y-%d-%m')
        except ValueError:
            try:
                date=datetime.datetime.strptime(line, '%m/%d/%Y')
            except Exception:
                continue
        print date.strftime('%Y-%m-%d')
        line=date.strftime('%Y-%m-%d')
        file2.write(line+'\n')
file.close()
file2.close()
