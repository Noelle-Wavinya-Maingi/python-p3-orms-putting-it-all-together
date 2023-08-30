import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
             CREATE TABLE IF NOT EXISTS dogs (
             id INTEGER PRIMARY KEY,
             name TEXT,
             breed TEXT
             )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)  

    def save(self):
            sql = """
                  INSERT INTO dogs(name, breed)
                  VALUES(?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
         new_dog = cls(name, breed)
         new_dog.save()
         return new_dog
    
    @classmethod
    def new_from_db(cls, row):
         id, name, breed = row
         dog = cls(name, breed)
         dog.id = id
         return dog
    
    @classmethod
    def get_all(cls):
         CURSOR.execute("SELECT * FROM dogs")
         rows = CURSOR.fetchall()
         dogs = []
         for row in rows:
              dog = cls.new_from_db(row)
              dogs.append(dog)
         return dogs
    
    @classmethod
    def find_by_name(cls, name):
         CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
         row = CURSOR.fetchone()
         if row:
              dog = cls.new_from_db(row)
              return dog
         else:
              return None
         
    @classmethod
    def find_by_id(cls, id):
         CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
         row = CURSOR.fetchone()
         if row:
              dog = cls.new_from_db(row)
              return dog
         else:
              return None
         
    @classmethod
    def find_or_create_by(cls, name, breed):
         dog = cls.find_by_name(name)
         if not dog:
              dog = cls.create(name, breed)
         return dog
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))


