import json
import os
from flask import request, Flask

app = Flask(__name__)

# Routes


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)