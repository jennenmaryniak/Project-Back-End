from flask import request, url_for, render_template, redirect
from flask_api import FlaskAPI, status, exceptions
import secrets 


app = FlaskAPI(__name__)

user_token_db = []



def db_has_user(credentials):
    """
    db_has_user checks to see if a dictionary exists in this fake database.
    """
    fake_db = [  {"user": "jennen", "password": "foo"},  {"user": "harsha", "password": "hi"}, {"user": "alec", "password": "bar"}, {"user": "rui", "password": ""} ]
    if credentials in fake_db:
        return True
    return False 

@app.route("/api/auth_user", methods=['GET', 'POST'])
def auth_user():
    """
    Checks for a username AND password and then authorizes it, assigning the user to a randomly generated string.
    """

    if request.method == 'POST':
        user = str(request.data.get('user', ''))
        if user == '': 
            return {"error": "empty user"}, status.HTTP_406_NOT_ACCEPTABLE

        pw = str(request.data.get('password', ''))
        if pw == '':
              return {"error": "empty pass"}, status.HTTP_406_NOT_ACCEPTABLE  

        if db_has_user({'user': user, 'password': pw}):
            token = secrets.token_urlsafe(10)
            user_token_db.append({'user': user, 'token': token})
            return {'token': token}, status.HTTP_202_ACCEPTED
        else:
            return {}, status.HTTP_401_UNAUTHORIZED

    return {"error": "expected POST"}, status.HTTP_406_NOT_ACCEPTABLE

         
@app.route('/api/<user>/<token>')
def reroute(user=None, token=None):
    """
    This takes an already created 'user' and the corresponding token and will reroute the webpage to show the user's profile. We can set different .html files for each different user essentially.
    """
    if {'user': user, 'token': token} in user_token_db:
        return render_template('pro.html', user=user)

@app.route('/home')
def home():
    return "This is the home page"
    """A basic home route
    """

@app.route('/admin')
def administrator():
    return redirect(url_for('home'))
    """This was a route we used for testing and showcasing how redirect works
    """
    
if __name__ == "__main__":
    app.run(debug=True)

