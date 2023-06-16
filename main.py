from fastapi import FastAPI
# Importar el módulo

app = FastAPI()
# Creación de la aplicación app

@app.get('/') #Decorador con la ubicación
def message():
    return "Hello world!"
#Función a ejecutar
