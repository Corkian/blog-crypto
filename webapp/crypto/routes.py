from flask import render_template, Blueprint
from webapp import db, scheduler
from webapp.db_models import Crypto
from .crypto_api import get_crypto_info

cryptos_bp = Blueprint('crypto', __name__)


@cryptos_bp.route("/crypto")
def crypto():
    query = db.session.query(Crypto).all()
    return render_template("crypto.html", query=query)


@scheduler.task('interval', id='update', minutes=1, misfire_grace_time=900)
def update():
    cryptos = get_crypto_info()
    app = scheduler.app
    with app.app_context():
        if db.session.query(Crypto).first() is None:
            for crypto in cryptos:
                cryptocurrency = Crypto(name=crypto['name'], symbol=crypto['symbol'], price=crypto['price'],
                                        percent_change_24h=crypto['percent_change_24h'],
                                        market_cap=crypto['market_cap'])
                db.session.add(cryptocurrency)
        else:
            for crypto in cryptos:
                for row in Crypto.query:
                    if row.name == crypto['name']:
                        row.price = crypto['price']
                        row.percent_change_24h = crypto['percent_change_24h']
                        row.market_cap = crypto['market_cap']

        db.session.commit()
