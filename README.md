# api-dev-python

This is a social-media app where you can create a user, create post, read post, update post and delete post. Also you can like others posts.

# Heroku Deployment

* Install heroku cli for your operating system. This app's development environment is windows.
* run `heroku --version` from your command line to double check
* run `heroku login` and login to your heroku cloud
* run `heroku create [app-name]`
* run `git push heroku main`
* Create a postgresql database instance by running `heroku addons:create heroku-postgresql:essential-0` [see the billing before]
* run `heroku run "alembic upgrade head"`
* enjoy


