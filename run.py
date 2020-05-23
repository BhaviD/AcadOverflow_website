from app import app

app.secret_key = 'secret123'
app.run('127.0.0.1','8889',debug=True)
