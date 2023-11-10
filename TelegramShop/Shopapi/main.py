import flask
import sql
import util
from flask import Flask, jsonify, request, render_template, redirect, url_for

app = flask.Flask(__name__)
db = sql.connect()
app.config["DEBUG"] = False


@app.route('/good/<int:go>/id/<int:id>', methods=['GET'])
def update_user_basket(go, id):
    try:
        sql.put_good_in_busket(db, go, id)
        util.write_log(' Добавлен товар ' + str(go) + ' В корзину ' + str(id))
        return jsonify({'CODE': '200',
                        'go': go,
                        'id': id})
    except:
        util.write_bug('Не добавлен товар ' + str(go) + ' В корзину ' + str(id))



if __name__ == '__main__':
    app.run(debug=False)