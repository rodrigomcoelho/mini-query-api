# Mini Query API

Mini Query API is a lightweight and efficient tool designed to automate the process of gathering data from Google Cloud BigQuery and making it accessible via a RESTful API. This application supports D-1 data and provides flexible entity management through its API, allowing users to convert any query or table into a registered entity.

## Features

- **Data Collection**: Seamlessly gathers data from Google Cloud BigQuery, focusing on D-1 data.
- **RESTful API**: Access and manage your data entities through a simple and robust API.
- **Entity Registration**: Register new entities based on any query or table from BigQuery.
- **Entity Management**: Retrieve entity definitions, count the number of registered entities, search records with pagination (100 rows per page), and fetch specific records.

## Architecture Overview

![image info](./assets/architecture.svg)

## Getting Started

### Prerequisites

- Google Cloud Project with BigQuery enabled.
- Basic knowledge of RESTful APIs.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your-repo-name
    ```
3. Install the necessary dependencies:
    ```bash
    poetry install
    ```
4. Set up environment variables for Google Cloud credentials and API configurations.

### Usage

#### Registering a New Entity

To register a new entity, send a `POST` request to the `/entities` endpoint with the query or table information. The API will handle the rest, transforming the input into a registered entity.

#### Retrieving Entity Definitions

To get the definition of a registered entity, use the `/entities/{entity_id}` endpoint.

#### Listing Registered Entities

You can list all registered entities using the `/entities` endpoint. Pagination is supported, with a default of 100 rows per page. Use `page` parameter to retrieve data from next page.

#### Fetching Records

To fetch specific records from an entity, use the `/entities/{entity_id}/records` endpoint. You can also fetch all records with pagination.

#### Fetch One Specific Record By Key

To fetch specific records from an entity, use the `/entities/{entity_id}/records/key:value` endpoint. The `key` references the field set as the index when the entity was created and the `value` is the actual content to be fetched.

### API Endpoints

- `POST /entities`: Register a new entity.
- `GET /entities`: List all registered entities.
- `GET /entities/{entity_id}/definition`: Get the definition of a specific entity.
- `GET /entities/{entity_id}/records`: Retrieve records from a specific entity.
- `GET /entities/{entity_id}/records/{record_id}`: Fetch a specific record by its ID.
- `PUT /entities/{entity_id}`: Update an existing entity.

### Examples

#### Registering a New Entity
```bash
curl -X POST https://your-api-url/entities -H "Content-Type: application/json" -d '{
  "entityName": "example_entity",
  "query": "SELECT id, description FROM `your-project.your-dataset.your-table`",
  "indexField": "id"
}'
