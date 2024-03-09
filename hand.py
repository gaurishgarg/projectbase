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
            st.write("Received message: " + str(message))
            st.write("Sending back response")
            # Process the message and prepare response
            response = "Response to: " + str(message)

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

        st.write("Websocket started")
        # Retrieve the assigned port
        assigned_port = server.sockets[0].getsockname()[1]
        st.write("Port assigned")
        st.session_state.websocket_port = assigned_port
        st.write("Port bound")
        mydict = {}
        mydict = browser_id.copy()
        print("My dictionary is")
        print(mydict)
        st.write(mydict)
        st.write(assigned_port)

        public_ip = get_public_ip()
        st.write(public_ip)
        url = "https://long-erin-abalone-gown.cyclic.app/getdata"
    
        if "browserId" in mydict:
            st.write("projectbase-gaurish.streamlit.app:"+str(assigned_port)+"/")
        # Data to be sent in the POST request
            data = {"port": assigned_port, "url": "projectbase-gaurish.streamlit.app","browserid": mydict["browserId"]}

        # Send POST requests
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


async def get_public_ip():
    try:
        # Make an HTTP request to a service that echoes back the requester's IP address
        response = await requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text  # The response text contains the public IP address
        else:
            return f"Failed to retrieve public IP: {response.status_code}"
    except Exception as e:
        return f"Error retrieving public IP: {str(e)}"

def start_websocket_server():
    # Display a message indicating that the WebSocket server is starting
    # Start the WebSocket server
    st.write("Starting websockets")
    asyncio.run(websocket_server())


