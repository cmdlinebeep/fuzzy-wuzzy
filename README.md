# RoboTerms API
## Programmatically generate website Terms of Service and other Policies

## About
This is my capstone project submission for Udacity's Full-Stack web developer Nanodegree.  

Nowadays, especially with passing of GPDR and other similar legislation, it's important that most commercial websites have a Privacy Policy, Terms of Service, or other site usage restrictions.  Consumers want to know, and deserve to know, what site owners are allowed to do with your data.

Well, you can toss out your lawyer, because the RoboTerms API can quickly and easily generate such policies for your site automatically.  The API is pre-populated with several boilerplate policies to choose from.  Configure your company, and RoboTerms will populate the boilerplate with text specific to your company.

Want to add a new policy to your site?  Easy.  Call the `rendered_policy` endpoint, and just paste the response text to your own site HTML.

![Robot Scholar](https://github.com/cmdlinebeep/roboterms/blob/master/robo-scholar.jpg?raw=true)

### Policies Currently Supported
- Terms of Service.  What are the terms users agree to when they use your site?  Prevent abuse of your site.
- Cookie policy.  Generate text that everyone will click without reading to go away.
- Disclaimer.  Cover your a**.
- Privacy Policy.  Enumerate all the many (many) ways you are willing to sell people's personal information.


## Model Classes
RoboTerms is made of two basic classes, **Company**, and **Policy**.  Companies have one or more Policies (one-to-many database relation).  For example, a company may have a Privacy Policy and also a Terms of Service.

**Company** is essentially an account setup for a particular user.  It contains essential information on the company, like the company name and website.  It also contains a collection of Policies which are essentially instantiated legalese boilerplates.

The **Policy** model contains individual policy boilerplate sections.  For example, there might be an acceptable use policy that a website administrator might add to prohibit users from crawling (spidering/scraping) the site.  A policy contains the boilerplate text that is "rendered" by populating it with company specifics in the display version, for example *"ACME, Inc."* instead of `{COMPANY_NAME}` placholders.


## Roles and Permissions
There are two roles supported by Roles Based Access Control (RBAC), **Clients** and **Admins**.  

**Clients** are essentially the end users of the service.  Clients can read any company profile, can read individual policy boilerplate (generic), and of course can read their finalized (non-generic) final policies for including in their sites.  Clients can also add and remove policies to and from their company.

**Admins** are the administrators of RoboTerms.  They have permissions to read any company profile, read individual policy boilerplate, and are also the only role that has permissions to create, edit, or delete individual policy boilerplate.  Of course, as you'd expect, they do not have permissions to edit company information (for example, which policies a company uses).

*NOTE: Changes to the policy boilerplate are reflected immediately in the next `GET /rendered_policy/<company_id>/<policy_id>`.*


## Authorization
FIXME


## Running the Server Locally
Create a virtual environment, and from within, run:

```bash
source setup.sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, environment variables are exported differently:
```bash
.\setup_windows.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Sourcing setup.sh sets environment variables needed by Auth0 and the Flask app.

To set up the local database with some initial data, run the following:
```bash
createdb -U postgres roboterms
psql -U postgres roboterms < trivia.psql    # FIXME
```

The database can then be explored via:
```bash
psql roboterms postgres
```


## Running the Test Suite
FIXME  use unittest (like class 3), not Postman


## Check out a [live deployment on Heroku](FIXME)


## Endpoint conventions and Error codes
All responses are returned in JSON format and all contain at the very least, a `"success"` key, which will return either `true` or `false`.

When error codes are returned (e.g. `401`, `403`, etc.), they will return in a format like the following 404 example:

```json
{
    "success": false,
    "error": 404,
    "message": "Not found"
}
```


## API Endpoints


The following contains a list of all the endpoints, as well as specific documentation on each one.

| Method | Route                           | Short Description |
|--------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | /                               | Home page with API documentation |
| GET    | /company                        | Returns a list of companies in the database (includes ids) |
| GET    | /policy                         | Returns a list of list of available policy boilerplate |
| GET    | /rendered_policy/`<company_id>`/`<policy_id>` | Returns a company policy, rendered for that company |
| POST   | /company                        | Create a new company.  **Client roles only** |
| DELETE | /company/`<company_id>`         | Deletes a company from the database.  **Client roles only** |
| PATCH  | /policy/`<policy_id>`           | Update the boilerplate text or name for a given policy.  **Admin roles only** |


##  `GET /`
- Displays the home page with this API documentation.  Not intended to be called by API clients, but rather viewed by developers in their browser.
- Request Arguments: None
- Returns: Rendered HTML


## `GET /company`
- Returns a list of companies in the database and accompanying information
- Request Arguments: None
- Returns: A list of JSON company data

```json
{
    "companies": [
        {
            "name": "ACME Inc.",
            "website": "acmerocks.com",
            "id": 1
        },
        {
            "name": "RealCorp LLC.",
            "website": "soooreal.com",
            "id": 2
        },
        ... TRUNCATED FOR BREVITY ...
        {
            "name": "FaceSold",
            "website": "facesold.com",
            "id": 70
        }
    ],
    "success": true
}
```


## `GET /policy`
- Returns a list of available policies (and associated boilerplate) to choose from
- Request Arguments: None
- Returns: A list of JSON policy boilerplate

```json
{
    "policies": [
        {
            "id": 1,
            "name": "Terms of Service",
            "body": "TERMS OF SERVICE    These Terms of Service (\"Terms\") govern your access to and use of the website \"{WEBSITE}\" and all its services. <TRUNCATED>",
        },
        {
            "id": 2,
            "name": "Cookies Policy",
            "body": "COOKIES POLICY    {COMPANY} (\"us\", \"we\", or \"our\") uses cookies on \"{WEBSITE}\" (the \"Service\"). By using the Service, you consent to the use of cookies. <TRUNCATED>",
        },
        ... TRUNCATED FOR BREVITY ...
        {
            "id": 4,
            "name": "Privacy Policy",
            "body": "PRIVACY POLICY    This statement (\"Privacy Policy\") covers the website {WEBSITE} owned and operated by {COMPANY} (\"we\", \"us\", \"our\") and all associated services. <TRUNCATED>",
        }
    ],
    "success": true
}
```


## `GET /rendered_policy/<company_id>/<policy_id>`
- Returns a rendered company policy, with templated placeholders filled in for your company
- Use this endpoint to capture instantiated legalese for pasting into your site
- Request Arguments: `company_id`, `policy_id`
- Returns: Site legalese in JSON format

```json
{
    "policy": "Please heretofore find attached and in no undertain terms the Terms of Service for ACME, Inc. from herein referred to as THE COMPANY and blah blah blah...",
    "success": true
}
```


## `POST /company`
- Create a new company.  Adds a new company to the list and automatically assigns a `company_id`
- **Client roles only**
- Request Arguments: JSON formatted data
- Returns: Success response and `company_id` that was created

Request Body Data:
```json
{
    "name": "Googolplex AtoZ Data",
    "website": "stopdoingevilwheneverconvenient.com"
}
```

Returns:
```json
{
    "id": 52,
    "success": true
}
```


## `DELETE /company/<company_id>`
- Deletes a company from the database
- **Client roles only**
- Request Arguments: None
- Returns: Success status and deleted `company_id`

```json
{
    "id": 52,
    "success": true
}
```


## `PATCH /policy/<policy_id>`
- Update the boilerplate text or name for a given policy.
- **Admin roles only**
- Request Arguments: JSON formatted data
- Returns: Success status

Request Body Data:
```json
{
    "name": "Better Cookie Policy Name",
    "body": "We get it.  You track us and we have to click OK or click 'more options' and lets face it, nobody ever does that.  Does that button even function?"
}
```

Returns:
```json
{
    "success": true
}
```