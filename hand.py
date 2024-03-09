import asyncio
import websockets
import streamlit as st

async def handle_message(websocket, path):
    try:
        # Retrieve the original client address
        st.write("Client connected")
        client_address = websocket.remote_address
        st.write("Client address is ")
        st.write(client_address)
        async for message in websocket:
            # Handle incoming message
            st.write("Received message: " + message)
            st.write("Sending back response")
            # Process the message and prepare response
            response = "Response to: " + message

            st.write(response)
            # Send the response back to the client
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosedError:
        st.write("You disconnected")
        print("client disconnected")
        # Handle client disconnect

async def websocket_server():
    server = None
    try:
        # Start the WebSocket server listening on 0.0.0.0 (all available interfaces)
        browser_id = st.query_params.to_dict()

        server = await websockets.serve(handle_message, "localhost", 0)
        # Retrieve the assigned port
        assigned_port = server.sockets[0].getsockname()[1]
        st.session_state.websocket_port = assigned_port
        mydict = {}
        mydict = browser_id.copy()
        print("My dictionary is")
        print(mydict)
        st.write(mydict)
        st.write(assigned_port)
        url = "https://long-erin-abalone-gown.cyclic.app/getdata"
    
        if "browserId" in mydict:
            st.write("ws://projectbase-gaurish.streamlit.app:"+str(assigned_port)+"/")
        # Data to be sent in the POST request
            data = {"port": assigned_port, "url": "projectbase-gaurish.streamlit.app","browserid": mydict["browserId"]}

        # Send POST request
            response = requests.post(url, json=data)

        # Check if the request was successful
            if response.status_code == 200:
                st.write('POST request successful!')
            else:
                st.write('POST request failed:', response.status_code)
     
        await asyncio.Future()
        
    except OSError as e:
        st.error(f"My OS Error: {e}")
    
import requests

# URL of the Node.js server



def start_websocket_server():
    # Display a message indicating that the WebSocket server is starting
    # Start the WebSocket server
    asyncio.run(websocket_server())


