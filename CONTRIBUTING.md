# Welcome

It's great that you are taking time to contribute to this project. If that
means you find a bug, triage an issue, write a client or contribute directly to
the project - we thank you! All contributors who desire will be given equal
access to the project and will be unconditionally made members of the
organisation. Once you hang around for a while, you'll get deployment access.

We try to adhere to our [code of conduct].

[code of conduct]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/blob/master/CONDUCT.md

Just [submit a pull request] as you normally would. We use [Travis CI] for our
continuous integration, and each pull request submitted will undergo various
tests to help assert the correctness of it. A maintainer will try to review
your change set as soon as possible.

Please complain in [the lobby] if no one is responding.

[submit a pull request]: https://help.github.com/articles/creating-a-pull-request/
[Travis CI]: https://travis-ci.org/
[the lobby]: https://gitter.im/giving-a-fuck-about-climate-change/Lobby

# Table of Contents
  * [Getting Started](#getting-started)
    * [Get a Local Copy](#get-a-local-copy)
    * [Configure the Environment](#configure-the-environment)
    * [Install JavaScript Dependencies](#install-javascript-dependencies)
    * [Install Python Dependencies](#install-python-dependencies)
    * [Install System Dependencies](#install-system-dependencies)
    * [Setup the Database](#setup-the-database)
  * [Commence Hacking](#commence-hacking)
  * [The Deployment](#the-deployment)
      * [Deploy with Heroku](#deploy-with-heroku)
        * [Deploy to the Test Instance](#deploy-to-the-test-instance)
        * [Deploy to the Production Instance](#deploy-to-the-production-instance)
          * [Mark the Current Version Released](#mark-the-current-version-released)
          * [Tag the Release](#tag-the-release)
          * [Push the Tagged Release to Heroku](#push-the-tagged-release-to-heroku)
  * [Consume the API](#consume-the-api)
    * [Using the CoreAPI Client Libraries](#using-the-coreapi-client-libraries)

# Getting Started

## Get a Local Copy

Firstly, [fork the repository] and [git clone] it:

[fork the repository]: https://help.github.com/articles/fork-a-repo://help.github.com/articles/fork-a-repo/
[git clone]: https://git-scm.com/book/en/Getting-Started-Git-Basics

``` bash
$ git clone git@github.com:<your-username>/carbondoomsday.git
```

## Configure the Environment

We use [django-configurations] to configure the application in the spirit of
the [The Twelve-Factor App].

You'll need to export a number of environment variables to configure the
application. Please see [a maintained list of variables].

You'll have to change the values slightly to suit your local setup. For
convenience, you can place all of these in a `.env` file in the project root
and use [autoenv] to automatically export all those values whenever you enter
the directory.

[django-configurations]: https://github.com/jazzband/django-configurations
[The Twelve-Factor App]: https://12factor.net/config
[autoenv]:https://github.com/kennethreitz/autoenv
[a maintained list of variables]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/blob/master/dockercompose/app/carbondoomsday.env

## Install Python Dependencies

We manage our Python dependencies with [Pipenv], [install it via Pipsi]:

[Pipenv]: http://pipenv.org/
[install it via Pipsi]: http://docs.pipenv.org/en/latest/advanced.html#fancy-installation-of-pipenv

``` bash
$ curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python3
$ pipsi install pipenv
```

Then run:

``` bash
$ pipenv install --dev
```

## Install JavaScript Dependencies

You need to have [node] and [npm] installed. Using [nvm], it's simple:

[node]: https://nodejs.org/
[npm]: https://www.npmjs.com/
[nvm]: https://github.com/creationix/nvm#installation

``` bash
$ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
$ nvm install lts/*
```

Then run:

``` bash
$ npm install
```

## Install System Dependencies

The application relies on [PostgreSQL] and [Redis].

Please refer to the relevant installation method for your operating system.

[PostgreSQL]: https://www.postgresql.org/
[Redis]: https://redis.io/

## Setup the Database

You'll need to initialize your PostgreSQL database:


``` bash
$ make dbmigrations
$ make dbmigrate
```

And get the latest data:

``` bash
$ make scrape_latest
$ make scrape_historic
```

# Commence Hacking

Once you've [got started], you can commence working on the application. We want
the development experience to be as smooth as possible, so we rely on a self-documenting
Makefile which lists all the available commands you might need to run.

To see them all, run:

[got started]: #getting-started

```
$ make help
```

Happy hacking!

# The Deployment

## Deploy with Heroku

We use [Heroku] to deploy the application. You'll need to [install the Heroku
tool belt].

Then, you can login with the command line client:

[Heroku]: https://devcenter.heroku.com/
[install the Heroku tool belt]: https://devcenter.heroku.com/articles/heroku-cli#download-and-install

``` bash
$ heroku login
```

Enter the credentials that you obtained from the other maintainers. Once you're
logged in, you have access to our Heroku setup via the command line. You'll need
to add the Heroku Git remotes that we use:

``` bash
$ git remote add heroku-test https://git.heroku.com/carbondoomsday-test.git
$ git remote add heroku-prod https://git.heroku.com/carbondoomsday.git
```

### Deploy to the Test Instance

Every time a pull request is merged into the master branch, the application
will be deployed to [a test instance]. So, you don't have to anything more than
get your pull request merged!

[a test instance]: https://carbondoomsday-test.herokuapp.com/

### Deploy to the Production Instance

We also have [a production instance]. You'll need to complete the following steps
to make a production release.

[a production instance]: https://carbondoomsday.herokuapp.com/

#### Mark the Current Version Released

Look in the [CHANGELOG.md] for the latest release version. It should be marked:

[CHANGELOG.md]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/blob/master/CHANGELOG.md

``` markdown
  <version> [UNRELEASED]
  ...
```

Replace `[UNRELEASED]` with the current date in the following format: `[YYYY-MM-DD]`.

#### Tag the Release

After you've marked the version released in the [CHANGELOG.md], tag the latest release with:

[CHANGELOG.md]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/blob/master/CHANGELOG.md

``` bash
$ git tag -a <version> <git hash>
```

Write your description of the tag and then push that tagged version to Github:

``` bash
$ git push upstream master --tags
```

#### Push the Tagged Release to Heroku

Then, simple push to the Heroku production remote with:

``` bash
$ git push heroku-prod master
```

That's it! :beers:

# Consume the API

## Using the CoreAPI Client Libraries

Since [Django REST Framework] supports [API clients], client creators
automatically have access to the existing wealth of clients that speak
[coreAPI's Document model]. As far as I know, there are three existing
clients:

[Django REST Framework]: http://www.django-rest-framework.org/
[API clients]: http://www.django-rest-framework.org/topics/api-clients/
[coreAPI's Document model]: http://www.coreapi.org/specification/document/

  * The [command line client]
  * The [JavaScript client]
  * The [Python client]

[command line client]: http://www.django-rest-framework.org/topics/api-clients/#command-line-client
[JavaScript client]: http://www.django-rest-framework.org/topics/api-clients/#javascript-client-library
[Python client]: http://www.django-rest-framework.org/topics/api-clients/#python-client-library

The command line is useful for prototyping interactions with the API. As an
example, here's how we consume a single CO2 measurement with [coreapi-cli]:

[coreapi-cli]: http://www.coreapi.org/tools-and-resources/command-line-client/

```bash
$ pip install coreapi-cli
$ coreapi get http://carbondoomsday.herokuapp.com/
$ coreapi action co2 read --param date=2017-01-01
```
