## Mepaquetar la libreria
python -m build

## Publicar una nueva version
twine upload dist/*

## Uso
from firebase_utils_jimmy import FirebaseClient

client = FirebaseClient(credential_path="ruta_a_credenciales.json")
client.initialize_app()
client.add_document("users", {"name": "Jimmy", "age": 34})
