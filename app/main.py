from app import create_app
import os


app = create_app()
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret")

if __name__ == "__main__":
    app.run(debug=True)
