import asyncio
import websockets
import argparse
import time

async def connect_client(uri, client_id, duration):
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Client {client_id} connected to {uri}")
            start_time = time.time()
            while time.time() - start_time < duration:
                try:
                    # Receive messages to keep connection alive and simulate active client
                    msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                except asyncio.TimeoutError:
                    # No message received in 5s, that's fine, keep alive
                    pass
            print(f"Client {client_id} disconnecting.")
    except Exception as e:
        print(f"Client {client_id} error: {e}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--uri', type=str, required=True, help="WebSocket URI, e.g., ws://localhost:3333")
    parser.add_argument('--clients', type=int, required=True, help="Number of concurrent clients")
    parser.add_argument('--duration', type=int, default=120, help="Duration in seconds to hold connections")
    args = parser.parse_args()

    print(f"Starting {args.clients} websocket clients to {args.uri} for {args.duration}s")
    
    tasks = []
    for i in range(args.clients):
        tasks.append(asyncio.create_task(connect_client(args.uri, i+1, args.duration)))
        # Stagger connections slightly
        await asyncio.sleep(0.1) 
        
    await asyncio.gather(*tasks)
    print("All clients finished.")

if __name__ == "__main__":
    asyncio.run(main())
