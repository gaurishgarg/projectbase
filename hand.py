import asyncio
import websockets
import streamlit as st

async def handle_message(websocket, path):
    try:
        # Retrieve the original client address
        client_address = websocket.remote_address
        
        async for message in websocket:
            # Handle incoming message
            st.text("Received message: " + message)
            
            # Process the message and prepare response
            response = "Response to: " + message
            
            # Send the response back to the client
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosedError:
        print("client disconnected")
        # Handle client disconnect

async def websocket_server():
    server = None
    try:
        # Start the WebSocket server listening on 0.0.0.0 (all available interfaces)
        server = await websockets.serve(handle_message, "0.0.0.0", 0)
        # Retrieve the assigned port
        assigned_port = server.sockets[0].getsockname()[1]
        st.session_state.websocket_port = assigned_port

        url = 'https://streamcom.onrender.com/getdata'

        # Data to be sent in the POST request
        data = {"port": assigned_port, url: "ws://projectbase-gaurish.streamlit.app"}

        # Send POST request
        response = requests.post(url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            print('POST request successful!')
        else:
            print('POST request failed:', response.status_code)
        # Injecting script
        script = """
        <script>
            window.streamlitInfo = {
                port: {assigned_port},
                url: 'ws://projectbase-gaurish.streamlit.app'
            };
        </script>
        """
        st.markdown(script, unsafe_allow_html=True)
        st.json({"port": assigned_port, "url":"ws://projectbase-gaurish.streamlit.app"})
        await server.wait_closed()
    except OSError as e:
        st.error(f"My OS Error: {e}")
    
import requests

# URL of the Node.js server



def start_websocket_server():
    # Display a message indicating that the WebSocket server is starting
    # Start the WebSocket server
    asyncio.run(websocket_server())


