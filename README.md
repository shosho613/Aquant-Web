Aquant Fault Tree Evaluator
========

## To Run:
`heroku ps:scale web=1`  
`heroku open`  

## To Build:
`cd frontend`  
`npm run build`  
Place js and css files in static directory.  
Replace the names of the of the js and css files in the `index.html` file in the templates directory. 


## To Run Locally:
`pip install -r requirements.txt`  
`python aquantweb.py`  
Or, to use `gunicorn`  
`gunicorn wsgi:application`
