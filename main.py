from api import init_app
import os

app = init_app()

if __name__ == "__main__":
  app.run(debug=True if os.getenv('FLASK_ENV') == 'development' else False)
