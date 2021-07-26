from flask import Flask, redirect, url_for,render_template,request
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from load_twitter_data import *
from dotenv import load_dotenv
import os

### initializing the app configuration
app = Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



twitter_blueprint = make_twitter_blueprint(api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))



app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')



db = SQLAlchemy(app)



### User class to store the data in the below mentioned format
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.Text)
    created_date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'tweet': self.tweet,
            'created_date': self.created_date
        }

db.create_all()


## endpoint for user authentication
@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    try:
        account_info = twitter.get('account/settings.json')
        account_info_json = account_info.json()
        get_data = load_data()
        get_data.load_twitter_dat(account_info_json['screen_name'])
        return redirect(url_for('index',user_name= account_info_json['screen_name']))
    except NoResultFound:
        return '<h1>Request Failed</h1>'
 



## endpint to give data to template in dictionary format
@app.route('/api/data')
def data():
    return {'data': [user.to_dict() for user in User.query]}


## index endpoint to view the data table
@app.route('/')
def index():
    return render_template('data_table.html', title='Twitter User Timeline', user_name=request.args.get('user_name'))




if __name__ == '__main__':
    app.run(debug=True)