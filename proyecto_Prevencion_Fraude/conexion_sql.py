from faker import Faker
import random
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta

fake = Faker()

# 
# CONEXIÓN SQL SERVER

server = 'DARIELPC'
database = 'FraudAnalyticsDB'

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)

# CONFIGURACIÓN

NUM_CLIENTES = 500
NUM_TRANSACCIONES = 15000

tipos_cliente = [
    'Institución Pública',
    'Empresa Privada',
    'Suplidor Gobierno',
    'Aseguradora'
]

sectores = [
    'Finanzas',
    'Construcción',
    'Salud',
    'Tecnología',
    'Telecomunicaciones',
    'Seguros'
]

tipos_transaccion = [
    'Transferencia',
    'Pago',
    'Compra',
    'Retiro'
]

metodos_pago = [
    'Tarjeta',
    'Transferencia Bancaria',
    'ACH',
    'Cheque'
]

paises_riesgo = [
    'Rusia',
    'Corea del Norte',
    'Irán'
]

# 
# GENERAR CLIENTES
# 

clientes = []

for i in range(1, NUM_CLIENTES + 1):

    cliente = {
        'id_cliente': i,
        'nombre_empresa': fake.company(),
        'tipo_cliente': random.choice(tipos_cliente),
        'sector': random.choice(sectores),
        'pais': 'República Dominicana',
        'ciudad': fake.city(),
        'fecha_registro': fake.date_between(
            start_date='-5y',
            end_date='today'
        ),
        'score_riesgo': round(random.uniform(1, 100), 2)
    }

    clientes.append(cliente)

df_clientes = pd.DataFrame(clientes)

# INSERTAR CLIENTES

df_clientes.to_sql(
    'clientes_empresariales',
    engine,
    if_exists='append',
    index=False
)

# GENERAR TRANSACCIONES

transacciones = []

for i in range(1, NUM_TRANSACCIONES + 1):

    id_cliente = random.randint(1, NUM_CLIENTES)

    monto = round(random.uniform(1000, 5000000), 2)

    intentos = random.randint(0, 10)

    pais = random.choice(
        ['República Dominicana'] * 9 +
        paises_riesgo
    )

    dispositivo_nuevo = random.choice([0,1])

    multiples_ips = random.choice([0,1])

    hora = random.randint(0,23)

    fuera_horario = 1 if hora <= 5 else 0

    pais_riesgo = 1 if pais in paises_riesgo else 0

    fraude = 0

    # 
    # REGLAS DE FRAUDE

    score_fraude = 0

    if monto > 2000000:
        score_fraude += 1

    if intentos > 5:
        score_fraude += 1

    if pais_riesgo == 1:
        score_fraude += 1

    if dispositivo_nuevo == 1:
        score_fraude += 1

    if multiples_ips == 1:
        score_fraude += 1

    if fuera_horario == 1:
        score_fraude += 1

    if score_fraude >= 4:
        fraude = 1

    transaccion = {

        'id_transaccion': i,

        'id_cliente': id_cliente,

        'fecha_transaccion':
            fake.date_time_between(
                start_date='-1y',
                end_date='now'
            ),

        'monto_transaccion': monto,

        'tipo_transaccion':
            random.choice(tipos_transaccion),

        'metodo_pago':
            random.choice(metodos_pago),

        'moneda': 'DOP',

        'pais_origen': pais,

        'ciudad_origen': fake.city(),

        'ip_dispositivo': fake.ipv4(),

        'dispositivo_nuevo': dispositivo_nuevo,

        'intentos_fallidos': intentos,

        'transacciones_24h':
            random.randint(1,20),

        'promedio_historico_cliente':
            round(random.uniform(1000,500000),2),

        'desviacion_monto':
            round(random.uniform(0,1000000),2),

        'pais_alto_riesgo': pais_riesgo,

        'transaccion_fuera_horario':
            fuera_horario,

        'multiples_ips': multiples_ips,

        'fraude': fraude
    }

    transacciones.append(transaccion)

df_transacciones = pd.DataFrame(transacciones)

# 
# INSERTAR TRANSACCIONES
# 

df_transacciones.to_sql(
    'transacciones_financieras',
    engine,
    if_exists='append',
    index=False
)

print("Datos generados correctamente.")