class KamerVragenData:
  id: str
  gewijzigdOp: str
  verwijderd: bool
  datum:str
  soort:str
  
  def __init__(self, id: str, gewijzigdOp: str, verwijderd: bool, datum:str, soort:str):
    self.id = id
    self.gewijzigdOp = gewijzigdOp
    self.verwijderd = verwijderd
    self.datum = datum
    self.soort = soort
    
  def convertToDict(self):
    return {
      'id': self.id,
      'GewijzigdOp': self.gewijzigdOp,
      'Verwijderd': self.verwijderd,
      'Datum': self.datum
    }
  
  def convertFromDict(self, data):
    self.id = data['id']
    self.gewijzigdOp = data['GewijzigdOp']
    self.verwijderd = data['Verwijderd']
    self.datum = data['Datum']