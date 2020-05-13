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

    @app.route('/', methods=['GET'])
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


    @app.route('/companies', methods=['GET'])
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
                "id": co.id,
                "name": co.name,
                "website": co.website
                # "policies": pol_list
            })

        # Build overall response
        data = {
            "companies": co_list,
            "success": True
        }
        return jsonify(data)

    
    @app.route('/policies', methods=['GET'])
    def get_policies():
        pol_list = []
        policies = Policy.query.all()
        for pol in policies:
            pol_list.append({
                "id": pol.id,
                "name": pol.name,
                "body": pol.body
            })
        
        data = {
            "policies": pol_list,
            "success": False
        }
        return jsonify(data)
    

    @app.route('/rendered_policy/<int:company_id>/<int:policy_id>', methods=['GET'])
    def get_rendered_policy(company_id, policy_id):
        company = Company.query.get(company_id)
        if not company:
            abort(404)
            # FIXME: add API error handler here
        
        policy = Policy.query.get(policy_id)
        if not policy:
            abort(404)
            # FIXME: add API error handler

        # Fill in the placeholders {COMPANY} and {WEBSITE} with real data
        rendered_policy = policy.body.format(COMPANY=company.name, WEBSITE=company.website)

        data = {
            "policy": rendered_policy,
            "success": True
        }
        return jsonify(data)

    
    @app.route('/company', methods=['POST'])
    def add_company():
        # FIXME: client role only
        body = request.json

        # Need to have name and website keys in body
        if not all([ x in body for x in ['name', 'website'] ]):
            abort(422)
            # FIXME: make error handlers API form
        
        new_co = Company(name=body['name'].strip(), website=body['website'].strip())

        try:
            new_co.insert()
        except Exception as e:
            print(f'Exception in add_company(): {e}')
            abort(422)  # Syntax is good, can't process for semantic reasons

        return jsonify({
            "id": new_co.id,
            "success": True
        })

    
    @app.route('/company/<int:company_id>', methods=['DELETE'])
    def delete_company(company_id):
        # Get the company to delete
        goner_co = Company.query.get(company_id)
        if not goner_co:
            abort(404)
        
        id = goner_co.id    # Will lose this after delete

        try:
            goner_co.delete()
        except Exception as e:
            print(f'Exception in delete_company(): {e}')
            abort(422)

        return jsonify({
            "id": id,
            "success": True
        })
        
    
    @app.route('/policy/<int:policy_id>', methods=['PATCH'])
    def edit_policy(policy_id):
        # Get the policy to edit
        policy = Policy.query.get(policy_id)
        if not policy:
            abort(404)  # FIXME
        
        body = request.json

        # Check for name and body keys in the request payload
        # Here it's allowable to only update one, or both, entries
        if not any([ x in body for x in ['name', 'body'] ]):
            abort(422)

        if 'name' in body:
            policy.name = body['name']
        if 'body' in body:
            policy.body = body['body']  # whoah
        
        try:
            policy.update()
        except Exception as e:
            print(f'Exception in edit_policy(): {e}')
            abort(422)
        
        return jsonify({
            "success": True
        })


    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)