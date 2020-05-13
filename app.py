import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from flask_migrate import Migrate

# Stuff to render my README.md on the home page
import markdown
import markdown.extensions.fenced_code  # Supports GitHub's backtick (```code```) blocks
import markdown.extensions.codehilite   # Code highlighting: Python, JSON
from pygments.formatters import HtmlFormatter

from models import setup_db, Company, Policy


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)   # Allow all origins

    # Set up the database first
    setup_db(app)

    # FIXME:  migrate = Migrate(app, db)  ?

    # Handle routes here
    # FIXME: Handle all routes without any authorization enforcement yet

    @app.route('/')
    def index():
        # https://dev.to/mrprofessor/rendering-markdown-from-flask-1l41
        readme = open("README.md", "r")
        md_template_string = markdown.markdown(
            readme.read(), extensions=["fenced_code", "codehilite", "tables"]
        )

        # Generate css for syntax highlighting
        formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
        css_string = formatter.get_style_defs()

        # Builds embedded CSS styling without a static file
        md_css_string = "<style>" + css_string + "</style>"

        md_template = md_css_string + md_template_string
        return md_template


    @app.route('/company')
    def get_companies():
        co_list = []
        companies = Company.query.all()
        for co in companies:
            # # get policy objects for that company
            # policies = co.policies
            # pol_list = []
            # # go through them all and add to a list of policy ids company uses
            # # e.g. pol_list = [3, 4] includes a Disclaimer and a Privacy Policy
            # for pol in policies:
            #     pol_list.append(pol.id)

            co_list.append({
                "name": co.name,
                "website": co.website,
                "id": co.id,
                # "policies": pol_list
            })

        # Build overall response
        data = {
            "companies": co_list,
            "success": True
        }
        return jsonify(data)


    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)