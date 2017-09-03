BrewLocker is a bulletin board made for barista for  exchanging barista tools and accessories.
A user can log in with his Facebook, Google or GitHub accounts: the app doesn't store passwords or other sensitive information. Both authorised and unauthorised can view the list of all items on the main page and the item page with full description, but only authorized user can access author's contact info. 
Logged in user can also create new items on board and upload photos of them. He can later edit and delete created items, add new or delete existing photos from the item page.


The application is built on flask framework and use:
- App factory to create multiple instances of the app and blueprints to separate app context
- SQLalchemy as a Python DB-API and Alembic to store versions of DB schema
- Jinja2 for templates
- WTForms and Flask-WTForms for form validation and CSRF protection
- Flask-Login to store user session and Rauth for implementing fully backend oauth2 authorisation
- Flask-Upload to manage uploaded images
- Gulp.js to run background tasks such as resizing and compression for uploaded images
- Foundation to create grid system and interface elements


To deploy locally:
- Install [Node.js](https://nodejs.org/en/download/), [npm](https://docs.npmjs.com/getting-started/installing-node) and Gulp `npm install gulp-cli -g`
- Clone repository
- Open Terminal in the project directory
- Create virtual environment `virtualenv venv`
- Activate virtual environment `source venv/bin/activate`
- Install dependencies `pip install -r requirements/dev.txt
- Run `python manage.py deploy` to prepare flask app
- Run `npm install --save-dev` to resolve dependencies
- Run `gulp default` to start background tasks
- Run server `python manage.py runserver` on localhost:5000


To run tests:
- Execute `python manage.py test`


To generate fake data:
- Start server and login with any provider
- Activate shell `python manage.py shell`
- Generate fake data with `User.generate_fake()` and `Item.generate_fake()`


To test admin privileges:
- Set admin mail address in the config `export BREWLOCKER_ADMIN=*mail address connected to oauth provider you use*`
- Start the server and login with provider accociated with BREWLOCKER_ADMIN mail address


To set up admin mail notifications:
- Set up gmail smtp `export MAIL_USERNAME=`, `export MAIL_PASSWORD=`
