import asyncio
import websockets
import streamlit as st
from streamlit.logger import get_logger
async def handle_message(websocket, path):
    async for message in websocket:
        st.text("Received message: " + message)

async def websocket_server():
    async with websockets.serve(handle_message, "localhost", 8765):
        await asyncio.Future()

def startwebserver():
    # Start the websocket server in a background task
    asyncio.run(websocket_server())

