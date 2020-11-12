import os
import sqlite3
from searchEngine import searchEngine
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField


app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdefg"

# Route untuk halaman upload
@app.route("/upload", methods=["GET", "POST"])
def upload():
    upload = UploadForm()
    if(request.method == "POST"):
        if upload.validate_on_submit():
            uploaded_file = upload.file.data
            database(name=uploaded_file.filename, data=uploaded_file.read())
            return render_template("upload.html", upload=upload)
    return render_template("upload.html", upload=upload)

class UploadForm(Form):
    file = FileField()
    submit = SubmitField("Upload File")

def database(name, data):
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS file_table (name TEXT, data BLOP) """)
    cursor.execute(""" INSERT INTO file_table (name, data) VALUES (?,?) """, (name, data))

    conn.commit()
    cursor.close()
    conn.close()

# Route untuk halaman searching
@app.route("/search", methods=["POST", "GET"])
def search():
    search = SearchQuery(request.form)
    if(request.method == "POST"):
        # Kalo user input query, web akan pindah ke /results
        return results(search)
    return render_template("search.html", search=search)

class SearchQuery(Form):
    query = StringField("")
    submit = SubmitField("Search")

# Route untuk halaman hasil searching
@app.route("/results")
def results(search):
    # Run fungsi searchEngine dari searchEngine.py
    (results, tableresults, documents) = searchEngine(search.data['query'])
    
    return render_template("result.html", query=search.data['query'], results=results, length=len(results), tableresults=tableresults, NTerm=len(tableresults),kolom=len(tableresults[0]),documents=documents)

# Route untuk landing page
@app.route("/")
def landingpage():
    return render_template("index.html")

# Ambil satu text
def get_file(filename):
    database = r"files.db"
    conn = sqlite3.connect(database)
    file = conn.execute('SELECT * FROM file_table WHERE name = ?',
                        (filename,)).fetchone()
    conn.close()
    #if file is None:
    #    abort(404)
    return file

# Route untuk setiap text
@app.route('/<filename>')
def showtext(filename):
    file = get_file(filename)
    content = file[1].decode('utf-8')
    return render_template("text.html",file=file,filename=filename, content=content)

if(__name__ == "__main__"):
    app.run(debug=True)