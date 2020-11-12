import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import math
import sqlite3
from sqlite3 import Error

def connect(db_file):
    # membuat koneksi ke database SQLite
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def selectFiles(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM file_table")

    return cur.fetchall()

def countWords(file):
    # Membaca data file dari database
    # Harus diencoding soalnya bentuk data berupa byte
    tokenizedFile = word_tokenize(file.decode('utf-8'))

    # menghitung wordcount
    return(len(tokenizedFile))

def searchEngine(query):
    # inisialisasi database
    database = r"files.db"
    conn = connect(database)

    # Mengambil file yang ada di database dan dimbuat menjadi array
    fileData = selectFiles(conn)

    # characters yang tidak diperlukan
    characters = ["?", ".", ";", ":", "!", ",", "/", "&", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

    # mengubah input menjadi lower case dan menghilangkan karakter yang tidak diperlukan
    query = query.lower()
    query = "".join(c for c in query if c not in characters)

    # mengambil stopwords dari nltk
    stopWords = set(stopwords.words('english'))

    # mengubah query yang berbentuk kalimat menjadi berbentuk array of words
    tokenizedQuery = word_tokenize(query)

    # memeriksa apakah semua query stopword
    """
    allStopWords = True
    i = 0
    while(not allStopWords and i < len(tokenizedQuery)):
        if(not(tokenizedQuery[i] in stopWords)):
            allStopWords = False
        else:
            i += 1
    """
    set_tokenizedQuery = set(tokenizedQuery)
    allStopWords = set_tokenizedQuery.issubset(stopWords)

    similarityTable = []
    
    if(allStopWords):
        for files in fileData:
            fileInfo = []
            
            # menyimpan similarity dari file ke-i
            fileInfo.append(0)

            # menyimpan nama file ke-i
            fileInfo.append(files[0])

            # menyimpan word count file ke-i
            fileInfo.append(countWords(files[1]))

            # menyimpan kalimat pertama file ke-i
            fileInfo.append(files[1].decode('utf-8').partition('.')[0] + '.')

            # Menyimpan similarityTabele
            similarityTable.append(fileInfo)

        # return similarityTable dan termtable kosong, dan documents juga kosong
        return (similarityTable, [[]],[]) 
    else:
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

        
        for files in fileData: # iterasi file yang ada di array fileData
            # Membaca data file dari database
            # Harus diencoding soalnya bentuk data berupa byte
            tokenizedFile = word_tokenize(files[1].decode('utf-8'))

            # menghitung wordcount
            wordCount = countWords(files[1])

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
            fileInfo.append(files[0])

            # menyimpan word count file ke-i
            fileInfo.append(wordCount)

            # menyimpan kalimat pertama file ke-i
            fileInfo.append(files[1].decode('utf-8').partition('.')[0] + '.')

            # memasukkan info-info tentang file ke tabel term
            termTable.append(fileTable)
            similarityTable.append(fileInfo)
        
        # End for

       # membuat array berisi judul dokumen, sesuai dengan urutan pada database
        documents = []
        for i in range(len(similarityTable)):
            documents.append(similarityTable[i][1])

        # sort similarityTable berdasarkan nilai similaritas
        similarityTable = sorted(similarityTable,key=lambda x: x[0], reverse=True) 
        
        # mentranspose termTable
        NTerm = len(termTable[0])
        kolom = len(termTable)
        sortedTermTable = [[0 for j in range (kolom) ] for i in range (NTerm)]
            
        for i in range (NTerm):
            for j in range (kolom):
                sortedTermTable[i][j]=termTable[j][i]
                
        # sort sortedTermTable berdasarkan term
        sortedTermTable = sorted(sortedTermTable,key=lambda x:x[0])
        
        return (similarityTable, sortedTermTable, documents) 

