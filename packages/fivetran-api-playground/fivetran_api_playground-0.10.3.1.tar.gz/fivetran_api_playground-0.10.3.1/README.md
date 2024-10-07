# Fivetran API Playground
The Fivetran API Playground enables you to explore various sample API endpoints on your local machine, helping you better understand the complexities of real-world APIs. It serves as a hands-on learning tool for building connectors, allowing you to write custom Python code within [Fivetran's](https://www.fivetran.com/) secure cloud environment. For more information, see our [Connector SDK documentation](https://fivetran.com/docs/connectors/connector-sdk).

## **Install**

    pip install fivetran-api-playground

## **Requirements**
- Python ≥3.9 and ≤3.11
- Operating System:
    - Windows 10 or later
    - MacOS 13 (Ventura) or later

## Usage
To start the API, run the following command:

```bash
playground start  # starts the server on 5001 port by default

playground start --port 
# starts the server on the specified port
```

You will see a message like:
```
Starting Local API on port 5001 ...
-------------------------------------------------------------------------------------
Pagination Type                | Endpoint                                          
-------------------------------------------------------------------------------------
Next Page URL Pagination       | GET http://127.0.0.1:5001/pagination/next_page_url
Page Number Pagination         | GET http://127.0.0.1:5001/pagination/page_number  
Offset Pagination              | GET http://127.0.0.1:5001/pagination/offset       
Keyset Pagination              | GET http://127.0.0.1:5001/pagination/keyset       
-------------------------------------------------------------------------------------
You can read about the API documentation for each endpoint on: 
https://pypi.org/project/fivetran-api-playground/
-------------------------------------------------------------------------------------
For your observability the API requests will be logged here!
Keep this process up and running until you finish trying out the API.

Press CTRL+C to quit
```

## API Endpoints
There are four types of pagination available, allowing you to fetch up to 200 dynamically-generated records with dummy data each time the server is run locally using the `playground start` command.

### 1. Next Page URL Pagination
- **Endpoint:** `/pagination/next_page_url`
- **Method:** `GET`
- **Query Parameters:**
  | Parameter      | Type     | Required | Description                                             |
  |----------------|----------|----------|---------------------------------------------------------|
  | `order_by`     | string   | No       | Parameter to order by. Allowed values: `createdAt`, `updatedAt`. Default: `updatedAt`. |
  | `order_type`   | string   | No       | Sorting order. Allowed values: `asc`, `desc`. Default: `asc`. |
  | `per_page`     | integer  | No       | Number of items per page (1-50). Default: `10`.       |
  | `updated_since`| string   | No       | Return items updated since this timestamp. Format: `YYYY-MM-DDTHH:MM:SSZ`. |
- **Response:**
  - `data`: Array of items for the current page.
  - `total_items`: Total number of items after filtering.
  - `page`: Current page number.
  - `per_page`: Number of items per page.
  - `next_page_url`: URL for the next page, if available.
- **Sample Request:**
    ```
    curl -X GET http://127.0.0.1:5001/pagination/next_page_url
    ```
- **Sample Response:**
    ```
    {
      "data": [
        {
          "id": "1989d8f6-57a5-41bf-b21b-4d6de6db6de6",
          "name": "XYZ",
          "email": "xyz@example.net",
          "address": "Some Random Address, AS 18073",
          "company": "Nguyen, Nash and King",
          "job": "Licensed conveyancer",
          "createdAt": "2024-09-22T12:15:33Z",
          "updatedAt": "2024-09-22T12:15:50Z"
        },
        ...
      ],
      "total_items": 200,
      "page": 1,
      "per_page": 10,
      "next_page_url": "http://127.0.0.1:5001/pagination/next_page_url?page=2&per_page=10&order_by=updatedAt&order_type=asc"
    }
    ```

### 2. PAGE Number Pagination
- **Endpoint:** `/pagination/page_number`
- **Method:** `GET`
- **Query Parameters:**
  | Parameter      | Type     | Required | Description                                             |
  |----------------|----------|----------|---------------------------------------------------------|
  | `order_by`     | string   | No       | Parameter to order by. Allowed values: `createdAt`, `updatedAt`. Default: `updatedAt`. |
  | `order_type`   | string   | No       | Sorting order. Allowed values: `asc`, `desc`. Default: `asc`. |
  | `per_page`     | integer  | No       | Number of items per page (1-50). Default: `10`.       |
  | `page`         | integer  | No       | Page number to retrieve (1 or higher). Default: `1`.   |
  | `updated_since`| string   | No       | Return items updated since this timestamp. Format: `YYYY-MM-DDTHH:MM:SSZ`. |
- **Response:**
  - `data`: Array of items for the current page.
  - `page`: Current page number.
  - `page_size`: Number of items per page.
  - `total_pages`: Total number of pages.
  - `total_items`: Total number of items.
- **Sample Request:**
    ```
    curl -X GET http://127.0.0.1:5001/pagination/page_number
    ```
- **Sample Response:**
    ```
    {
      "data": [
        {
          "id": "1989d8f6-57a5-41bf-b21b-4d6de6db6de6",
          "name": "XYZ",
          "email": "xyz@example.net",
          "address": "Some Random Address, AS 18073",
          "company": "Nguyen, Nash and King",
          "job": "Licensed conveyancer",
          "createdAt": "2024-09-22T12:15:33Z",
          "updatedAt": "2024-09-22T12:15:50Z"
        },
        ...
      ],
      "page": 1,
      "page_size": 10,
      "total_pages": 20,
      "total_items": 200
    }
    ```

### 3. Offset Pagination
- **Endpoint:** `/pagination/offset`
- **Method:** `GET`
- **Query Parameters:**
  | Parameter      | Type     | Required | Description                                             |
  |----------------|----------|----------|---------------------------------------------------------|
  | `order_by`     | string   | No       | Parameter to order by. Allowed values: `createdAt`, `updatedAt`. Default: `updatedAt`. |
  | `order_type`   | string   | No       | Sorting order. Allowed values: `asc`, `desc`. Default: `asc`. |
  | `limit`        | integer  | No       | Number of items to return (1-50). Default: `10`.      |
  | `offset`       | integer  | No       | Number of items to skip before starting to collect the result set. Default: `0`. |
  | `updated_since`| string   | No       | Return items updated since this timestamp. Format: `YYYY-MM-DDTHH:MM:SSZ`. |
- **Response:**
  - `data`: Array of items retrieved based on limit and offset.
  - `offset`: The offset used in the request.
  - `limit`: The limit used in the request.
  - `total`: Total number of items after filtering.
- **Sample Request:**
    ```
    curl -X GET http://127.0.0.1:5001/pagination/offset
    ```
- **Sample Response:**
    ```
    {
      "data": [
        {
          "id": "1989d8f6-57a5-41bf-b21b-4d6de6db6de6",
          "name": "XYZ",
          "email": "xyz@example.net",
          "address": "Some Random Address, AS 18073",
          "company": "Nguyen, Nash and King",
          "job": "Licensed conveyancer",
          "createdAt": "2024-09-22T12:15:33Z",
          "updatedAt": "2024-09-22T12:15:50Z"
        },
        ...
      ],
      "offset": 0,
      "limit": 10,
      "total": 200
    }
    ```

### 4. Keyset Pagination
- **Endpoint:** `/pagination/keyset`
- **Method:** `GET`
- **Query Parameters:**
  | Parameter      | Type     | Required | Description                                             |
  |----------------|----------|----------|---------------------------------------------------------|
  | `scroll_param` | string   | No       | Base64 encoded timestamp to fetch items after this timestamp. |
  | `updated_since`| string   | No       | Return items updated since this timestamp. Format: `YYYY-MM-DDTHH:MM:SSZ`. |
- **Response:**
  - `data`: Array of items retrieved based on keyset pagination.
  - `total_count`: Total number of items after filtering.
  - `scroll_param`: Base64 encoded parameter for the next page, if available.
- **Sample Request:**
    ```
    curl -X GET http://127.0.0.1:5001/pagination/keyset
    ```
- **Sample Response:**
    ```
    {
      "data": [
        {
          "id": "1989d8f6-57a5-41bf-b21b-4d6de6db6de6",
          "name": "XYZ",
          "email": "xyz@example.net",
          "address": "Some Random Address, AS 18073",
          "company": "Nguyen, Nash and King",
          "job": "Licensed conveyancer",
          "createdAt": "2024-09-22T12:15:33Z",
          "updatedAt": "2024-09-22T12:15:50Z"
        },
        ...
      ],
      "scroll_param": "MjAyNC0wOS0yNFQxNDozMTozN1o="
    }
    ```


## Error Responses
- **400 Bad Request:** Returned for validation errors or unexpected query parameters.
  - **Example:** `{"error": "Invalid value for 'order_by'. Use 'createdAt' or 'updatedAt'."}`


## **Maintenance**
This package is actively maintained by Fivetran Developers. Please reach out to our [Support team](https://support.fivetran.com/hc/en-us) for any inquiries.