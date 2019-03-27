import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

            #add mongo db name and the url linking to that database
app.config["MONGO_DBNAME"] = 'project3-data-centric'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
#app.config["MONGO_URI"] = 'mongodb+srv://shoot:<pass>@myfirstcluster-tjr5r.mongodb.net/project3-data-centric?retryWrites=true'

    
mongo = PyMongo(app)                                #create instance of pymongo. add app into it with method called constructor method

#make connection to database. create a function with a decorator that includes a route to that function
#routing is a string that when we attach it to a url..will redirect to a particular function in a flask application
#in case below we use a string called get_tasks. we create a function with that decorator using app.route. we add it on below the default route('/')
@app.route('/')             # / refers to default route         #decorator
@app.route('/get_tasks')     #this one is default               #decorator
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())   #redirect to existing template called tasks.html
                                                                        #also a tasks collection which is returned by making call directly to mongo
                                                                        #.tasks is a collection

if __name__ == "__main__":          
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 8080)), 
            debug=True) 



                            #set up ip address and port num
#if __name__ == '__main__':
#    app.run(host=os.environ.get('IP'),
#            port=int(os.environ.get('PORT')),
#            debug=True)