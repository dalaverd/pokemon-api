# REST API pokemon application

This is an API for Pokemon.

## Run the app

    uvicorn main:app --reload  

## Interactive API docs

    http://localhost:8000/docs

## Run tests

    pytest tests/

# REST API

The REST API to the pokemon-api app is described below.

### Get list of Pokemons

`GET /pokemons/`

### Create a new Pokemon

`POST /pokemons/`

### Get a Pokemon by id

`GET /pokemon/:id`

### Delete a Pokemon

`DELETE /pokemons/:id`

### Update a Pokemon

`PATCH /pokemons/:id`

### Get a Pokemon by Name

`GET /pokemons/name/:name`
