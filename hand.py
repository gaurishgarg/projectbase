import asyncio
import websockets
import streamlit as st

async def handle_message(websocket, path):
    try:
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
    except Exception as e:
        # Handle other errors
        st.error(f"Server Error  Occured: {e}")
        # Close the WebSocket server
        await websocket.close()

async def websocket_server():
    server = None
    try:
        # Start the WebSocket server
          server = websockets.serve(handle_message, "localhost", 8765)
          async with server:
                
                # Display server running message
            st.write("WebSocket server running")
                # Keep the server running indefinitely
            await asyncio.Future()
       
    except OSError as e:    
        st.error(f"OS Error: {e}")
    finally:
        if server:
            server.ws_server.close()
        # Wait for the server to close
            await server.ws_server.wait_closed()

            st.write("Server closed")
            # start_websocket_server()


def start_websocket_server():
    # Display a message indicating that the WebSocket server is starting
    st.write("Starting WebSocket server...")
    
    # Start the WebSocket server
    asyncio.run(websocket_server())
