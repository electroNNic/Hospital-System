#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "postgres"
    passwd = "123456"
    myHost = "localhost"
    myPort = "5432"


    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

'''
Validate staff based on username and password
'''
def checkLogin(login, password):

    conn = openConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT UserName, FirstName, LastName, Email FROM Administrator
                       WHERE UserName = %s AND Password = %s""", (login, password))

        login_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return login_data


    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        cursor.close()
        conn.close()
        return None


'''
List all the associated admissions records in the database by staff
'''
def findAdmissionsByAdmin(login):

    conn = openConnection()
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT A.AdmissionID, At.AdmissionTypeName, De.DeptName, 
        COALESCE(TO_CHAR(A.DischargeDate, 'DD-MM-YYYY'), '') AS Discharge_Date, 
            COALESCE(A.Fee::TEXT, '') AS Fee, CONCAT(P.FirstName,'\n', P.LastName) AS FullName,COALESCE(A.Condition, '') AS Condition
                       FROM Admission A
                       JOIN AdmissionType At ON A.AdmissionType = At.AdmissionTypeID
                       JOIN Department De ON A.Department = De.DeptId
                       JOIN Patient P ON A.Patient = P.PatientID
                       WHERE A.Administrator = %s
                       ORDER BY A.DischargeDate DESC NULLS LAST,FullName ASC, At.AdmissionTypeName DESC
                       ''', (login,))

        admissions = []
        while True:
            row = cursor.fetchone()
            if row is None:
                break

            admission = {
                'admission_id': row[0],
                'admission_type': row[1],
                'admission_department': row[2],
                'discharge_date': row[3],
                'fee': row[4],
                'patient': row[5],
                'condition': row[6]
            }
            admissions.append(admission)

        cursor.close()
        conn.close()
        return admissions

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        cursor.close()
        conn.close()
        return None


'''
Find a list of admissions based on the searchString provided as parameter
See assignment description for search specification
'''
def findAdmissionsByCriteria(searchString):
    conn = openConnection()
    cursor = conn.cursor()

    try:
        cursor.callproc('findAdmissionsByCriteria',[searchString,])
        admissions = []
        while True:
            row = cursor.fetchone()
            if row is None:
                break

            admission = {
                'admission_id': row[0],
                'admission_type': row[1],
                'admission_department': row[2],
                'discharge_date': row[3],
                'fee': row[4],
                'patient': row[5],
                'condition': row[6]
            }
            admissions.append(admission)

        cursor.close()
        conn.close()
        return admissions

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        cursor.close()
        conn.close()
        return None


'''
Add a new addmission 
'''
def addAdmission(type, department, patient, condition, admin):
    conn = openConnection()
    cursor = conn.cursor()

    try:
        cursor.callproc('add_admission', [type, department, patient, condition, admin])
        result = cursor.fetchone()
        conn.commit()

        cursor.close()
        conn.close()
        return result[0]

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        cursor.close()
        conn.close()
        return False



'''
Update an existing admission
'''
def updateAdmission(id, type, department, dischargeDate, fee, patient, condition):
    conn = openConnection()
    cursor = conn.cursor()

    try:
        cursor.callproc('update_Admission_func', [id, type, department, dischargeDate, fee, patient, condition])
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        cursor.close()
        conn.close()
        return False

