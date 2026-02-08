from model.connection import *



class Station(Base):
    def __init__(self, ville = '', title = '', address = '', tel = '', longitude = 0, latitude = 0, localisation = '', hours = '', stock = 'disponible', password = ''):
        self.ville = ville
        self.title = title
        self.address = address
        self.tel = tel
        self.longitude = longitude
        self.latitude = latitude
        self.localisation = localisation
        self.hours = hours
        self.stock = stock
        self.password = password
        self.Session = sessionmaker(bind = engine)

    __tablename__ = 'Station'
    id = Column('id', Integer, primary_key = True, autoincrement = True)
    ville = Column('ville', String(255))
    title = Column('title', String(255))
    address = Column('address', String(255))
    tel = Column('tel', String(255))
    longitude = Column('longitude', Float)
    latitude = Column('latitude', Float)
    localisation = Column('localisation', String(511))
    hours = Column('hours', String(255))
    stock = Column('stock', String(255))


    def SearchStation(self):
        session = self.Session()
        result = session.query(Station).filter(Station.title == self.title and Station.password == self.password).first()
        session.commit()

        if result == None:
            return False
        return True
    
    
    def Search(self):
        session = self.Session()
        result = session.query(Station).filter(Station.title == self.title).first()
        session.commit()

        if result == None:
            return False
        return True
    
    
    def Get_id(self):
        session = self.Session()
        result = session.query(Station).filter(Station.title == self.title).first()
        return result.id
    
    
    def Get_station(self):
        session = self.Session()
        result = session.query(Station).filter(Station.title == self.title).first()
        return result
    
    
    def Get_all(self):
        session = self.Session()
        result = session.query(Station).all()
        return result
    
    def Update(self, title):
        session = Session()
        result = session.query(Station).filter(Station.title == title).first()
        if result != None:
            if self.ville != '':
                result.ville = self.ville
            if self.title != '':
                result.title = self.title
            if self.tel != '':
                result.tel = self.tel
            if self.address != '':
                result.address = self.address
            if self.longitude != 0:
                result.longitude = self.longitude
            if self.latitude != 0:
                result.latitude = self.latitude
            if self.localisation != '':
                result.localisation = self.localisation
            if self.hours != '':
                result.hours = self.hours
            if self.stock != '':
                result.stock = self.stock
            session.commit()
            return True
        return False
        

    

    def Connexion(self):
        session = self.Session()
        result = session.query(Station).filter(Station.title == self.title and Station.password == self.password).first()
        if result == None:
            return False
        return True

    def Add_station(self):
        if self.Search():
            print('Une station similaire existe deja')
        else:
            try:
                session = self.Session()
                session.add(self)
                session.commit()
                session.refresh(self)
            except(sqlalchemy.exc.IntegrityError):
                print("Erreur Un tuple avec le meme id existe deja")
                

Base.metadata.create_all(engine)