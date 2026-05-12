import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="7007", port=5432
)
cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS person(
            id INT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            gender CHAR
            );
""")
# cur.execute("""INSERT INTO person (id,name,age,gender) VALUES
#             (1, 'Gleb', 18, 'm'),
#             (2, 'Max', 19, 'm'),
#             (3, 'Nazar', 38, 'm'),
#             (4, 'John', 22, 'm')""")

cur.execute("""SELECT * FROM person WHERE name='Gleb';""")
print(cur.fetchone())
cur.execute("""SELECT * FROM person WHERE age<50;""")
for row in cur.fetchall():
    print(row)


sql = cur.mogrify(
    """SELECT * FROM person WHERE starts_with(name,%s) AND age<%s;""", ("J", 50)
)
print(sql)
cur.execute(sql)
print(cur.fetchall())

conn.commit()
cur.close()
conn.close()
