# Table of Contents
  * [Get a Local Copy](#get-a-local-copy)
  * [Configure the Environment](#configure-the-environment)
  * [Install Python Dependencies](#install-python-dependencies)
  * [Install System Dependencies](#install-system-dependencies)
  * [Populate Database](#populate-database)

# Get a Local Copy

Firstly, [fork the repository] and [git clone] it:

[fork the repository]: https://help.github.com/articles/fork-a-repo/
[git clone]: https://git-scm.com/book/en/Getting-Started-Git-Basics

``` bash
$ git clone git@github.com:<your-username>/carbondoomsday.git
```

# Install Python Dependencies

We manage our Python dependencies with [Pipenv], you can [install it via Pipsi]:


[Pipenv]: http://pipenv.org/
[install it via Pipsi]: https://pipenv.readthedocs.io/en/latest/install/#fancy-installation-of-pipenv

``` bash
$ curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python3
$ source ~/.bashrc  # OPTIONAL, depending on your operating system and configuration
$ pipsi install pew
$ pipsi install pipenv
```

> Pipsi is installed in a location that you may have to add to your $PATH environment variable. You'll have to add $HOME/.local/bin to your $PATH in order to get access to the `pipsi` executable

Then run:

``` bash
$ pipenv install --dev --three
```

# Configure the Environment

We use [django-configurations] to configure the application in the spirit of
the [The Twelve-Factor App]. You'll need to have a number of environment
variables to configure the application.

[django-configurations]: https://github.com/jazzband/django-configurations
[The Twelve-Factor App]: https://12factor.net/config

Luckily, [pipenv does this for us]. You just need to make a copy of the
existing [example.env], rename it as a `.env` file  and fill it with values
that are right for your environment.

[pipenv does this for us]: https://docs.pipenv.org/advanced/#automatic-loading-of-env
[the example configuration to get started]: https://github.com/giving-a-fuck-about-climate-change/carbondoomsday/blob/master/example.env

# Using Pipenv

There are many helpful commands contained in the Makefile. Each of them
make sure to run commands inside the pipenv environment. If you're not
using the targets, please remember to prefix your commands with:

```bash
$ pipenv run <command>
```

Or else, just drop into a configured environment with:

```bash
$ pipenv shell
```

# Install System Dependencies

The application relies on [PostgreSQL] and [Redis].

Please refer to the relevant installation method for your operating system.

[PostgreSQL]: https://www.postgresql.org/
[Redis]: https://redis.io/

# Populate Database

You can load the latest data into your PostgreSQL with:

``` bash
$ make dbmigrate
```

And get the latest data:

``` bash
$ make scrape_mlo_co2_since_2015
```

# Start Application

```bash
$ make server
```

# Run the Test Suite

```bash
$ make test
```

# Run the Linter, isort, Test Suite, and dbcheckmigrations

```bash
$ make proof
```
