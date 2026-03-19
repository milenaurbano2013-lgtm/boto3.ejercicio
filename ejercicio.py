import boto3
import csv

# Clientes AWS
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

def obtener_ec2():
    instancias_info = []
    response = ec2.describe_instances()

    for reserva in response['Reservations']:
        for instancia in reserva['Instances']:
            instancias_info.append({
                'ID': instancia['InstanceId'],
                'Tipo': instancia['InstanceType'],
                'Estado': instancia['State']['Name']
            })
    return instancias_info

def obtener_s3():
    buckets_info = []
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        buckets_info.append({
            'Nombre': bucket['Name'],
            'Fecha_creacion': bucket['CreationDate']
        })
    return buckets_info

def guardar_csv(ec2_data, s3_data):
    with open('inventario_aws.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['=== EC2 ==='])
        writer.writerow(['ID', 'Tipo', 'Estado'])
        for i in ec2_data:
            writer.writerow([i['ID'], i['Tipo'], i['Estado']])

        writer.writerow([])
        writer.writerow(['=== S3 ==='])
        writer.writerow(['Nombre', 'Fecha_creacion'])
        for b in s3_data:
            writer.writerow([b['Nombre'], b['Fecha_creacion']])

if __name__ == "__main__":
    ec2_data = obtener_ec2()
    s3_data = obtener_s3()
    guardar_csv(ec2_data, s3_data)

    print("Inventario generado correctamente ✅")
    import boto3
import random
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')

def enviar_metrica():
    valor = random.randint(0, 100)

    response = cloudwatch.put_metric_data(
        Namespace='MiAplicacion',
        MetricData=[
            {
                'MetricName': 'UsoCPU',
                'Timestamp': datetime.utcnow(),
                'Value': valor,
                'Unit': 'Percent'
            }
        ]
    )

    print(f"Métrica enviada: {valor}%")

if __name__ == "__main__":
    enviar_metrica()