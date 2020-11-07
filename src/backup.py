# Fungsi yang me-return tabel
def displayTable(query):
    # inisialisasi database
    database = r"files.db"
    conn = connect(database)

    # characters yang tidak diperlukan
    characters = ["?", ".", ";", ":", "!", ",", "/", "&", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

    # mengubah input menjadi lower case dan menghilangkan karakter yang tidak diperlukan
    query = query.lower()
    query = "".join(c for c in query if c not in characters)

    # mengambil stopwords dari nltk
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

    similarityTable = []

    # Mengambil file yang ada di database dan dimbuat menjadi array
    fileData = selectFiles(conn)

    for files in fileData: # iterasi file yang ada di array fileData
        # Membaca data file dari database
        # Harus diencoding soalnya bentuk data berupa byte
        tokenizedFile = word_tokenize(files[1].decode('utf-8'))

        # mengubah isi yang berbentuk kalimat menjadi berbentuk array of words dan membersihkan dari karakter2 yang tidak perlu
        filteredFile = [w for w in tokenizedFile if not w in stopWords and not w in characters]

        # mengisi tabel dokumen ke-n dengan 0
        fileTable = [0 for i in range (len(termTable[0]))]

        # mengecek apabila kata-kata yang ada di file sama dengan di query
        for w in filteredFile:
            # Mengubah kata-kata di file menjadi lowercase
            w = w.lower()

            if w in term:
                fileTable[term.index(w)] += 1
            else:
                fileTable.append(1)
                for i in range (len(termTable)):
                    if i == 0:
                        termTable[i].append(w)
                    else:
                        termTable[i].append(0)
        # End for


        # menghitung dot product dari query dan file ke-i serta norma file ke-n
        dotProduct = 0
        fileNorm = 0

        for i in range (0, len(fileTable)):
            dotProduct += fileTable[i] * queryTable[i]
            fileNorm += fileTable[i]*fileTable[i]
        # End for

        fileNorm = math.sqrt(fileNorm)

        fileInfo = []
        # menyimpan similarity dari file ke-i
        fileInfo.append((dotProduct/(fileNorm*queryNorm)))

        # menyimpan nama file ke-i
        fileInfo.append(files[0])

        # memasukkan info-info tentang file ke tabel term
        termTable.append(fileTable)
        similarityTable.append(fileInfo)

    # End for
    # mentranspose termTable
    NTerm = len(termTable[0])
    kolom = len(termTable)
    table = [[0 for j in range (kolom) ] for i in range (NTerm)]
        
    for i in range (NTerm):
        for j in range (kolom):
            table[i][j]=termTable[j][i]
    # sort table
    table = sorted(table,key=lambda x:x[0])
    return (table)