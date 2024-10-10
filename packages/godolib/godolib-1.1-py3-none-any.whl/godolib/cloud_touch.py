import boto3
import os
import json
import pandas as pd
import numpy as np
from io import BytesIO, StringIO
import pickle
import h5py

class S3Touch():
    """
    Clase S3Touch para interactuar con Amazon S3. Permite subir archivos o directorios completos a un bucket de S3
    y leer archivos desde S3 en diferentes formatos como JSON, CSV y Numpy (.npy).

    Atributos:
    ----------
    bucket_name : str
        El nombre del bucket de S3 con el cual se desea interactuar.
    
    s3 : boto3.client
        El cliente de boto3 que permite realizar operaciones con S3.

    Métodos:
    --------
    __init__(bucket_name, access_key, secret_access_key, region_name):
        Inicializa la clase con las credenciales y la configuración para interactuar con S3.
    
    _upload_file(file_path, s3_folder=None):
        Sube un archivo único desde el sistema local a un bucket de S3.
    
    _upload_folder(folder_path, s3_folder=None):
        Sube un directorio completo de archivos desde el sistema local a un bucket de S3.
    
    write(path, s3_folder=None):
        Detecta si el path es un archivo o directorio y llama a los métodos correspondientes para subirlos a S3.
    
    read(s3_key, local_path=None):
        Lee un archivo de S3 y lo procesa en base a su extensión (JSON, CSV, Numpy).
    """
    
    def __init__(self, bucket_name, access_key, secret_access_key, region_name):
        """
        Inicializa la clase S3Touch con las credenciales y configuraciones necesarias para interactuar con S3.
        
        Parámetros:
        -----------
        bucket_name : str
            El nombre del bucket de S3 al que se subirán o leerán archivos.
        
        access_key : str
            Clave de acceso (AWS Access Key) para autenticar el cliente S3.
        
        secret_access_key : str
            Clave secreta (AWS Secret Access Key) asociada al acceso S3.
        
        region_name : str
            Región de AWS en la que se encuentra el bucket de S3.
        """
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_access_key,
                               region_name=region_name)

    def _upload_file(self, file_path, s3_folder=None):
        """
        Sube un archivo único al bucket de S3.

        Parámetros:
        -----------
        file_path : str
            Ruta completa del archivo en el sistema local que se va a subir.
        
        s3_folder : str, opcional
            Carpeta dentro del bucket de S3 donde se guardará el archivo. Si no se especifica, se sube a la raíz del bucket.
        
        Excepciones:
        ------------
        Podría generar excepciones relacionadas con permisos o accesos a S3 si el cliente no tiene acceso adecuado.
        """
        s3_key = f"{s3_folder}/{os.path.basename(file_path)}" if s3_folder else os.path.basename(file_path)
        s3_key = s3_key.lstrip('/')  # Elimina barra inicial si existe
        self.s3.upload_file(file_path, self.bucket_name, s3_key)

    def _upload_folder(self, folder_path, s3_folder=None):
        """
        Sube todos los archivos dentro de un directorio al bucket de S3, manteniendo la estructura de subcarpetas.

        Parámetros:
        -----------
        folder_path : str
            Ruta del directorio en el sistema local que se va a subir.
        
        s3_folder : str, opcional
            Carpeta dentro del bucket de S3 donde se guardará la estructura de archivos. Si no se especifica, se suben a la raíz del bucket.
        
        Excepciones:
        ------------
        Podría generar excepciones si no tiene acceso a S3 o si hay problemas con los permisos.
        """
        if not s3_folder:
            s3_folder = f'{os.path.basename(folder_path)}/'
        else:
            s3_folder = f'{s3_folder}/'
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                s3_key = os.path.join(s3_folder, relative_path).replace("\\", "/")
                self.s3.upload_file(file_path, self.bucket_name, s3_key)
                print (f'{file} succesfully wrote')

    def write(self, path, s3_folder=None):
        """
        Sube un archivo o directorio al bucket de S3. Si la ruta proporcionada es un archivo, lo sube. Si es un directorio, sube todo su contenido.

        Parámetros:
        -----------
        path : str
            Ruta del archivo o directorio que se desea subir.
        
        s3_folder : str, opcional
            Carpeta dentro del bucket de S3 donde se subirá el archivo o directorio. Si no se especifica, se sube a la raíz del bucket.
        
        Excepciones:
        ------------
        ValueError: Si la ruta proporcionada no es ni un archivo ni un directorio.
        """
        if os.path.isfile(path):
            self._upload_file(path, s3_folder)
        elif os.path.isdir(path):
            self._upload_folder(path, s3_folder)
        else:
            raise ValueError("La ruta proporcionada no es válida. Debe ser un archivo o un directorio.")
            
    def read(self, s3_key, local_path=None):
        """
        Lee un archivo desde el bucket de S3 y lo procesa según su tipo de archivo.
    
        Parámetros:
        -----------
        s3_key : str
            Clave (ruta) del archivo dentro del bucket de S3.
        
        local_path : str, opcional
            Ruta local donde se desea descargar el archivo. Si se especifica, el archivo se guardará localmente en lugar de solo procesarlo.
        
        Retorno:
        --------
        El archivo procesado, que puede ser:
        - Un diccionario (para archivos JSON).
        - Un array de Numpy (para archivos .npy).
        - Un DataFrame de pandas (para archivos .csv).
        - Un objeto Python (para archivos .pkl).
        - Un objeto h5py.File (para archivos .h5).
        
        Excepciones:
        ------------
        ValueError: Si el formato del archivo no es soportado.
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
            file_content = response['Body'].read()
    
            if s3_key.endswith('.json'):
                file = json.loads(file_content.decode('utf-8'))
            elif s3_key.endswith('.npy'):
                file = np.load(BytesIO(file_content), allow_pickle=True)
            elif s3_key.endswith('.csv'):
                file = pd.read_csv(StringIO(file_content.decode('utf-8')))
            elif s3_key.endswith('.pkl'):
                file = pickle.loads(file_content)
            elif s3_key.endswith('.h5'):
                # Crear un archivo temporal para poder abrirlo con h5py
                with open('temp_model.h5', 'wb') as f:
                    f.write(file_content)
                file = h5py.File('temp_model.h5', 'r')
            else:
                raise ValueError(f"Formato de archivo no soportado: {s3_key}")
    
            if local_path:
                with open(local_path, 'wb') as f:
                    f.write(file_content)
            
            return file
    
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            raise e

def download_directory_from_s3(aws_access_key_id, aws_secret_access_key, region_name, bucket_name, s3_folder, local_dir):
    """
    Descarga una carpeta completa de S3 a un directorio local.

    Parámetros:
    - aws_access_key_id: Tu AWS Access Key ID.
    - aws_secret_access_key: Tu AWS Secret Access Key.
    - region_name: Región de AWS donde se encuentra el bucket.
    - bucket_name: Nombre del bucket de S3.
    - s3_folder: Ruta de la carpeta dentro del bucket de S3.
    - local_dir: Directorio local donde se guardarán los archivos.
    """

    s3 = boto3.client(
        's3',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    if not s3_folder.endswith('/'):
        s3_folder += '/'

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder)
    
    if 'Contents' in response:
        for file in response['Contents']:
            file_name = file['Key']
            if not file_name.endswith('/'):
                local_file_path = os.path.join(local_dir, os.path.relpath(file_name, s3_folder))
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                s3.download_file(bucket_name, file_name, local_file_path)
                print(f"Descargado {file_name} a {local_file_path}")

def invoke_lambda_to_stop_instance(access_key, secret_access_key, region_name, instance_id):
    """
    Invoca una función Lambda de AWS para detener una instancia EC2 específica.

    Esta función utiliza las credenciales de AWS y los parámetros proporcionados para invocar 
    una función Lambda que está configurada para detener una instancia EC2. La invocación 
    se realiza de manera asíncrona (InvocationType='Event').

    Parámetros:
    -----------
    access_key : str
        Clave de acceso de AWS (AWS access key) necesaria para autenticarse en los servicios de AWS.
    
    secret_access_key : str
        Clave secreta de AWS (AWS secret access key) asociada al acceso.
    
    region_name : str
        Nombre de la región de AWS en la que se encuentra la función Lambda y la instancia EC2.
    
    instance_id : str
        ID de la instancia EC2 que se desea detener mediante la función Lambda.

    Retorna:
    --------
    response : dict
        Respuesta del cliente de Lambda de AWS, que contiene información sobre el resultado de la invocación.
    """
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name=region_name
    )

    payload = {
        'instance_id': instance_id
    }

    response = lambda_client.invoke(
        FunctionName='stop_instance_after_executed',  # Nombre de la función Lambda que detiene la instancia.
        InvocationType='Event',  # 'Event' significa que la invocación es asíncrona.
        Payload=json.dumps(payload)  # Cargar el ID de la instancia como un JSON.
    )
    print ('lambda invoked')
    return response

