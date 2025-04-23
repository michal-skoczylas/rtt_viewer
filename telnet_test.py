import asyncio
import telnetlib3

async def test_telnet_connection(port="19021"):
    try:
        print(f"🔌 Attempting to connect to localhost:{port}...")
        reader, writer = await telnetlib3.open_connection(
            'localhost', 
            port,
            connect_minwait=0.1,
            connect_maxwait=0.5
        )
        
        print("✅ Connection successful!")
        print("Type messages to send (or 'quit' to exit)")
        
        while True:
            message = input("> ")
            if message.lower() == 'quit':
                break
                
            writer.write(message + "\n")
            await writer.drain()
            
            data = await reader.read(1024)
            if data:
                print(f"📥 Received: {data.strip()}")
                
    except ConnectionRefusedError:
        print("❌ Connection refused. Is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()
        print("✅ Connection closed")

if __name__ == "__main__":
    asyncio.run(test_telnet_connection())