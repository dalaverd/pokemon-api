from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


def get_pokemon(db: Session, pokemon_id: int):
    return db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()


def get_pokemon_by_name(db: Session, pokemon_name: str):
    return db.query(models.Pokemon).filter(func.lower(models.Pokemon.name) == func.lower(pokemon_name)).first()


def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pokemon).offset(skip).limit(limit).all()


def create_pokemon(db: Session, pokemon: schemas.PokemonCreate):
    db_pokemon = models.Pokemon(number=pokemon.number, name=pokemon.name, type_one=pokemon.type_one, type_two=pokemon.type_two,
                                total=pokemon.total, hp=pokemon.hp, attack=pokemon.attack, defense=pokemon.defense,
                                sp_atk=pokemon.sp_atk, sp_def=pokemon.sp_def, speed=pokemon.speed, generation=pokemon.generation,
                                legendary=pokemon.legendary)
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon


def delete_pokemon(db: Session, db_pokemon: schemas.Pokemon):
    db.delete(db_pokemon)
    db.commit()
    return {"ok": True}


def update_pokemon(db: Session, db_pokemon: schemas.Pokemon, pokemon: schemas.PokemonUpdate):
    pokemon_data = pokemon.dict(exclude_unset=True)

    for key, value in pokemon_data.items():
        setattr(db_pokemon, key, value)

    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon
