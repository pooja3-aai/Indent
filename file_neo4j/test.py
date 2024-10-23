except xmlrpc.client.Fault as e:
    print(f"XML-RPC Fault: {e}")
except Exception as e:
    print(f"Error: {e}")