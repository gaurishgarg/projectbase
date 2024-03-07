import asyncio
import websockets
import streamlit as st
from aiohttp import web
async def handle_message(websocket, path):
    try:
        # Retrieve the original client address
        client_address = websocket.remote_address
        st.write(f"Client connected from: {client_address}")
        
        async for message in websocket:
            # Handle incoming message
            st.text("Received message: " + message)
            
            # Process the message and prepare response
            response = "Response to: " + message
            
            # Send the response back to the client
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosedError:
        # Handle client disconnect
        st.write("Client disconnected")

async def websocket_server():
    server = None
    try:
        # Start the WebSocket server listening on 0.0.0.0 (all available interfaces)
        server = await websockets.serve(handle_message, "0.0.0.0", 0)
        
        # Retrieve the assigned port
        assigned_port = server.sockets[0].getsockname()[1]

        async def get_assigned_port(request):
                return web.json_response({"websocket_port": assigned_port})
            
        aiohttp_app = web.Application()
        aiohttp_app.router.add_get("/get_websocket_port", get_assigned_port)
        
        aiohttp_runner = web.AppRunner(aiohttp_app)
        await aiohttp_runner.setup()
        aiohttp_site = web.TCPSite(aiohttp_runner, 'localhost', 8000)
        await aiohttp_site.start()
        
        st.write(f"WebSocket server running on port {assigned_port}")
        st.write(f"Port information available at http://localhost:8000/get_websocket_port")

        # Keep the WebSocket server running indefinitely
        await server.wait_closed()
    except OSError as e:
        st.error(f"OS Error: {e}")

def start_websocket_server():
    # Display a message indicating that the WebSocket server is starting
    st.write("Starting WebSocket server...")
    
    # Start the WebSocket server
    asyncio.run(websocket_server())
