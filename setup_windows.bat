REM Of course, Windows is different!
REM Run ./setup_windows.bat if on Windows
set AUTH0_DOMAIN='http://<FIXME>.auth0.com'
set ALGORITHMS='RS256'
set API_AUDIENCE='<FIXME>'
set CLIENT_ID='<FIXME>'

set client_token=FIXME
set admin_token=FIXME

set DATABASE_URL=postgres://postgres:a@localhost:5432/roboterms

set FLASK_APP=app.py
set FLASK_ENV=development