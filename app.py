'''
做一個簡單的伺服器
'''
import flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    """
    這個函式會回傳 "Hello World!" 字串
    """

    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)

