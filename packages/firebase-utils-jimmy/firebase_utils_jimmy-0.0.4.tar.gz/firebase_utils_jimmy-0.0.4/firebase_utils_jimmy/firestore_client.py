import os
import firebase_admin
from firebase_admin import firestore, credentials
from pathlib import Path
from google.cloud.firestore_v1.base_query import FieldFilter
import firebase_admin.exceptions
from datetime import datetime

class FirestoreError(Exception):
  """Clase base para excepciones de Firestore"""
  pass

class FirestoreConnectionError(FirestoreError):
  "Se lanza error de conexion"
  pass

class FirestoreClient:
  def __init__(self, credential_path: str, use_emulator: bool = False):
    try:
      self._credential_path = credential_path
      
      if use_emulator:
        os.environ["FIRESTORE_EMULATOR_HOST"] = os.getenv("FIRESTORE_EMULATOR_HOST", "host.docker.internal:8081")

      if not credential_path.exists():
        raise FileNotFoundError(f"Credentials files not found")

      cred = credentials.Certificate(self.credential_path)
      self._app = firebase_admin.initialize_app(cred)
      self._db = firestore.client()
    except Exception as e:
      raise FirestoreConnectionError(f'Error al conectar con firebase: {str(e)}')

  @property
  def credential_path(self):
    raise AttributeError("This atribute cannot read")

  @property
  def app(self):
    return self._app

  @app.setter
  def app(self, value):
    raise AttributeError("You cannot modify this attribute")

  @property
  def db(self):
    return self._db

  @db.setter
  def db(self, value):
    raise AttributeError("You cannot modify this attribute")
                           
  def addDocument(self, data: dict, collection: str) -> str:

    if not data:
      raise AttributeError("'data' atributte its not defined.")
    if not collection:
      raise AttributeError("'collection' attribute its not defined.")
    
    try:
      insertData = {}
      dates = self.get_new_document_dates()
      insertData['createdAt'] = dates['createdAt']
      insertData['updatedAt'] = dates['updatedAt']
      update_time, user_ref = self.db.collection(collection).add(insertData)
      return user_ref.id
    except firebase_admin.exceptions.FirebaseError as fef:
      print(f'A firebase error exceptions ocurred: {fef}')
      return None
    except Exception as e:
      print(f"And error occurred: {e}")
      return None


  def searchUser(self, phonenumber: str):
    try:
      query = (self.db.collection("users").where(filter=FieldFilter("phonenumber", "==", phonenumber)).stream())
      print(f"query: {query}")
      for doc in query:
        if doc.exists:
          return doc.to_dict()
        
      print("User not found.")
      return None
    except firebase_admin.exceptions.FirebaseError as fef:
      print(f'A firebase error exceptions ocurred: {fef}')
      return None
    except Exception as e:
      print(f"And error occurred: {e}")
      return None
  
  @staticmethod
  def get_new_document_dates() -> dict[str, datetime]:
    now = datetime.now()
    return {
      "createdAt": now,
      "updatedAt": now,
    }