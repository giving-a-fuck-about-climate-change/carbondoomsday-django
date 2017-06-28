# Table of Contents
  * [Get a Local Copy](#get-a-local-copy)
  * [Configure the Environment](#configure-the-environment)
  * [Install Python Dependencies](#install-python-dependencies)
  * [Install System Dependencies](#install-system-dependencies)
  * [Setup the Database](#setup-the-database)

# Get a Local Copy

Firstly, [fork the repository] and [git clone] it:

[fork the repository]: https://help.github.com/articles/fork-a-repo://help.github.com/articles/fork-a-repo/
[git clone]: https://git-scm.com/book/en/Getting-Started-Git-Basics

``` bash
$ git clone git@github.com:<your-username>/carbondoomsday.git
```

# Configure the Environment

We use [django-configurations] to configure the application in the spirit of
the [The Twelve-Factor App].

You'll need to export a number of environment variables to configure the
application. You'll have to change the values slightly to suit your local setup.
Please see [the example configuration to get started].

You can export them into your environment with:

``` bash
$ set -a
$ source example.env
$ set +a
```

Or, for convenience, you can place all of these in a `.env` file in the project
root and use [autoenv] to automatically export all those values whenever you
enter the directory.

[django-configurations]: https://github.com/jazzband/django-configurations
[The Twelve-Factor App]: https://12factor.net/config
[autoenv]:https://github.com/kennethreitz/autoenv
[the example configuration to get started]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/blob/master/example.env

# Install Python Dependencies

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

# Install System Dependencies

The application relies on [PostgreSQL] and [Redis].

Please refer to the relevant installation method for your operating system.

[PostgreSQL]: https://www.postgresql.org/
[Redis]: https://redis.io/

# Setup the Database

You can load the latest data into your PostgreSQL with:

``` bash
$ make dbmigrate
```

And get the latest data:

``` bash
$ make scrapelatest
```
