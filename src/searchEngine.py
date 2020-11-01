import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import math

# query = input melalui search bar
query = input("Masukkan query: ")

# mengubah input menjadi lower case dan menghilangkan karakter "?", ".", ";", ":", "!", ",", "/"
query = query.lower()
query = "".join(c for c in query if c not in ("?", ".", ";", ":", "!", ",", "/"))

# mengambil stopwords fari nltk
stopWords = set(stopwords.words('english'))

# mengubah query yang berbentuk kalimat menjadi berbentuk array of words
tokenizedQuery = word_tokenize(query)

# menghapus kata-kata yang ada di stopwords
filteredQuery = [w for w in tokenizedQuery if not w in stopWords]

# membuat term table
termTable = []

# term = kata-kata yang ada di query
term = []

# queryTable = jumlah masing-masing kata 
queryTable = []

# menghitung jumlah masing-masing kata
for w in filteredQuery:
    if w not in term:
        term.append(w)
        queryTable.append(1)
    else:
        queryTable[term.index(w)] += 1

# menghitung norma query
queryNorm = 0

for i in queryTable:
    queryNorm += i*i

queryNorm = math.sqrt(queryNorm)


# memasukkan term dan queryTable ke termTable
termTable.append(term)
termTable.append(queryTable)

# input nama file
namaFile = input("Masukkan nama file: ")

similarityTable = []

while namaFile != '0' : #berhenti mengambil input jika user memasukkan 0
    # membuka file dan membaca isi file
    file = open(namaFile, 'r')
    tokenizedFile = word_tokenize(file.read())

    # mengubah isi yang berbentuk kalimat menjadi berbentuk array of words
    filteredFile = [w for w in tokenizedFile if not w in stopWords]

    # mengisi tabel dokumen ke-n dengan 0
    fileTable = [0 for i in range (len(termTable[0]))]

    # mengecek apabila kata-kata yang ada di file sama dengan di query
    for w in filteredFile:
        if w in term:
            fileTable[term.index(w)] += 1
        else:
            fileTable.append(1)
            for i in range (len(termTable)):
                if i == 0:
                    termTable[i].append(w)
                else:
                    termTable[i].append(0)


    # menghitung dot product dari query dan file ke-i serta norma file ke-n
    dotProduct = 0
    fileNorm = 0

    for i in range (0, len(fileTable)):
        dotProduct += fileTable[i] * queryTable[i]
        fileNorm += fileTable[i]*fileTable[i]

    fileNorm = math.sqrt(fileNorm)

    fileInfo = []
    # menyimpan similarity dari file ke-i
    fileInfo.append(round((dotProduct/(fileNorm*queryNorm)),2))

    # menyimpan nama file ke-i
    fileInfo.append(namaFile)

    # memasukkan info-info tentang file ke tabel term
    termTable.append(fileTable)
    similarityTable.append(fileInfo)
    namaFile = input("Masukkan nama file: ")

# sort similarityTable
similarityTable = sorted(similarityTable,key=lambda x: x[0], reverse=True)  

for i in range (len(termTable)):
    print(termTable[i])
    
print(similarityTable)

