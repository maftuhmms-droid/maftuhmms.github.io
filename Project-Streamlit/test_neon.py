import psycopg2

try:
    conn = psycopg2.connect(
        host="ep-cool-salad-azebuawg.c-3.ap-southeast-1.aws.neon.tech",
        dbname="neondb",
        user="neondb_owner",
        password="npg_ZtFEK6dNXYR2",
        port=5432,
        sslmode="require",
        channel_binding="require"
    )

    print("Berhasil terkoneksi!")
    conn.close()

except Exception as e:
    print(e)