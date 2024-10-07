import base64
import os
import time
import uuid
import argparse
from flask import Flask, jsonify, request, Response
from faker import Faker
from datetime import datetime, timedelta
import random
from collections import OrderedDict
import json

__version__ = "0.10.03.1"

app = Flask(__name__)
fake = Faker()

items = []
MAX_RECORDS = 200  # Total Records that API will serve for each endpoint
DEFAULT_ORDER_BY = 'updatedAt'
DEFAULT_ORDER_TYPE = 'asc'
DEFAULT_PAGE_SIZE = 10

ROOT_LOCATION = ".ft_api_playground"
LAST_VERSION_CHECK_FILE = "_last_version_check"
ONE_DAY_IN_SEC = 24 * 60 * 60
VALID_COMMANDS = ["start"]
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_TIME_FORMAT_WITHOUT_Z = "%Y-%m-%dT%H:%M:%S"
APPLICATION_JSON = 'application/json'
INVALID_DATE_FORMAT_MESSAGE = "Invalid date format for 'updated_since'. Use 'YYYY-MM-DDTHH:MM:SSZ'"
INVALID_DATE_FORMAT_MISSING_Z_MESSAGE = "Invalid date format for 'updated_since'. Must end with 'Z' for UTC"

for index in range(MAX_RECORDS):
    record_creation_time = datetime.now() - timedelta(hours=MAX_RECORDS - index, minutes=random.randint(0, 59),
                                                      seconds=random.randint(0, 59))
    user = OrderedDict([
        ('id', str(uuid.uuid4())),
        ('name', fake.name()),
        ('email', fake.email()),
        ('address', fake.address()),
        ('company', fake.company()),
        ('job', fake.job()),
        ('createdAt', record_creation_time.strftime(
            DATE_TIME_FORMAT)),
        ('updatedAt',
         (record_creation_time + timedelta(minutes=random.randint(0, 59), seconds=random.randint(0, 59))).strftime(
             DATE_TIME_FORMAT))
    ])
    items.append(user)


# Custom JSON encoder to preserve order in API Response
class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, OrderedDict):
            return json.dumps(obj, indent=4, separators=(',', ': '))
        return super().encode(obj)


@app.route('/pagination/next_page_url', methods=['GET'])
def get_next_page_url_pagination():
    allowed_params = {'order_by', 'order_type', 'per_page', 'updated_since', 'page'}

    # Get filters from query parameters
    received_params = set(request.args.keys())

    # Throw an error if any unexpected parameters are passed
    unexpected_params = received_params - allowed_params
    if unexpected_params:
        return jsonify({'error': f'Unexpected query parameters: {", ".join(unexpected_params)}'}), 400

    # Get allowed filters from query parameters
    order_by_arg = request.args.get('order_by', type=str, default=DEFAULT_ORDER_BY)  # createdAt, updatedAt [Default
    # updatedAt]
    order_type_arg = request.args.get('order_type', type=str, default=DEFAULT_ORDER_TYPE)  # asc, desc [Default asc]
    per_page_arg = request.args.get('per_page', type=int, default=DEFAULT_PAGE_SIZE)  # [1-50] Default 10
    updated_since_arg = request.args.get('updated_since', type=str)

    # Validate order_by value
    if order_by_arg not in ['createdAt', 'updatedAt']:
        return jsonify({"error": "Invalid value for 'order_by'. Use 'createdAt' or 'updatedAt'"}), 400

    # Validate order_type value
    if order_type_arg not in ['asc', 'desc']:
        return jsonify({"error": "Invalid value for 'order_type'. Use 'asc' or 'desc'"}), 400

    # Validate per_page value
    if not (1 <= per_page_arg <= 50):
        return jsonify({"error": "Invalid value for 'per_page'. It should be between 1 and 50."}), 400

    # Filter items based on the updated_since parameter
    filtered_items = items
    if updated_since_arg:
        try:
            # Ensure the format ends with 'Z' indicating UTC
            if updated_since_arg.endswith('Z'):
                updated_since_arg = updated_since_arg[:-1]  # Strip the 'Z' before parsing
                updated_since_date = datetime.strptime(updated_since_arg, DATE_TIME_FORMAT_WITHOUT_Z)
                updated_since_date = updated_since_date.replace(tzinfo=None)  # Set the timezone to UTC
            else:
                return jsonify({"error": INVALID_DATE_FORMAT_MISSING_Z_MESSAGE}), 400

            # Convert 'updatedAt' to datetime for comparison
            filtered_items = [item for item in items if
                              datetime.strptime(item['updatedAt'][:-1], DATE_TIME_FORMAT_WITHOUT_Z)
                              >= updated_since_date]
        except ValueError:
            return jsonify({"error": INVALID_DATE_FORMAT_MESSAGE}), 400

    # Sort the filtered items
    reverse_order = (order_type_arg == 'desc')
    filtered_items.sort(key=lambda x: x[order_by_arg], reverse=reverse_order)

    # Pagination logic
    page = request.args.get('page', default=1, type=int)
    start_index = (page - 1) * per_page_arg
    end_index = start_index + per_page_arg
    paginated_items = filtered_items[start_index:end_index]

    # Next page logic
    next_page_url = None
    if end_index < len(filtered_items):
        next_page_url = f"{request.base_url}?page={page + 1}&per_page={per_page_arg}&order_by={order_by_arg}&order_type={order_type_arg}"
        if updated_since_arg:
            next_page_url += f"&updated_since={updated_since_arg}Z"  # Add 'Z' back for the next page

    response = {
        'data': paginated_items,
        'total_items': len(filtered_items),
        'page': page,
        'per_page': per_page_arg,
        'next_page_url': next_page_url
    }

    return Response(json.dumps(response, cls=CustomJSONEncoder), mimetype=APPLICATION_JSON)


@app.route('/pagination/page_number', methods=['GET'])
def get_page_number_pagination():
    allowed_params = {'order_by', 'order_type', 'per_page', 'page', 'updated_since'}

    # Get filters from query parameters
    received_params = set(request.args.keys())

    # Throw an error if any unexpected parameters are passed
    unexpected_params = received_params - allowed_params
    if unexpected_params:
        return jsonify({'error': f'Unexpected query parameters: {", ".join(unexpected_params)}'}), 400

    # Get allowed filters from query parameters
    order_by_arg = request.args.get('order_by', type=str, default=DEFAULT_ORDER_BY)  # Default to updatedAt
    order_type_arg = request.args.get('order_type', type=str, default=DEFAULT_ORDER_TYPE)  # Default to asc
    per_page_arg = request.args.get('per_page', type=int, default=DEFAULT_PAGE_SIZE)  # Default to 10
    page_arg = request.args.get('page', default=1, type=int)  # Default to page 1
    updated_since_arg = request.args.get('updated_since', type=str)

    # Validate `order_by` value
    if order_by_arg not in ['createdAt', 'updatedAt']:
        return jsonify({"error": "Invalid value for 'order_by'. Use 'createdAt' or 'updatedAt'."}), 400

    # Validate `order_type` value
    if order_type_arg not in ['asc', 'desc']:
        return jsonify({"error": "Invalid value for 'order_type'. Use 'asc' or 'desc'."}), 400

    # Validate `per_page` value
    if not (1 <= per_page_arg <= 50):
        return jsonify({"error": "Invalid value for 'per_page'. It should be between 1 and 50."}), 400

    # Validate `page` value
    if page_arg < 1:
        return jsonify({"error": "Invalid value for 'page'. It must be greater than or equal to 1."}), 400

    # Filter items based on the updated_since parameter
    filtered_items = items
    if updated_since_arg:
        try:
            if updated_since_arg.endswith('Z'):
                updated_since_arg = updated_since_arg[:-1]  # Strip the 'Z' before parsing
                updated_since_date = datetime.strptime(updated_since_arg, DATE_TIME_FORMAT_WITHOUT_Z)
                updated_since_date = updated_since_date.replace(tzinfo=None)  # Set the timezone to UTC
            else:
                return jsonify({"error": INVALID_DATE_FORMAT_MISSING_Z_MESSAGE}), 400

            # Filter items
            filtered_items = [item for item in items if
                              datetime.strptime(item['updatedAt'][:-1],
                                                DATE_TIME_FORMAT_WITHOUT_Z) >= updated_since_date]
        except ValueError:
            return jsonify({"error": INVALID_DATE_FORMAT_MESSAGE}), 400

    # Sort the filtered items
    reverse_order = (order_type_arg == 'desc')
    filtered_items.sort(key=lambda x: x[order_by_arg], reverse=reverse_order)

    # Pagination logic
    start_index = (page_arg - 1) * per_page_arg
    end_index = start_index + per_page_arg
    paginated_items = filtered_items[start_index:end_index]

    # Total pages calculation
    total_items = len(filtered_items)
    total_pages = (total_items + per_page_arg - 1) // per_page_arg  # Calculate total pages

    # Prepare the response
    response = {
        'data': paginated_items,
        'page': page_arg,
        'page_size': per_page_arg,
        'total_pages': total_pages,
        'total_items': total_items  # Optional total items count
    }

    return Response(json.dumps(response, cls=CustomJSONEncoder), mimetype=APPLICATION_JSON)


@app.route('/pagination/offset', methods=['GET'])
def get_offset_pagination():
    allowed_params = {'order_by', 'order_type', 'limit', 'offset', 'updated_since'}

    # Get filters from query parameters
    received_params = set(request.args.keys())

    # Throw an error if any unexpected parameters are passed
    unexpected_params = received_params - allowed_params
    if unexpected_params:
        return jsonify({'error': f'Unexpected query parameters: {", ".join(unexpected_params)}'}), 400

    # Get allowed filters from query parameters
    order_by_arg = request.args.get('order_by', type=str, default=DEFAULT_ORDER_BY)  # Default to updatedAt
    order_type_arg = request.args.get('order_type', type=str, default=DEFAULT_ORDER_TYPE)  # Default to asc
    limit_arg = request.args.get('limit', type=int, default=DEFAULT_PAGE_SIZE)  # Default to 10
    offset_arg = request.args.get('offset', type=int, default=0)  # Default to 0
    updated_since_arg = request.args.get('updated_since', type=str)

    # Validate `limit` value
    if not (1 <= limit_arg <= 50):
        return jsonify({"error": "Invalid value for 'limit'. It should be between 1 and 50."}), 400

    # Validate `offset` value
    if offset_arg < 0:
        return jsonify({"error": "Invalid value for 'offset'. It must be greater than or equal to 0."}), 400

    # Validate `order_by` value
    if order_by_arg not in ['createdAt', 'updatedAt']:
        return jsonify({"error": "Invalid value for 'order_by'. Use 'createdAt' or 'updatedAt'."}), 400

    # Validate `order_type` value
    if order_type_arg not in ['asc', 'desc']:
        return jsonify({"error": "Invalid value for 'order_type'. Use 'asc' or 'desc'."}), 400

    # Filter items based on the updated_since parameter
    filtered_items = items
    if updated_since_arg:
        try:
            if updated_since_arg.endswith('Z'):
                updated_since_arg = updated_since_arg[:-1]  # Strip the 'Z' before parsing
                updated_since_date = datetime.strptime(updated_since_arg, DATE_TIME_FORMAT_WITHOUT_Z)
                updated_since_date = updated_since_date.replace(tzinfo=None)  # Set the timezone to UTC
            else:
                return jsonify({"error": INVALID_DATE_FORMAT_MISSING_Z_MESSAGE}), 400

            # Filter items
            filtered_items = [item for item in items if
                              datetime.strptime(item['updatedAt'][:-1],
                                                DATE_TIME_FORMAT_WITHOUT_Z) >= updated_since_date]
        except ValueError:
            return jsonify({"error": INVALID_DATE_FORMAT_MESSAGE}), 400

    # Sort the filtered items
    reverse_order = (order_type_arg == 'desc')
    filtered_items.sort(key=lambda x: x[order_by_arg], reverse=reverse_order)

    # Calculate total items after filtering
    total_items = len(filtered_items)

    # Calculate the data slice based on offset and limit
    paginated_items = filtered_items[offset_arg:offset_arg + limit_arg]

    # Prepare the response
    response = {
        'data': paginated_items,
        'offset': offset_arg,
        'limit': limit_arg,
        'total': total_items  # Total number of items
    }

    return Response(json.dumps(response, cls=CustomJSONEncoder), mimetype=APPLICATION_JSON)


@app.route('/pagination/keyset', methods=['GET'])
def get_keyset_pagination():
    page_size = 5 * DEFAULT_PAGE_SIZE

    allowed_params = {'scroll_param', 'updated_since'}

    # Get filters from query parameters
    received_params = set(request.args.keys())

    # Throw an error if any unexpected parameters are passed
    unexpected_params = received_params - allowed_params
    if unexpected_params:
        return jsonify({'error': f'Unexpected query parameters: {", ".join(unexpected_params)}'}), 400

    # Get allowed request parameters
    scroll_param = request.args.get('scroll_param', type=str)
    updated_since_arg = request.args.get('updated_since', type=str)

    # Ensure that both `scroll_param` and `updated_since` are not used together
    if scroll_param and updated_since_arg:
        return jsonify({"error": "You can only use 'updated_since' in first request, subsequent requests should use "
                                 "only 'scroll_param'"}), 400

    # Filter items
    filtered_items = items

    # Handle the first request with `updated_since`
    if updated_since_arg:
        try:
            if updated_since_arg.endswith('Z'):
                updated_since_arg = updated_since_arg[:-1]  # Strip the 'Z'
                updated_since_date = datetime.strptime(updated_since_arg, DATE_TIME_FORMAT_WITHOUT_Z)
            else:
                return jsonify({"error": INVALID_DATE_FORMAT_MISSING_Z_MESSAGE}), 400

            # Filter based on `updatedAt`
            filtered_items = [item for item in items if
                              datetime.strptime(item['updatedAt'][:-1],
                                                DATE_TIME_FORMAT_WITHOUT_Z) >= updated_since_date]
        except ValueError:
            return jsonify({"error": ("%s" % INVALID_DATE_FORMAT_MESSAGE)}), 400

    # Handle subsequent requests with `scroll_param`
    elif scroll_param:
        try:
            # Decode the base64 encoded `scroll_param`
            decoded_param = base64.b64decode(scroll_param).decode('utf-8')
            scroll_date = datetime.strptime(decoded_param, (DATE_TIME_FORMAT))

            # Filter items based on `updatedAt` for keyset pagination
            filtered_items = [item for item in items if
                              datetime.strptime(item['updatedAt'][:-1], DATE_TIME_FORMAT_WITHOUT_Z) > scroll_date]
        except ValueError:
            return jsonify({"error": "Invalid scroll_param value"}), 400

    # Sort the filtered items by `updatedAt` in ascending order
    filtered_items.sort(key=lambda x: x['updatedAt'])

    # Limit the number of items returned (for example, 10 items per page)
    per_page_arg = request.args.get('per_page', type=int, default=page_size)
    paginated_items = filtered_items[:per_page_arg]

    # Generate the next `scroll_param` if there are more items
    next_scroll_param = None
    if len(filtered_items) > per_page_arg:
        last_item_updated_at = paginated_items[-1]['updatedAt']
        next_scroll_param = base64.b64encode(last_item_updated_at.encode('utf-8')).decode('utf-8')

    # Prepare the response
    response = {
        'data': paginated_items,
        'scroll_param': next_scroll_param
    }

    return Response(json.dumps(response, cls=CustomJSONEncoder), mimetype=APPLICATION_JSON)


def check_newer_version():
    root_dir = os.path.join(os.path.expanduser("~"), ROOT_LOCATION)
    last_check_file_path = os.path.join(root_dir, LAST_VERSION_CHECK_FILE)
    if not os.path.isdir(root_dir):
        os.makedirs(root_dir, exist_ok=True)

    if os.path.isfile(last_check_file_path):
        # Is it time to check again?
        with open(last_check_file_path, 'r') as f_in:
            timestamp = int(f_in.read())
            if (int(time.time()) - timestamp) < ONE_DAY_IN_SEC:
                return

    # check version and save current time
    from get_pypi_latest_version import GetPyPiLatestVersion
    obtainer = GetPyPiLatestVersion()
    latest_version = obtainer('fivetran_api_playground')
    if __version__ < latest_version:
        print("[notice] A new release of 'fivetran-api-playground' is available: {}".format(latest_version))
        print("[notice] To update, run: pip install --upgrade fivetran-api-playground")

    with open(last_check_file_path, 'w') as f_out:
        f_out.write(f"{int(time.time())}")


def main():
    """The main entry point for the script.
    Parses command line arguments and passes them to connector object methods
    """

    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("command", help="|".join(VALID_COMMANDS))
    parser.add_argument("--port", type=int, default=None, help="Provide the port on which you want to run the API on "
                                                               "localhost")
    args = parser.parse_args()
    port = args.port if args.port else 5001

    if args.command.lower() == "start":
        check_newer_version()
        print("Starting Local API on port " + str(port) + " ...\n")
        pagination_types = [
            "Next Page URL Pagination",
            "Page Number Pagination",
            "Offset Pagination",
            "Keyset Pagination"
        ]

        endpoints = [
            f"GET http://127.0.0.1:{port}/pagination/next_page_url",
            f"GET http://127.0.0.1:{port}/pagination/page_number",
            f"GET http://127.0.0.1:{port}/pagination/offset",
            f"GET http://127.0.0.1:{port}/pagination/keyset"
        ]

        # Print header
        print("-" * 85)
        print(f"{'Pagination Type':<30} | {'Endpoint':<50}")
        print("-" * 85)

        # Print each pagination type and its corresponding endpoint
        for pagination_type, endpoint in zip(pagination_types, endpoints):
            print(f"{pagination_type:<30} | {endpoint:<50}")
        print("-" * 85)
        print("You can read about the API documentation for each endpoint on: \n"
              "https://pypi.org/project/fivetran-api-playground/")
        print("-" * 85)
        print("For your observability the API requests will be logged here!")
        print("Keep this process up and running until you finish trying out the API.\n")
        app.run(debug=True, port=port)

    else:
        raise NotImplementedError(f"Invalid command: {args.command}, see `api_playground --help`")


if __name__ == "__main__":
    main()
