from flask import Flask, request, jsonify,send_file,send_from_directory, abort


app = Flask("__name__")

@app.route("/")
def landing():
    
    data = {
        "First-page": "this",
    }
    return jsonify(data), 200

@app.route("/get-data")
def get_data():
    
    data = {
        "Name": "Prateek",
        "Department" : "QA",
        "Experience" : 2,
        "Is-Employee" : True
    }

    return jsonify(data), 200

@app.route("/create-data", methods=["POST"])
def create_data():
       data = request.get_json()

       return jsonify(data), 201 


# DOWNLOAD_DIRECTORY = "D:\6x\RingTones\Baby Calm Down - Instrumental Music.wav"

# @app.route('/get-files',methods = ['GET','POST'])
# def get_files():

#     """Download a file."""
#     try:
#         return send_from_directory(DOWNLOAD_DIRECTORY, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)



if __name__== "__main__":
    app.run(debug=True)