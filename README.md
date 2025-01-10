# api-dev-python

This is a social-media app where you can create a user, create post, read post, update post and delete post. Also you can like each-others posts.

# Run locally:

Clone the repository by

`git clone https://github.com/liumOazed/api-dev-python.git`

Create `venv` by following command

`Py -3 -m venv "your venv name"`

Run the following command:

`pip install -r requirements.txt`

Then run 

`fastapi dev app/main.py`

Now you can access the app in your browser:

`http://127.0.0.1:8000/docs`


# Heroku Deployment

* Install heroku cli for your operating system. This app's development environment is windows.
* run `heroku --version` from your command line to double check
* run `heroku login` and login to your heroku cloud
* run `heroku create [app-name]`
* run `git push heroku main`
* Create a postgresql database instance by running `heroku addons:create heroku-postgresql:essential-0` [see the billing before]
* run `heroku run "alembic upgrade head"`
* enjoy


