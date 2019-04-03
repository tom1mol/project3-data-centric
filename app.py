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
                                                                        
@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
    categories=mongo.db.categories.find())                     #use find function to fetch categories and pass it back in categories parameter
    
    
@app.route('/insert_task', methods=['POST'])      #add_task submit button. POST is set in top of form in add_task(is why we specify it here)
def insert_task():
    tasks = mongo.db.tasks                      #get the tasks collection from mongo
    tasks.insert_one(request.form.to_dict())    #do a task insert of the request.when we submit info to uri or web location is submitted in                                           form of a request obj. the form is converted into a dictionary(dict) for mongo to understand
    return redirect(url_for('get_tasks'))   #redirect to get_tasks so we can view any changes
    

@app.route('/edit_task/<task_id>')       #wire up edit button
def edit_task(task_id):     #retrieve task from database using. fetching the task that matches task_id and redirect to edittask.html template
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)}) #wrap task_id in objectid
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)
    
    
    
@app.route('/update_task/<task_id>', methods=['POST'])        #POST method hides values from URL bar when being sent across
def update_task(task_id):                                   #pass in task_id às its our hook into primary key
    tasks = mongo.db.tasks                                  #we access tasks collection and then we call update function
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get['task_name'],
        'category_name': request.form.get['category_name'],
        'task_description': request.form.get['task_description'],
        'due_date': request.form.get['due_date'],
        'is_urgent': request.form.get['is_urgent']
    })
    return redirect(url_for('get_tasks'))
    
    
    
@app.route('/delete_task, <task_id>')  
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))
    
    
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())
    
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    
    
    
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name') })
    return redirect(url_for('get_categories'))
    
    
    

if __name__ == "__main__":          
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 8080)), 
            debug=True) 



                            #set up ip address and port num
#if __name__ == '__main__':
#    app.run(host=os.environ.get('IP'),
#            port=int(os.environ.get('PORT')),
#            debug=True)