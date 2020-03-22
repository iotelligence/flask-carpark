from app import app, db
from app.models import Carpark


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Carpark': Carpark}
