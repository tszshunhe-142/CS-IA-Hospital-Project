"""Allow the app to be started with ``python -m app``."""

from app import create_app

app = create_app()
app.run(debug=True)
