from flask import Flask, render_template, redirect, request, url_for, flash
import time
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


app.config["SECRET_KEY"] = "Your secret key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTS = {"txt", "jpeg", "jpg", "png","TXT","JPEG","JPG","PNG"}

def check_file(file):
    return file.endswith(tuple(ALLOWED_EXTS))


@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    error = None
    filename = None

    if request.method == "POST":
        if "file" not in request.files:
            error = "File not selected"
            return render_template("form.html", error = error)
        
        file = request.files['file']
        filename = file.filename

        if filename =='':
            error = "File name is empty."
            return render_template("form.html", error = error)
        
        if check_file(filename) == False:
            error = "This file is not supported."
            return render_template("form.html",error = error)
        
        start_time = time.time()
        
        file.save(os.path.join("/coding/something/uploads",filename))

        end_time = time.time()

        filesize = os.path.getsize(os.path.join("/coding/something/uploads",filename)) / (1024 * 1024)

        upload_time = end_time - start_time

        upload_speed = (filesize * 8 ) / upload_time

        flash(f"File uploaded successfully!", "success")
        flash(f"File Size: {round(filesize, 2)} MB", "info")
        flash(f"Upload Time: {round(upload_time, 2)} seconds", "info")
        flash(f"Upload Speed: {round(upload_speed, 2)} Mbps", "info")

        return redirect(url_for("form"))



    return render_template("form.html", error=error,filename = filename)


if __name__ == "__main__":
    app.run(debug=True)
