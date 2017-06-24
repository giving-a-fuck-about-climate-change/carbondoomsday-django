"""An example of using the coreapi Python client library."""

import csv
from datetime import datetime as dt

import coreapi

client = coreapi.Client()


def retrieve_schema():
    """Retrieve the specified schema."""
    return client.get("https://carbondoomsday.herokuapp.com")


def build_date_params(num_years):
    """A comma separated string of dates in format YYYY-DD-MM."""
    year = dt.today().year
    last_N_years = range(year, year - num_years, -1)
    formatted = ["{}-01-01".format(year) for year in last_N_years]
    return ",".join(formatted)


def write_to_csv(response):
    """A paginated response converted and written to CSV."""
    with open("output.csv", "w") as output:
        writer = csv.DictWriter(output, fieldnames=["date", "ppm"])
        writer.writeheader()
        writer.writerows(response['results'])


if __name__ == "__main__":
    """The main function."""
    schema = retrieve_schema()
    actions = ["co2", "list"]
    params = {"date__in": build_date_params(50)}
    response = client.action(schema, actions, params=params)

    # Unfortunately, the client does not support CSV rendering
    # So, we must do this manually for now. Please see:
    # https://github.com/core-api/python-client/issues/140
    write_to_csv(response)

    print("Consumed and packed into ./output.csv")
