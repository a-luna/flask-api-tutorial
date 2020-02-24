# flask-api-tutorial

Hello! This project is the application documented in a tutorial series on my website: [How To: Create a Flask API with JWT-Based Authentication](https://aaronluna.dev/series/flask-api-tutorial/overview/)

This can be used as boilerplate for any REST API project that is built on Flask, SQLAlchemy, Swagger UI and pytest. My goal is to provide a REST API that is secured via JSON Web Tokens (JWT) and is robust and secure enough for use in a real-world, production application. The most important packages/extensions used by the application are:

- `Flask-RESTx`
- `Flask-SQLAlcheny`
- `Flask-Migrate`
- `PyJWT`
- `Pytest`
- `Tox`

Throughout the tutorial series the importance of developing automated test coverage is emphasized, along with explanations for configuring several `pytest` plugins that enforce code style/format, perform linting, calculate test coverage, etc.

Ensuring that your test cases are executed against your code as it would be installed by an end-user, **and not against the code in your local development environment** is explained and accomplished with `tox`.

Deploying the application as part of a CICD system is demonstrated for Github Actions and Azure Pipelines.

The methodology and step-by-step process of implementing this application is [documented as a tutorial series on my website](https://aaronluna.dev/series/flask-api-tutorial/overview/). Please check it out if you would like to learn how it was built.

Feedback can be provided either by creating a new issue here or by commenting on the article series on my website.
