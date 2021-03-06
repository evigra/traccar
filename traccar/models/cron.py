import psycopg2

try:
    print("Conectando")
    connection = psycopg2.connect(user="admin_evigra",
                                  password="EvG30JiC06",
                                  host="odoo.solesgps.com",
                                  port="5432",
                                  database="produccion")
    print("Conectado!! ")
    print("Buscando positions")
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
                WHEN tp.devicetime + INTERVAL '8' MINUTE > tp.servertime AND tp.devicetime - INTERVAL '8' MINUTE < tp.servertime THEN true
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
    print("Positions insertadas !!")

    print("Modificando Positions")
    PostgreSQL_select_Query = """
        UPDATE tc_positions SET read=1 WHERE read=0
    """
    cursor = connection.cursor()
    cursor.execute(PostgreSQL_select_Query)

    
    PostgreSQL_select_Query = """
        UPDATE fleet_vehicle SET positionid= gp.id
        FROM gpsmap_positions gp
        WHERE concat(gp.deviceid,gp.devicetime) IN 
        (
          SELECT  concat(deviceid, MAX(devicetime)) FROM gpsmap_positions
          where devicetime>=NOW()::date
          GROUP BY deviceid
        )    
    """
    cursor = connection.cursor()
    cursor.execute(PostgreSQL_select_Query)
    
    print("Modificando position del Vehiculo")
    """
    positions = cursor.fetchall()
    for position in positions:                                       
        print("GPSMAP")
        print(position)
    """

        
except (Exception, psycopg2.Error) as error :
    print ("Error while getting data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
