from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, index=True)
    name = Column(String, unique=True, index=True)
    type_one = Column(String, index=True)
    type_two = Column(String, index=True)
    total = Column(Integer, index=True)
    hp = Column(Integer, index=True)
    attack = Column(Integer, index=True)
    defense = Column(Integer, index=True)
    sp_atk = Column(Integer, index=True)
    sp_def = Column(Integer, index=True)
    speed = Column(Integer, index=True)
    generation = Column(Integer, index=True)
    legendary = Column(Boolean, index=True)

    def __repr__(self):
        return '''<Pokemon(id='{0}', number='{1}', name='{2}', type_one='{3}', type_two='{4}', total='{5}', hp='{6}',
            attack='{7}', defense='{8}', sp_atk='{9}', sp_def='{10}', speed='{11}', generation='{12}',
            legendary='{13}')>'''.format(self.id, self.number, self.name, self.type_one, self.type_two, self.total,
                                         self.hp, self.attack, self.defense, self.sp_atk, self.sp_def, self.speed,
                                         self.generation, self.legendary)
