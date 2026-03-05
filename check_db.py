import sqlite3
import pandas as pd


def consultar_ventas():
    # Espera hasta 20 segundos si está bloqueada
    conn = sqlite3.connect('retail_history.db', timeout=20)
    # Usamos Pandas para que la tabla se vea bonita en la consola
    df = pd.read_sql_query(
        "SELECT * FROM ventas ORDER BY fecha DESC LIMIT 5", conn)
    print("📊 ÚLTIMOS REGISTROS EN LA BASE DE DATOS SQL:")
    print(df)
    conn.close()


if __name__ == "__main__":
    consultar_ventas()
