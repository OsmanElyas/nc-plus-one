# from app.db.connection import get_connection
# from psycopg2.extras import RealDictCursor

# def get_user(email):

#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)

#     cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (email,))
#     user = cursor.fetchone()

#     cursor.close()
#     conn.close()


#     return user
