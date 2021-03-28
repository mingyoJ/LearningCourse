from pynetdicom import AE, debug_logger

debug_logger()

ae = AE()

# Add a presentation context (Need at least 1 presentation context)
ae.add_requested_context("1.2.840.10008.1.1")

# Association is subclass of threading.Thread
assoc = ae.associate("localhost", 11112)
if assoc.is_established:
    print("Association established with echo SCP!")
    status = assoc.send_c_echo()
    assoc.release()
else:
    print("Failed to associate")
