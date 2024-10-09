import argparse

from . import Server

def run_server():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-P", "--port", type=int, help="The port number.")
    parser.add_argument("-K", "--apikey", type=str, help="The authentication key.")
    args = parser.parse_args()

    server = Server(API_KEY=args.apikey)
    server.port = args.port
    server.run()
    
