import sqlite3
from flask import current_app, g,request

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(                    # Connectionオブジェクトの作成
            current_app.config['DATABASE'],        # DBの設定キー
            detect_types=sqlite3.PARSE_DECLTYPES   # 戻り値のカラムの型を読み取る
        # gはdbの接続情報を保持するディクショナリ
        # g.db = sqlite3.connect(
        # # ’current_app’はアプリケーション本体の情報や設定の為のメソッドを備えたオブジェクト
        # 'user_db'
        # # この定数は戻り値の絡むの宣言された型を読み取る
        # # detect_types=sqlite3.parase_decltypes
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """DBの切断"""
    db = g.pop('db', None)

    if db is not None:
        db.close()

# 古いアプリを破棄し、初期化する。
def init_app(app):
    app.teardown_appcontext(close_db)
