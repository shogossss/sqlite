from flask import Flask
import os

def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
    secret_key='temp',
    DATABASE=os.path.join(app.instance_path,'user_db')
    )
    # instanceフォルダがあるか確認
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import users
    app.register_blueprint(users.bp)

    import userdb
    userdb.init_app(app)


    return app

if __name__ == '__main__':
    app=create_app()
    app.run(host="localhost")
