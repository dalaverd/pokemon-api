import logging
import pandas

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker

from db import crud, models, schemas
from db.database import SessionLocal, engine
from db.models import Pokemon

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)

file_name = "pokemon.csv"
df = pandas.read_csv(file_name)

df.to_sql(con=engine, name=Pokemon.__tablename__, if_exists="append", index=False)

session = sessionmaker()
session.configure(bind=engine)
s = session()

count_pokemon = s.query(Pokemon).count()
logger.info("Number of pokemons in database : %s", count_pokemon)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/pokemons/", response_model=schemas.Pokemon)
def create_pokemon(pokemon: schemas.PokemonCreate, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon_by_name(db, pokemon_name=pokemon.name)
    if db_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon already registered")
    return crud.create_pokemon(db=db, pokemon=pokemon)


@app.get("/pokemons/", response_model=list[schemas.Pokemon])
def read_pokemons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pokemons = crud.get_pokemons(db, skip=skip, limit=limit)
    return pokemons


@app.get("/pokemons/{pokemon_id}", response_model=schemas.Pokemon)
def read_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon(db, pokemon_id=pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return db_pokemon


@app.get("/pokemons/name/{pokemon_name}", response_model=schemas.Pokemon)
def read_pokemon_by_name(pokemon_name: str, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon_by_name(db, pokemon_name=pokemon_name)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return db_pokemon


@app.delete("/pokemons/{pokemon_id}")
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon(db, pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return crud.delete_pokemon(db, db_pokemon=db_pokemon)


@app.patch("/pokemons/{pokemon_id}", response_model=schemas.Pokemon)
def update_pokemon(pokemon_id: int, pokemon: schemas.PokemonUpdate, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon(db, pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return crud.update_pokemon(db, db_pokemon=db_pokemon, pokemon=pokemon)
