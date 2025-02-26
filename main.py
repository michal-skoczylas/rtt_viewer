# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import asyncio
import telnetlib3


from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


async def read_rtt():
    #parameters
    host = "localhost"
    port = 19021
    
    print(f"Connecting with {host}:{port}")
    
    #Connect to telnet
    reader, writer  = await telnetlib3.open_connection(host,port)
    
    print("Connected with RTT, Waiting for data...")
    
    try:
        #Continous reading
        while True:
            data = await reader.read(1024) #Read 1024 bytes
            if data:
                print("Receiveed: ",data.strip())
                
            await asyncio.sleep(0.1)
    except Exception as e:
        print("Error: ",e)
    finally:
        print("Closing connection")
        writer.close()
        await writer.wait_closed()
        
    
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    asyncio.run(read_rtt())
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
