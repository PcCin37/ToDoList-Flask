from flask import Flask, session, g
import config
from exts import db, mail
from main import todo_bp # the connecting link in main/__init__.py
from main import user_bp
from flask_migrate import Migrate
from models import UserModel


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(todo_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # combined g with a variety called user and the value is user
            # setattr(g, "user", user)
            g.user = user
        except:
            g.user = None


# request -> before_request -> views -> models in views -> context_processor
        
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}
        

if __name__ == '__main__':
    app.run()
