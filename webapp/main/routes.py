from flask import render_template, request, Blueprint
from webapp.db_models import Blogpost
from .utility import sendContactForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    posts = Blogpost.query.filter(Blogpost.id < 8)

    return render_template('index.html', posts=posts)


@main_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        result = {}
        result['name'] = request.form['name']
        result['email'] = request.form['email'].replace(' ', '').lower()
        result['message'] = request.form['message']

        response = sendContactForm(result)

        return render_template('contact.html', response=response)

    return render_template('contact.html')
