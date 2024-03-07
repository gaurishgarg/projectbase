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
        st.write("Websocket Server created")
        # Retrieve the assigned port
        assigned_port = server.sockets[0].getsockname()[1]
        st.write("Websocket Server Port has been assigned")
        async def get_assigned_port(request):
                return web.json_response({"websocket_port": assigned_port})
        st.write("aiohttp function has been defined")    
        aiohttp_app = web.Application()
        st.write("aiohttp function web app declared")    
        aiohttp_app.router.add_get("/get_websocket_port", get_assigned_port)
        st.write("aiohttp web app route added")    
        aiohttp_runner = web.AppRunner(aiohttp_app)
        st.write("aiohttp runner innitialised")    
        await aiohttp_runner.setup()
        st.write("aiohttp runner set up")    
        aiohttp_site = web.TCPSite(aiohttp_runner, 'localhost', 9509)
        st.write("aiohttp runner declared")    
        await aiohttp_site.start()
        st.write("aiohttp site started")    
        st.write(f"WebSocket server running on port {assigned_port}")
        st.write(f"Port information available at http://projectbase-gaurish.streamlit.app:9509/get_websocket_port")

        # Keep the WebSocket server running indefinitely
        await server.wait_closed()
    except OSError as e:
        st.error(f"My OS Error: {e}")

def start_websocket_server():
    # Display a message indicating that the WebSocket server is starting
    st.write("Starting WebSocket server...")
    # Start the WebSocket server
    asyncio.run(websocket_server())
