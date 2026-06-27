from flask import Flask, render_template, request, flash
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.secret_key = "myflashsecretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/create" ,methods = ["GET","POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        print(request.files.keys())
        rec_id= request.form.get("uuid")
        desc = request.form.get("text")
        selected_music = request.form.get("music")
        # print(selected_music)
        input_files = []
        for key,value in request.files.items():
            print(key,value)
            #uppload the file
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
                os.makedirs(upload_path, exist_ok=True)

                file.save(os.path.join(upload_path, filename))
                input_files.append(file.filename)
            # capture the description(text) and save it to file    
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id,"desc.txt"),"w") as f:
                f.write(desc)
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "music.txt"),"w") as f:
                f.write(selected_music)   
        for i in input_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id,"input.txt"),"a") as f:
                f.write(f"file '{i}'\nduration 1\n")

        flash("🎉 Reel creation started successfully!")       
    return render_template("create.html",myid=myid)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html",reels = reels)

app.run(host="0.0.0.0", debug=True)
