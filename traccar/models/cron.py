import psycopg2

try:
    connection = psycopg2.connect(user="",
                                  password="",
                                  host="",
                                  port="5432",
                                  database="")

    PostgreSQL_select_Query = """
        INSERT INTO gpsmap_positions (
            protocol,deviceid,servertime,devicetime,fixtime,valid,latitude,longitude,altitude,speed,course,address,attributes,status,leido,
            event,create_uid,online,create_date
        )
        SELECT
            tp.protocol, fv.id as deviceid,tp.servertime,tp.devicetime,tp.fixtime,
            1,tp.latitude,tp.longitude,tp.altitude,tp.speed,tp.course,tp.address,tp.attributes,
            CASE 				            
                WHEN tp.attributes::json->>'alarm'!='' THEN 'alarm'
                WHEN tp.devicetime + INTERVAL '8' MINUTE > tp.servertime AND tp.devicetime - INTERVAL '8' MINUTE < tp.servertime THEN 'Online'	                
                ELSE 'Offline'
            END  as status,0,
            CASE 				            
                WHEN tp.attributes::json->>'alarm'!='' THEN tp.attributes::json->>'alarm'
                WHEN tp.attributes::json->>'motion'='false' THEN 'Stopped'
                WHEN tp.attributes::json->>'motion'='true' AND tp.speed>2 THEN 'Moving'
                ELSE 'Stopped'
            END	as event,1,
            CASE 				            
                WHEN tp.devicetime + INTERVAL '5' MINUTE > tp.servertime AND tp.devicetime - INTERVAL '5' MINUTE < tp.servertime THEN true
                ELSE false
            END  as online,
            tp.servertime
                
        FROM tc_positions tp 
            JOIN tc_devices td ON tp.deviceid=td.id 
            JOIN fleet_vehicle fv ON fv.imei=td.uniqueid
        WHERE tp.read=0 
        ORDER BY tp.devicetime DESC 
    """

    cursor = connection.cursor()
    cursor.execute(PostgreSQL_select_Query)
    """
    positions = cursor.fetchall()
    for position in positions:                                       
        print("POSITIONS")
        print(position)
    """


    PostgreSQL_select_Query = """
            SELECT    count(*)
            FROM gpsmap_positions 
    """
    cursor = connection.cursor()
    cursor.execute(PostgreSQL_select_Query)
    positions = cursor.fetchall()
    for position in positions:                                       
        print("GPSMAP")
        print(position)


        
except (Exception, psycopg2.Error) as error :
    print ("Error while getting data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
