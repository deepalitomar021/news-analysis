from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('all')
from nltk.tokenize import sent_tokenize, word_tokenize
import psycopg2
import re
import urllib

app = Flask(__name__)
app.secret_key = b'1122'
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='21466463081-btqrll8176rp1hseikvsg2pst8bn3cga.apps.googleusercontent.com',
    client_secret='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',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    refresh_token_params=None,
    redirect_uri='http://127.0.0.1:5000/history',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/login')
def login():
    redirect_uri = url_for('history', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    # Here, you can check if the user_info corresponds to an admin user in your system
    # If it does, log in the user
    session['user_info'] = user_info
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_info' in session:
        user_info = session['user_info']
        return render_template('dashboard.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_info', None)
    return redirect(url_for('login'))


# Database connection
conn = psycopg2.connect(host="localhost",database="dhp2024",user="postgres",password="dp15#21/L@")
cur = conn.cursor()

# Create table if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS news_data
               (id SERIAL PRIMARY KEY,
                url TEXT,
                news_text TEXT,
                num_sentences INT,
                num_words INT,
                num_stopwords int,
                pos_tags TEXT,
                news_category text)''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    
    url = request.form['url']
    if url.startswith('https://timesofindia.indiatimes.com/') and requests.head(url).status_code==200:
      
        # Extract news text
    
        html=urllib.request.urlopen(url).read().decode('utf8')
        # Extract news text
        soup = BeautifulSoup(html, 'html.parser')
    

        head=soup.find_all('h1')

        main_div=soup.findAll("div", class_="_s30J clearfix")

        All_text=head+main_div
        news_text=''
        for i in All_text:
            raw_html=str(i)
            cleantext=re.sub(r'<.*?>', '',raw_html)
            news_text+=cleantext
        # Clean news text (You can implement your own cleaning method here)
        lst1=[]
        while len(lst1)!=2:
            n=36
            for i in range(36,70):
                if url[i]=='/':
                    lst1.append(url[n:i])
                    n=i+1
        str1=''
        for i in lst1:
            str1=str1+' =>'+i

        # Analyze text
        sentences = sent_tokenize(news_text)
        words = word_tokenize(news_text)
        num_sentences = len(sentences)
        num_words = len(words)
        #pos_tags = pos_tag(words)
            # Remove stopwords
        stop_words = set(nltk.corpus.stopwords.words('english'))
        count_stopWords=0
        for i in words:
            if i.lower() in stop_words:
                count_stopWords+=1

        dict_pos={}
        for i in nltk.pos_tag(words,tagset='universal'):
            if i[1] not in dict_pos.keys():
                dict_pos[i[1]]=1
            else:
                dict_pos[i[1]]+=1

        # dict_pos=json.dumps(dict_pos)
        # Store data in database
        cur.execute('''INSERT INTO news_data (url, news_text, num_sentences, num_words,num_stopwords, pos_tags, news_category)
                        VALUES (%s, %s, %s, %s, %s,%s,%s)''',
                        (url, news_text, num_sentences, num_words, count_stopWords, str(dict_pos), str1))
        conn.commit()
        # redirect(url_for('login'))
        return render_template('analysis.html', url=url,news_text=news_text,num_sentences=num_sentences, num_words=num_words, count_stopWords=count_stopWords,dict_pos=str(dict_pos),str1=str1)
    
    else:
        message="Please Enter a valid URL of Times of India"
        return render_template('index.html',message=message)

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin_1234"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def sub():
    # Your code for extracting and analyzing news text goes here
    pass
@app.route("/login_page")
def login_page():
    return render_template('login.html')

@app.route('/history')
def history():
    # Fetch history from database
    cur.execute("SELECT * FROM news_data")
    history = cur.fetchall()
    return render_template('history.html', history=history)

@app.route('/Admin_login', methods=['GET', 'POST'])
def Admin_slogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['email'] = email
            return redirect(url_for('history'))
        else:
            return render_template('login.html', message='Invalid email or password.')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
