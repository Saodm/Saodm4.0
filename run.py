from app import app, db
from flask_migrate import Migrate

# 初始化 Flask-Migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)