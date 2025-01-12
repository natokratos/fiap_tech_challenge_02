import boto3
from botocore.client import ClientError
import pandas as pd
import os

class AwsS3:

    def __init__(self):
        try:
            if os.environ['AWS_ENDPOINT_URL']:
                self.aws_endpoint = os.environ['AWS_ENDPOINT_URL']
        except KeyError as e:
            self.aws_endpoint = 'http://localhost:4566'
        print(f"AWS_ENDPOINT_URL [ {self.aws_endpoint} ]")
        #self.source_url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'

    def upload_file(self, bucket_name, file_name):
        print(f"Carregando o arquivo [{file_name}] para o bucket [{bucket_name}] ...")
        try:
            boto3.client(service_name='s3', endpoint_url=self.aws_endpoint).head_bucket(Bucket=bucket_name)
        except ClientError:
            print(f"O Bucket [{bucket_name}] NAO existe!!!")
            return None

        print(f"O Bucket [{bucket_name}] EXISTE!!!")

        try:
            df = pd.read_csv(file_name, encoding = "ISO-8859-1")
            print(f"Convertendo o arquivo [{file_name}] para parquet...")
            parquet_file = file_name.replace(".csv", ".parquet").split("/")[-1]
            df.to_parquet(parquet_file)
            print(f"Obtendo o conteudo do arquivo [{parquet_file}] ...")
            parquet_content=""
            with open(parquet_file, mode='rb') as f:
                parquet_content = f.read()
            print(f"Enviando o arquvo [{file_name}] para o bucket [{bucket_name}] ...")
            bucket = boto3.client(service_name='s3', endpoint_url=self.aws_endpoint).put_object(Bucket=bucket_name, Key=parquet_file, Body=parquet_content)
        except Exception as e:
            print(f"Exception {repr(e)}")
            return None


