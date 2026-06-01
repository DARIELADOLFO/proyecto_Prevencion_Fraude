CREATE DATABASE FraudAnalyticsDB;
GO

USE FraudAnalyticsDB;
GO


CREATE TABLE clientes_empresariales (
    id_cliente INT PRIMARY KEY,
    nombre_empresa VARCHAR(150),
    tipo_cliente VARCHAR(50),
    sector VARCHAR(100),
    pais VARCHAR(100),
    ciudad VARCHAR(100),
    fecha_registro DATE,
    score_riesgo FLOAT
);


CREATE TABLE transacciones_financieras (
    id_transaccion INT PRIMARY KEY,
    id_cliente INT,
    fecha_transaccion DATETIME,
    monto_transaccion DECIMAL(18,2),
    tipo_transaccion VARCHAR(50),
    metodo_pago VARCHAR(50),
    moneda VARCHAR(10),

    pais_origen VARCHAR(100),
    ciudad_origen VARCHAR(100),
    ip_dispositivo VARCHAR(50),

    dispositivo_nuevo BIT,
    intentos_fallidos INT,
    transacciones_24h INT,

    promedio_historico_cliente DECIMAL(18,2),
    desviacion_monto DECIMAL(18,2),

    pais_alto_riesgo BIT,
    transaccion_fuera_horario BIT,
    multiples_ips BIT,

    fraude BIT,

    FOREIGN KEY (id_cliente)
    REFERENCES clientes_empresariales(id_cliente)
);


CREATE TABLE alertas_fraude (
    id_alerta INT PRIMARY KEY,
    id_transaccion INT,
    nivel_riesgo VARCHAR(20),
    descripcion_alerta VARCHAR(255),
    fecha_alerta DATETIME,

    FOREIGN KEY (id_transaccion)
    REFERENCES transacciones_financieras(id_transaccion)
);


SELECT * FROM transacciones_financieras

SELECT * FROM clientes_empresariales

select * from alertas_fraude

select * from predicciones_fraude