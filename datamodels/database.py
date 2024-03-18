import mysql.connector


con = mysql.connector.connect(
    # user='rnovikov',
    user='root',
    password='Dend1y13',
    # password='Qwerty123',
    # host='ubuntu2',
    host='localhost',
    database='doctor'
    # database='fistech'
)
print('connect')
cur = con.cursor()



def get_data():
    request_string = """
        SELECT Symptom FROM Symptom_severity
    """
    cur.execute(request_string)
    result = cur.fetchall()



    return result



