from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_pokemon():
    response = client.get("/pokemons/1")
    assert response.status_code == 200
    assert response.json() == {
        "number": 1,
        "name": "Bulbasaur",
        "type_one": "Grass",
        "type_two": "Poison",
        "total": 318,
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "sp_atk": 65,
        "sp_def": 65,
        "speed": 45,
        "generation": 1,
        "legendary": False,
        "id": 1
    }


def test_read_inexistent_pokemon():
    response = client.get("/pokemons/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon not found"}


def test_read_pokemon_by_name():
    response = client.get("/pokemons/name/pikachu")
    assert response.status_code == 200
    assert response.json() == {
        "number": 25,
        "name": "Pikachu",
        "type_one": "Electric",
        "type_two": None,
        "total": 320,
        "hp": 35,
        "attack": 55,
        "defense": 40,
        "sp_atk": 50,
        "sp_def": 50,
        "speed": 90,
        "generation": 1,
        "legendary": False,
        "id": 31
    }


def test_read_inexistent_pokemon_by_name():
    response = client.get("/pokemons/name/missingno")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon not found"}


def test_read_pokemons():
    response = client.get("/pokemons", params={"skip": 0, "limit": 3})
    assert response.status_code == 200
    assert response.json() == [
        {"number": 1, "name": "Bulbasaur", "type_one": "Grass", "type_two": "Poison", "total": 318, "hp": 45,
         "attack": 49, "defense": 49, "sp_atk": 65, "sp_def": 65, "speed": 45, "generation": 1, "legendary": False,
         "id": 1},
        {"number": 2, "name": "Ivysaur", "type_one": "Grass", "type_two": "Poison", "total": 405, "hp": 60,
         "attack": 62, "defense": 63, "sp_atk": 80, "sp_def": 80, "speed": 60, "generation": 1,
         "legendary": False, "id": 2},
        {"number": 3, "name": "Venusaur", "type_one": "Grass", "type_two": "Poison", "total": 525, "hp": 80,
         "attack": 82, "defense": 83, "sp_atk": 100, "sp_def": 100, "speed": 80, "generation": 1, "legendary": False,
         "id": 3}]


def test_create_pokemon():
    response = client.post(
        "/pokemons/",
        json={
            "number": 850,
            "name": "Arctibax",
            "type_one": "Water",
            "total": 340,
            "hp": 45,
            "attack": 55,
            "defense": 45,
            "sp_atk": 45,
            "sp_def": 45,
            "speed": 95,
            "generation": 7,
            "legendary": False
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    response_json.pop("id")
    assert response_json == {
        "number": 850,
        "name": "Arctibax",
        "type_one": "Water",
        'type_two': None,
        "total": 340,
        "hp": 45,
        "attack": 55,
        "defense": 45,
        "sp_atk": 45,
        "sp_def": 45,
        "speed": 95,
        "generation": 7,
        "legendary": False
    }


def test_create_already_existent_pokemon():
    response = client.post(
        "/pokemons/",
        json={
            "number": 1,
            "name": "Bulbasaur",
            "type_one": "Grass",
            "type_two": "Poison",
            "total": 318,
            "hp": 45,
            "attack": 49,
            "defense": 49,
            "sp_atk": 65,
            "sp_def": 65,
            "speed": 45,
            "generation": 1,
            "legendary": False,
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Pokemon already registered"}


def test_delete_pokemon():
    response = client.delete("/pokemons/1")
    assert response.status_code == 200

    response = client.get("/pokemons/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon not found"}


def test_delete_inexistent_pokemon():
    response = client.delete("/pokemons/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon not found"}


def test_update_pokemon():
    response = client.patch(
        "/pokemons/31",
        json={
            "type_two": "Fairy",
            "total": 350,
            "sp_atk": 60,
            "legendary": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "number": 25,
        "name": "Pikachu",
        "type_one": "Electric",
        "type_two": "Fairy",
        "total": 350,
        "hp": 35,
        "attack": 55,
        "defense": 40,
        "sp_atk": 60,
        "sp_def": 50,
        "speed": 90,
        "generation": 1,
        "legendary": True,
        "id": 31
    }


def test_update_inexistent_pokemon():
    response = client.patch(
        "/pokemons/999",
        json={
            "type_two": "Fairy",
            "total": 350,
            "sp_atk": 60,
            "legendary": True,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon not found"}
