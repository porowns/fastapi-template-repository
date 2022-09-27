# Professional Template for FastAPI

Template repository with professional guidelines. Good enough to pass the technical lead sniff test for a deployed public company Minimum Viable Product.

You'll likely need to add an ORM like SqlAlchemy or Tortoise.

When breaking this out of the MVP stage,

- Add migrations for your ORM or SQL schema (e.g Alembic, DBMate)
- Add a pipeline (e.g CircleCI)
- Add system tests with Postman
- Add load tests with K6
- Add authentication (OAuth 2.0, if you're bandwidth constrained use Auth0)

# Tenants

## Monitoring

Professional applications need real monitoring.

- Sentry.io (performance dashboard, error monitoring)
- LogDNA (remote logging)
- Request ID and Correlation ID injected into every request

New Relic and Datadog are stronger alternatives, but expensive. If you need these for your business, simply rip out the Sentry and LogDNA components and add them.

## Code quality

If you're going to use Python, you need robust linting, and it needs to run every time an engineer commits to a repository using [Pre Commit](https://pre-commit.com/).

- PyLint
- Flake
- Isort
- Mypy
- Black
- Bandit

## Containerization

It's 2022. Your application needs to be containerized so that it can be pushed to ECS, EKS, Cloud Run, or whatever proprietary flavor of Kubernetes you're choosing.

My flavor is Docker, but containerd is getting more popular.

## Local environment

Engineers need a local environment to run against, something that stands up all of your dependencies.

My flavor is Docker Compose, if you're using containerd then look at nerdctl.

# Repository Structure

Recommended repository structure is going to change depending on what kind of API you're building.

If you're building monolithic or SOA services, I'd follow something close to Django's repository pattern.

```
api/
   main.py
   customers/
    router.py
    schemas.py
    models.py
    routes/
        v1.py
        v2.py
    tests.py
   orders/
    router.py
    schemas.py
    models.py
    routes/
        v1.py
        v2.py
   payments/
    router.py
    schemas.py
    models.py
    routes/
        v1.py
        v2.py
    ... many more apps
```

If you're building leaner microservices, I'd follow something close to the traditional FastAPI repository pattern.

```
api/
    main.py
    routes/
        v1/
            customers.py
            orders.py
            payments.py
        v2/
            customers.py
    tests/
        v1/
            test_customers.py
            test_orders.py
            test_payments.py
        v2/
            test_customers.py
    models.py   # Could be broken into a folder, but are you lean at that point?
    schemas.py  # Could be broken into a folder
```
