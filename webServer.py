# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    # Create a server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("127.0.0.1", port))

    # Start listening for incoming client connections
    serverSocket.listen(1)  # Listen for one client at a time

    print(f"Server listening on port {port}...")

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept incoming connection

        try:
            message = connectionSocket.recv(1024)  # Receive the client's request message
            filename = message.split()[1]  # Get the filename from the request (e.g., "/index.html")

            # Open the requested file (skip the leading '/')
            try:
                f = open(filename[1:], 'r')  # Open the file in read mode
            except FileNotFoundError:
                # If the file is not found, send a 404 error
                error_message = b"HTTP/1.1 404 Not Found\r\n" \
                                b"Content-Type: text/html; charset=UTF-8\r\n" \
                                b"Server: Python Web Server\r\n" \
                                b"Connection: close\r\n" \
                                b"\r\n" \
                                b"<html><body><h1>404 Not Found</h1></body></html>"
                connectionSocket.send(error_message)  # Send the error message to the client
                connectionSocket.close()  # Close the connection
                continue  # Skip further processing and go back to accepting new connections

            # If file is found, read its content
            content = f.read()  # Read the entire file content
            f.close()  # Close the file after reading

            # Prepare the HTTP response headers
            outputdata = b"HTTP/1.1 200 OK\r\n" \
                         b"Content-Type: text/html; charset=UTF-8\r\n" \
                         b"Server: Python Web Server\r\n" \
                         b"Connection: close\r\n" \
                         b"Content-Length: " + str(len(content)).encode() + b"\r\n" \
                         b"\r\n"  # Blank line to separate headers and body

            # Send the response (headers + content) in one go
            response = outputdata + content.encode()  # Make sure to encode content as bytes
            connectionSocket.send(response)  # Send the response

        except Exception as e:
            # Handle unexpected exceptions here (e.g., socket issues)
            print(f"Error occurred: {e}")
            error_message = b"HTTP/1.1 500 Internal Server Error\r\n" \
                            b"Content-Type: text/html; charset=UTF-8\r\n" \
                            b"Server: Python Web Server\r\n" \
                            b"Connection: close\r\n" \
                            b"\r\n" \
                            b"<html><body><h1>500 Internal Server Error</h1></body></html>"
            connectionSocket.send(error_message)  # Send the error message to the client

        finally:
            # Close the client connection socket
            connectionSocket.close()

    # Commented out as mentioned in the comments (do not uncomment in Gradescope)
    # serverSocket.close()
    # sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
