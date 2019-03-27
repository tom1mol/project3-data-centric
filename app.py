import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'project3-data-centric'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
#app.config["MONGO_URI"] = 'mongodb+srv://shoot:<pass>@myfirstcluster-tjr5r.mongodb.net/project3-data-centric?retryWrites=true'

    
mongo = PyMongo(app)


@app.route('/')             # / refers to default route
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find()) 

if __name__ == "__main__":          
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 8080)), 
            debug=True) 



                            #set up ip address and port num
#if __name__ == '__main__':
#    app.run(host=os.environ.get('IP'),
#            port=int(os.environ.get('PORT')),
#            debug=True)