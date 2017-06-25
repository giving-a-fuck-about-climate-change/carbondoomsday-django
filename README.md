[![Build Status](https://travis-ci.org/giving-a-fuck-about-climate-change/carbondoomsday.svg?branch=master)](https://travis-ci.org/giving-a-fuck-about-climate-change/carbondoomsday)
[![codecov](https://codecov.io/gh/giving-a-fuck-about-climate-change/carbondoomsday/branch/master/graph/badge.svg)](https://codecov.io/gh/giving-a-fuck-about-climate-change/carbondoomsday)
[![Heroku](https://img.shields.io/badge/Heroku-Deployed-brightgreen.svg)](http://carbondoomsday.herokuapp.com/)

[![GitHub issues](https://img.shields.io/github/issues/giving-a-fuck-about-climate-change/carbondoomsday.svg)](https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/issues)
[![GitHub forks](https://img.shields.io/github/forks/giving-a-fuck-about-climate-change/carbondoomsday.svg)](https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/network)
[![GitHub stars](https://img.shields.io/github/stars/giving-a-fuck-about-climate-change/carbondoomsday.svg)](https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/stargazers)

[![Gitter chat](https://badges.gitter.im/giving-a-fuck-about-climate-change/gitter.png)](https://gitter.im/giving-a-fuck-about-climate-change/Lobby)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/giving-a-fuck-about-climate-change/carbondoomsday.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

# carbondoomsday

A [Django] web API for climate change data inspired by [no one giving a fuck].

This is a community driven project which aims to bring all levels of
contributor to engage in providing a reliable, free (price and [freedom]) and
feature packed web API to allow front-end client creators consume climate
change related data in order to fuel a new wave of interesting and engaging
visualisations and interactive environments to help us all understand and more
importantly, to act on stopping the ongoing trend of [ecocide].

Join us, and give a fuck.

http://api.carbondoomsday.com

[Django]: https://www.djangoproject.com/
[no one giving a fuck]: http://titojankowski.com/no-one-gives-a-fck-about-climate-change/
[freedom]: https://fsfe.org/about/basics/freesoftware.en.html
[ecocide]: https://en.wikipedia.org/wiki/Ecocide

# Table of Contents

  * [Contribute to the API](#contribute-to-the-api)
    * [Get a Local Copy](#get-a-local-copy)
    * [Install Python Dependencies](#install-python-dependencies)
    * [Install Services](#install-services)
    * [Configure the Environment](#configure-the-environment)
    * [Run the Tests](#run-the-tests)
    * [Run the Development Server](#run-the-development-server)
    * [Run the Entire Application](#run-the-entire-application)
    * [Find Some Work](#find-some-work)
    * [Submitting Your Work](#submitting-your-work)
    * [Deploy with Heroku](#deploy-with-heroku)
  * [Consume the API](#consume-the-api)
    * [Using the CoreAPI Client Libraries](#using-the-coreapi-client-libraries)

# Contribute to the API

The following instructions are for setting up a local environment for
contributing to the development of this application.

We are using version 3 of the [Python programming language] and the [Django Web
framework].

[Python programming language]: https://www.python.org/
[Django Web framework]: https://www.djangoproject.com/

## Get a Local Copy

Firstly, [fork the repository] and [git clone] it:

[fork the repository]: https://help.github.com/articles/fork-a-repo://help.github.com/articles/fork-a-repo/
[git clone]: https://git-scm.com/book/en/Getting-Started-Git-Basics

``` bash
$ git clone git@github.com:<your-username>/carbondoomsday.git
```

If you are feeling particularly generous, star the repository so that any of
your followers might see it or ultimately that the repository will be marked as
trending and many others will see the project and hopefully join the effort.

## Install Python Dependencies

We manage our dependencies with [Pipenv], [install it via Pipsi]:

[Pipenv]: http://pipenv.org/
[Install it via Pipsi]: http://docs.pipenv.org/en/latest/advanced.html#fancy-installation-of-pipenv

``` bash
$ curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python3
$ pipsi install pipenv
```

Then inside the project root, run:

``` bash
$ pipenv install --dev
```

This will install application and development dependencies.

## Install Services

The application relies on [PostgreSQL] and [Redis]. Please refer to the
relevant installation method for your operating system.

[PostgreSQL]: https://www.postgresql.org/
[Redis]: https://redis.io/

## Configure the Environment

We use [django-configurations] to configure the application in the spirit of
the [The Twelve-Factor App]. You'll need to export a number of environment
variables to configure the application. Please see [a maintained list of
variables]. For convenience, you can place all of these in a `.env` file in the
project root and use [autoenv] to automatically export all those values
whenever you enter the directory.

[django-configurations]: https://github.com/jazzband/django-configurations
[The Twelve-Factor App]: https://12factor.net/config
[autoenv]:https://github.com/kennethreitz/autoenv
[a maintained list of variables]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/blob/master/dockercompose/app/carbondoomsday.env

## Run the Tests

We use [pytest] to write our tests. You can run the tests with:

``` bash
$ make test
```

[pytest]: https://docs.pytest.org/en/latest/

## Run the Static Analysis Tools

In order to foster a more helpful code review atmosphere, similar coding styles
and best practices in the code base, we automate code quality opinions with the
very useful static analysis tools [pylama] and [isort].

[pylama]: https://github.com/klen/pylama
[isort]: https://github.com/timothycrosley/isort

Quality check the code with:

``` bash
$ make lint
```

Check you've got your imports correct with:

``` bash
$ make isort
```

## Run the Development Server

Use the development server for convenience, whilst hacking with:

``` bash
$ make devserver
```

## Run the Entire Application

We support a local [docker-compose] powered deployment of the application. If you want to see
the entire application and all necessary services up and running, just run the following:

[docker-compose]: https://docs.docker.com/compose/

``` bash
$ make compose
```

You'll then start to receive a stream of logs and will find the application available on your [localhost].
This differs from the [development server] in that all the necessary services are provided in separate docker
containers and [nginx] serves the application. It is closer to the actual production deployment and changes that
affect the entire system can be locally tested.

[localhost]: http://localhost/
[development server]: #run-the-development-server
[nginx]: https://www.nginx.com/resources/wiki/

## Find Some Work

Please take a look at [the issues] or if you don't find something interesting
there, come asking questions [on Gitter]. There will be an ongoing effort to
make prospective work more discoverable for new contributors. Please help us
improve this.

[the issues]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/issues/
[on Gitter]: https://gitter.im/giving-a-fuck-about-climate-change/Lobby

## Submitting your Work

Thank you for taking time to contribute to this project. All contributors will
be given equal access to the project and will be unconditionally made members
of the organisation.

Just [submit a pull request] as you normally would. We use [Travis CI] for our
continuous integration, and each pull request submitted will undergo various
tests to help assert the correctness of it.

To be reasonably sure your change set will pass the CI, run:

``` bash
$ make proof
```

A maintainer will try to review your change set as soon as possible. Please
complain in [the lobby] if no one is responding.

[submit a pull request]: https://help.github.com/articles/creating-a-pull-request/
[Travis CI]: https://travis-ci.org/
[the lobby]: https://gitter.im/giving-a-fuck-about-climate-change/Lobby

## Deploy with Heroku

We use [Heroku] to deploy the application. Every time a pull request is merged into
the master branch, the application will be deployed to [a test instance]. We also have
[a production instance] which we tag and manually deploy releases.

[a test instance]: https://carbondoomsday-test.herokuapp.com/
[a production instance]: https://carbondoomsday.herokuapp.com/

If your changes might affect the Heroku deployment, you'll need to test this
locally. [Install the toolbelt] and run:

[Install the toolbelt]: https://devcenter.heroku.com/articles/heroku-cli#download-and-install

``` bash
$ heroku local web
```

If the servers comes up, you can be fairly confident that things will work.

[Heroku]: https://devcenter.heroku.com/

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

Please also check the [clientexamples] directory for an example of using the
Python library. If you are a JavaScript programmer, please consider
contributing an example of using the library as well if you start to use the
API. It would be much appreciated.

[clientexamples]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/tree/master/clientexamples

Happy Hacking!
