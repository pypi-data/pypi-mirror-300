import random
import socket
import struct
import sys
import hashlib
import time
from collections import deque, OrderedDict
import threading
import pickle
from loguru import logger
from cryptography.fernet import Fernet
import urllib.request
# import requests

# Self Imports
from libChord import chord

# Global Variables
GLOBAL_LOOPBACK_IP = "127.0.0.1"


def get_ip_port(testing: bool) -> tuple:
    """Gets the public IP address and port of the client machine."""
    if testing:
        hostname = socket.gethostname()  # LOCAL TESTING
        ip_addr = socket.gethostbyname(hostname)  # LOCAL TESTING
    else:
        ip_addr = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')

    # Use an external service to get the public IP
    # public_ip = requests.get('https://api.ipify.org').text

    port = 0

    return ip_addr, port


class Node:
    """Node class that is part of the chord network. It is not recommended to create a Node class directly
    but rather use join() function to join an already existing chord network or create your own chord network using Chord class."""
    __BUFFER = 4096
    __TIMEOUT = 450  # Default timeout for all operations

    # Request Types
    __GET_INIT_DETS = 100

    __LOOKUP_REQ = 111
    __JOIN_REQ = 222

    # Central Hub Functionality
    __M_CHORD_UPDATE_REQ = 233
    __M_CHORD_DELETE_REQ = 244

    __NOTIFY_REQ = 333
    __CHECK_PRED_REQ = 444

    # Stabilize Requests
    __STAB_DICT_REQ = 555
    __STAB_REQ = 595

    __LEAVE_REQ = 999

    __SEND_DATA_REQ = 1001

    def __init__(self, port: int, ip_addr: str, chord_obj: 'chord.Chord' = None, key_space: int = None) -> None:
        # [INFO] Socket Initialization
        try:
            self.node_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.node_sock.bind((ip_addr, port))
            ip_addr, port = self.node_sock.getsockname()
        except socket.error as E:
            print("Chord Network Initialization Error: ", E)
            print("[ERROR] Something went wrong. Please try again.")
            self.node_sock.close()
            return

        self.__LEAVE = False

        self.ip_addr = ip_addr
        self.port = port
        self.address = (self.ip_addr, self.port)

        # Chord class object instance
        self.__chord_obj = chord_obj

        # M of main chord node
        self.node_M = None

        # Key space of main chord node
        self.node_keySpace = key_space

        # Is the main chord Node a central hub type
        self.isCentralHub = False

        # Encryption Key
        self.__enKey = None

        # Address of main chord node
        if self.__chord_obj is not None:
            self.m_chord_node_addr = self.address
            if self.__chord_obj.central_hub:
                self.isCentralHub = True
            self.__enKey = self.__chord_obj._enKey
            self.node_M = self.__chord_obj._M
            self.node_keySpace = self.__chord_obj.KEY_SPACE
        else:
            self.m_chord_node_addr = None

        # self.uid = uid
        # self.id = get_hash(uid)
        self.id = chord.get_hash(self.ip_addr + "," + str(self.port), self.node_keySpace)

        self.successor_id = self.id
        self.successor_addr = self.address
        self.predecessor_id = None
        self.predecessor_addr = None
        self.finger_table = OrderedDict()
        self.successor_list = deque(maxlen=self.node_M)  # successor_list is a deque list of tuples where 1st element = id and 2nd element = (ip, port) address

        # [INFO] Socket Listen Setup
        try:
            self.node_sock.listen(self.node_keySpace)
        except socket.error as E:
            logger.error("Chord Network Initialization Error: ", E)
            print("[ERROR] Something went wrong. Please try again.")
            self.node_sock.close()
            return

    @property
    def _chord_obj(self):
        return self.__chord_obj

    @property
    def _enKey(self):
        """Getter: This will get the _enKey."""
        raise AttributeError("This attribute is write-only.")

    @_enKey.setter
    def _enKey(self, value):
        """Setter: This will set the _enKey."""
        self.__enKey = value

    @staticmethod
    def __encrypt(key, data):
        # For Fernet encryption
        cipher = Fernet(key)
        # Serialize the data with pickle
        serialized_data = pickle.dumps(data)
        # Encrypt the serialized data
        encrypted_data = cipher.encrypt(serialized_data)
        return encrypted_data

    @staticmethod
    def __decrypt(key, encrypted_data):
        # For Fernet decryption
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data)
        # Deserialize the original data
        data = pickle.loads(decrypted_data)
        return data

    @staticmethod
    def get_elements(dct, k):
        """Get dictionary Node addresses that come after or before the specified ID."""
        sorted_keys = list(sorted(dct.keys()))  # Get the keys of the dictionary as a list
        if k in sorted_keys:
            index = sorted_keys.index(k)
            if len(sorted_keys) == 1:
                # If there's only one element, return it
                return {k: dct[k]}
            elif index == len(sorted_keys) - 1:
                # If k is the last key, get all key-value pairs before x
                return {k: dct[k] for k in sorted_keys[:index]}
            else:
                # If k is not the last key, get all key-value pairs after x
                return {k: dct[k] for k in sorted_keys[index + 1:]}
        else:
            return None  # If k is not in the dictionary

    def __node_listening(self, timeout: int = 300) -> None:  ## NON-DAEMON THREAD ##
        # [INFO] Listening Thread for Incoming Connections
        logger.info("Joined Chord Network Successfully. Listening....")
        # These variables are only created once
        accept_connections = True
        processor_threads = []
        while accept_connections:
            try:
                inc_conn_obj, inc_address = self.node_sock.accept()  # Code Block
                inc_conn_obj.settimeout(timeout)  # Default is 300 sec; 5 Min
            except socket.error as E:
                if self.__LEAVE:
                    accept_connections = False
                    break
                # self.node_sock.close() # No need to close here because the Node should keep listening regardless
                logger.exception("Listening Thread Exception: ", E)
                print("[ERROR] Something went wrong.")
                continue

            # Request Process Threading
            # Each processor thread closes after processing a request.
            process_thread = threading.Thread(target=self.processor_thread, args=(inc_conn_obj, inc_address), name="Processor-Thread", daemon=True)
            process_thread.start()
            processor_threads.append(process_thread)

        if not accept_connections:
            for thread in processor_threads:
                thread.join()
            self.node_sock.close()  # This will actually close the socket
            return

    def start_listen(self, timeout: int = 300) -> None:
        """Start listening for incoming connections to this Node."""
        listen_thread = threading.Thread(target=self.__node_listening, args=(timeout,), name="Listening-Thread")
        listen_thread.daemon = False  # This has to be False because the main thread has no other work to do after initiating listen()
        listen_thread.start()

        # Start all other threads
        stabilize_thread = threading.Thread(target=self.__stabilize, args=(), name="Stabilize-Thread")
        stabilize_thread.daemon = True
        fix_finger_thread = threading.Thread(target=self.__fix_fingers, args=(), name="FixFinger-Thread")
        fix_finger_thread.daemon = True
        check_pred_thread = threading.Thread(target=self.__check_predecessor, args=(), name="CheckPred-Thread")
        check_pred_thread.daemon = True

        stabilize_thread.start()
        fix_finger_thread.start()
        check_pred_thread.start()

    @staticmethod
    def encrypt(data):
        """Encrypt data using Fernet."""
        # Generate a key for Fernet encryption
        key = Fernet.generate_key()
        cipher = Fernet(key)
        # Serialize the data with pickle
        serialized_data = pickle.dumps(data)
        # Encrypt the serialized data
        encrypted_data = cipher.encrypt(serialized_data)
        return key, encrypted_data

    @staticmethod
    def recv_all(sock, length):
        """Receive exactly 'length' bytes from the socket."""
        data = b''
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                raise EOFError("Connection closed before receiving all data")
            data += packet
        return data

    def processor_thread(self, inc_conn_obj, inc_address):  ## DAEMON THREAD ##
        """Processor thread for processing each request to a Node. Each processor thread will close after processing the request"""
        try:
            # First, receive the length of the data (4 bytes)
            length_data = Node.recv_all(inc_conn_obj, 4)  # Code Block  # This is in Big Endian C-struct format
            data_length = struct.unpack('!I', length_data)[0]  # Unpack this length number to use
            # Then, receive the actual data
            full_data = Node.recv_all(inc_conn_obj, data_length)
            inc_data_form = pickle.loads(full_data)
            request_type = inc_data_form[0]
            assert isinstance(request_type, int), "Request Type Error. Something went wrong."
        except (socket.error, ValueError) as E:
            logger.exception("Listening Thread Exception: ", E)
            return

        try:
            # Lookup Request
            if request_type == self.__LOOKUP_REQ:
                # inc_data_form[1] is id of the node that is trying to find its successor in the ring
                id_to_find = inc_data_form[1]
                found_successor = self.__find_successor(id_to_find)  # This returns a (tuple)
                fid = found_successor[0]
                faddr = found_successor[1]
                if self.m_chord_node_addr is not None:  # This is ((id, (addr)), (addr), M)
                    n_data = {"fid": fid, "faddr": faddr, "m_chord_addr": self.m_chord_node_addr,
                              "node_M": self.node_M, "centralHub": self.isCentralHub}

                    # Send length of data first for iterative recv
                    b_data = pickle.dumps(n_data)  # Byte Stream Data
                    length = struct.pack('!I', len(b_data))  # Pack the length as a 4-byte integer (network byte order-Big Endian)
                    # Encrypt here
                    inc_conn_obj.sendall(length)  # Send the length first
                    inc_conn_obj.sendall(b_data)  # Then send the actual serialized data

                    logger.info("Lookup Request Served")

            # Get Keyspace and enKey Request
            elif request_type == self.__GET_INIT_DETS:
                if self.node_keySpace is not None:
                    k_data = {"enKey": self.__enKey,
                              "node_keySpace": self.node_keySpace}
                    # The only non-encrypt data transfer for the fresh node

                    # Send length of data first for iterative recv
                    b_data = pickle.dumps(k_data)  # Byte Stream Data
                    length = struct.pack('!I',len(b_data))  # Pack the length as a 4-byte integer (network byte order-Big Endian)
                    # Encrypt here
                    inc_conn_obj.sendall(length)  # Send the length first
                    inc_conn_obj.sendall(b_data)  # Then send the actual serialized data

                    logger.info("Get Initial Details Request Served")

            # Join Request
            elif request_type == self.__JOIN_REQ:
                new_predecessor = inc_data_form[1]
                # Check if I got 'None' or corrupted tuple
                if new_predecessor is not None:
                    new_predecessor_id, new_predecessor_addr = new_predecessor
                    # If I have no predecessor
                    if self.predecessor_id is None:
                        self.predecessor_id = new_predecessor_id
                        self.predecessor_addr = new_predecessor_addr
                    # I have a predecessor, but need to check if this is my new predecessor
                    elif self.__is_in_interval(start=self.predecessor_id, end=self.id, target=new_predecessor_id):
                        self.predecessor_id = new_predecessor_id
                        self.predecessor_addr = new_predecessor_addr

                    logger.info("Join Request Served")

            # Update Main Chord Node Dictionary Request
            # Main chord Node perspective
            elif request_type == self.__M_CHORD_UPDATE_REQ:
                # inc_data_form[1] is a tuple (join_node.id, join_node.addr) to add into the main Chord Node dictionary
                tuple_to_add = inc_data_form[1]
                if (self.__chord_obj and tuple_to_add) is not None:
                    self.__chord_obj.__setitem__(*tuple_to_add)  # Unpack and serve
                    logger.info("Main Chord Node Update Request Served")

            # Stabilize Dictionary Retrieve Request
            # Main chord Node perspective
            # This request is always served by the main Chord Node only
            elif request_type == self.__STAB_DICT_REQ:
                id_comes_after = inc_data_form[1]
                if (self.__chord_obj and id_comes_after) is not None:
                    # ids_dict only contain the address of the Nodes but not the whole objects
                    ids_dict = Node.get_elements(dct=self.__chord_obj.CHORD_DICT, k=id_comes_after)

                    # Send length of data first for iterative recv
                    b_data = pickle.dumps(ids_dict)
                    length = struct.pack('!I', len(b_data))
                    # Encrypt here
                    inc_conn_obj.sendall(length)
                    inc_conn_obj.sendall(b_data)

                    logger.info("Stabilize Dictionary Request Served")

            # Stabilize Request
            # Successor POV
            elif request_type == self.__STAB_REQ:
                # Send successor list too along with my predecessor details
                data = [(self.predecessor_id, self.predecessor_addr), self.successor_list]
                # Sending my predecessor for stabilize check

                # Send length of data first for iterative recv
                b_data = pickle.dumps(data)
                length = struct.pack('!I', len(b_data))
                # Encrypt here
                inc_conn_obj.sendall(length)
                inc_conn_obj.sendall(b_data)

                logger.info("Stabilize Request Served")

            # Delete Main Chord Node Element Dictionary Request
            # Main chord Node perspective
            elif request_type == self.__M_CHORD_DELETE_REQ:
                # inc_data_form[1] is self.id of the node that is leaving the network. I should use its id to remove its dict entry
                id_to_delete = inc_data_form[1]
                if (self.__chord_obj and id_to_delete) is not None:
                    self.__chord_obj.__delitem__(id_to_delete)
                    logger.info("Main Chord Node Delete Element Request Served")

            elif request_type == self.__CHECK_PRED_REQ:
                # Do nothing. This is just to check if I am alive (connection established) or not.
                logger.info("Check Predecessor Request Served")

            # Notify Request Received
            elif request_type == self.__NOTIFY_REQ:
                pred_check_id, pred_check_addr = inc_data_form[1]

                if self.predecessor_id is None or Node.__is_in_interval(start=self.id, end=self.predecessor_id, target=pred_check_id):
                    self.predecessor_id = pred_check_id
                    self.predecessor_addr = pred_check_addr
                else:
                    pass

            # Send Data Request
            # User need to modify how his data needs to be handled here
            elif request_type == self.__SEND_DATA_REQ:
                pass

            # Leave Request Received
            # 0 -> req_type | 1 -> (succ_id, address of succ)
            # Predecessor Perspective
            elif request_type == self.__LEAVE_REQ:
                succ_id, succ_addr = inc_data_form[1]
                if self.__notify(succ_id, succ_addr):
                    self.successor_id = succ_id
                    self.successor_addr = succ_addr
                    # Ancillary successor list added here
                    self.successor_list.clear()
                    self.successor_list.appendleft((self.successor_id, self.successor_addr))
                else:
                    logger.error("Something went wrong with the notify function.")

            else:
                logger.error("Unidentified Request Type. Closing the Node for security.")
                raise socket.error

        except (socket.error, ValueError, TypeError) as E:
            logger.exception("Request Process Exception", E)

        finally:
            return

    @staticmethod
    def send_requests(request_type: int, r_addr: tuple, timeout: int = 40, **kwargs):
        """Send requests to the clients. Do not modify this function for chord to work properly internally. """
        def handle_request(data_form, offset: int, retries: int = 0):
            # Create socket and set timeout
            send_request_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_request_sock.settimeout(timeout + offset)
            try:
                # Connect, send data, and optionally receive
                send_request_sock.connect(r_addr)

                # Send length of data first for iterative recv
                b_data = pickle.dumps(data_form)
                length = struct.pack('!I', len(b_data))
                # Encrypt here if needed
                send_request_sock.sendall(length)
                send_request_sock.sendall(b_data)

                if request_type in (Node.__LOOKUP_REQ, Node.__STAB_DICT_REQ, Node.__STAB_REQ, Node.__GET_INIT_DETS):
                    # Lookup-Req: Successor details
                    # Stab-Dict-Req: Dictionary with keys as IDs and values as addresses
                    # Stab-Req: Predecessor details and Successor list
                    # Get-Init-Dets-Req: Get initial details like enKey and key space for creating Node object for joining node

                    # First, receive the length of the data (4 bytes)
                    length_data = Node.recv_all(send_request_sock, 4)  # Code Block  # This is in Big Endian C-struct format
                    data_length = struct.unpack('!I', length_data)[0]  # Unpack this length number to use
                    # Then, receive the actual data
                    full_data = Node.recv_all(send_request_sock, data_length)
                    return pickle.loads(full_data)
                return True
            except (socket.timeout, socket.error, ValueError, pickle.PicklingError, TypeError) as E:
                logger.error(f"Request Type {request_type} Exception: {E}")
                print(f"[ERROR] Something went wrong with request type {request_type}.")
                return None
            finally:
                send_request_sock.close()

        # Map request types to data and offsets
        request_map = {
            # The second values in the tuple are offset times
            Node.__GET_INIT_DETS: (None, 0),
            Node.__LOOKUP_REQ: (kwargs.get("l_id"), 10),
            Node.__JOIN_REQ: (kwargs.get("j_req"), 10),
            Node.__M_CHORD_UPDATE_REQ: (kwargs.get("cnu_req"), 0),
            Node.__M_CHORD_DELETE_REQ: (kwargs.get("cnd_req"), 0),
            Node.__NOTIFY_REQ: (kwargs.get("noti_req"), 0),
            Node.__CHECK_PRED_REQ: (None, 1),
            Node.__STAB_DICT_REQ: (kwargs.get("stab_dict_req"), 5),  # Send the id to only grab elements that come after it
            Node.__STAB_REQ: (None, 5),
            Node.__LEAVE_REQ: (kwargs.get("lev_req"), 10)
        }

        data, offset = request_map.get(request_type, (None, 0))

        if data is None and request_type not in (Node.__STAB_REQ, Node.__GET_INIT_DETS, Node.__CHECK_PRED_REQ):
            logger.error("Invalid or missing data for the request.")
            return None

        data_form = [request_type, data]  # data is None here if request type is STAB_REQ, GET_INIT_DETS
        # Handle the request
        return handle_request(data_form, offset)

    @staticmethod
    def __is_in_interval(start, end, target):
        if (start is None) or (end is None) or (target is None):
            return False
        if start >= end:
            return (target < end) or (target > start)
        else:
            return start < target < end

    def __find_successor(self, node_id: int):  # This is bound to the Node class
        # This will check if the joining Node is my (this Node's) successor
        if self.__is_in_interval(start=self.id, end=self.successor_id, target=node_id):
            return self.successor_id, self.successor_addr
        else:
            # Using Parent Chord Object for Fast Lookup
            if self.__chord_obj is not None:  # Main Chord Node that started this network
                sorted_dict_keys = sorted(self.__chord_obj.CHORD_DICT.keys())
                for k in range(len(sorted_dict_keys)):
                    if self.__is_in_interval(start=sorted_dict_keys[k], end=sorted_dict_keys[k + 1], target=node_id):
                        succ_node_id = sorted_dict_keys[k + 1]
                        succ_node_addr = self.__chord_obj.CHORD_DICT[succ_node_id]
                        return succ_node_id, succ_node_addr
            else:  # Other Node that has no access to the main chord obj
                ### IMPLEMENT NON-CENTRAL HUB OPERATION HERE ###
                ip_addr, port = self.m_chord_node_addr
                dets_dict = Node.get_successor(ip_addr=ip_addr, port=port, join_node_id=node_id)  # Sending request to main Chord Node
                successor_id = dets_dict.get("fid")
                successor_addr = dets_dict.get("faddr")
                # Ignoring the m_chord_node_addr because this is secondary connection to the central hub for getting the successor
                return successor_id, successor_addr

    # This method will only make Lookup requests.
    @staticmethod
    def get_successor(port: int, ip_addr: str, join_node_id: int) -> tuple or None:
        # Send Lookup Request
        dets_dict = Node.send_requests(r_addr=(ip_addr, port), request_type=Node.__LOOKUP_REQ, l_id=join_node_id)
        # Return successor values
        logger.info("Get Successor Found")
        return dets_dict

    def __notify(self, notify_id: int, notify_addr: tuple):
        # If only two nodes in the network and one leaves.
        if (notify_id, notify_addr) == (self.id, self.address):
            self.predecessor_id = None
            self.predecessor_addr = None
            return True

        notify_req = Node.send_requests(r_addr=notify_addr, request_type=Node.__NOTIFY_REQ, noti_req=(self.id, self.address))
        if notify_req:
            return True
        else:
            logger.error("Something went wrong in notifying my potential successor that I am its predecessor.")
            return False

    # Run every few seconds # Thread
    def __stabilize(self):
        while True:
            time.sleep(round(random.uniform(6, 11)))

            try:
                # Don't run stabilize if only one node
                if self.id == self.successor_id and self.predecessor_id is None:
                    continue

                if self.isCentralHub:  # Central hub
                    # Ask main chord Node to send its dictionary of elements with ids that comes after my self.id
                    nodes_dict = Node.send_requests(r_addr=self.m_chord_node_addr, request_type=Node.__STAB_DICT_REQ, stab_dict_req=self.id)
                    for key, value in nodes_dict.items():
                        # This returns my successor's predecessor to check if I am indeed its predecessor.
                        s_id = key
                        s_value_addr = value

                        # Send request
                        succ_vals = Node.send_requests(r_addr=s_value_addr, request_type=Node.__STAB_REQ)  # Successor predecessor dets and successor list

                        if not succ_vals:  # If my successor is not responding
                            # Send to main chord Node about removing this unresponsive Node from its dict
                            Node.send_requests(r_addr=self.m_chord_node_addr, request_type=Node.__M_CHORD_DELETE_REQ, cnd_req=s_id)  # To remove s_id
                            continue  # Not break from for-loop

                        succ_pred, succ_list = succ_vals
                        succ_pred_id, succ_pred_addr = succ_pred

                        if succ_pred_id == self.id:  # I am my successor's predecessor. All is going well.
                            logger.success("Stabilize Request Successful. Nothing's changed.")
                            break

                        if succ_pred_id is not None and Node.__is_in_interval(start=self.id, end=s_id, target=succ_pred_id):
                            if self.__notify(succ_pred_id, succ_pred_addr):
                                self.successor_id = succ_pred_id
                                self.successor_addr = succ_pred_addr
                                # Successor List Operations
                                self.successor_list.clear()
                                self.successor_list.appendleft((self.successor_id, self.successor_addr))
                                # Break from the for-loop and continue stabilize
                                break
                            else:
                                logger.warning("[STAB-NOTIFY ERR-1] Something went wrong in stabilizing my potential successor "
                                             "that came between me and my actual successor")
                                break  # Can't do anything; just continue stabilize new

                        else:
                            if self.__notify(s_id, s_value_addr):
                                self.successor_id = s_id
                                self.successor_addr = s_value_addr
                                # Successor List Operations
                                self.successor_list.clear()
                                self.successor_list.appendleft((self.successor_id, self.successor_addr))
                                # Break from the for-loop and continue stabilize
                                break
                            else:
                                logger.warning("[STAB-NOTIFY ERR-2] Something went wrong in stabilizing my successor")
                                break  # Can't do anything; just continue stabilize new

                else:  # Not a central hub, but standard chord protocol
                    # Use fingertable instead
                    pass

            except (TypeError, ValueError) as E:
                logger.error(f"Something went wrong in stabilizing: {E}")

    # Run every few seconds # Thread
    def __fix_fingers(self):
        if not self.isCentralHub:  # Not a central hub, but standard chord protocol
            next_itr = 0
            while True:
                time.sleep(round(random.uniform(7, 13)))

                if self.id == self.successor_id:
                    continue

                if next_itr >= self.node_M:  #NTC
                    next_itr = 0

                #equ_id = next(iter(self.finger_table))
                equ_id = list(self.finger_table.keys())[next_itr]

                try:
                    actual_id, actual_addr = self.__find_successor(equ_id)
                    self.finger_table[equ_id] = (actual_id, actual_addr)
                except TypeError as TE:
                    # Do nothing;
                    logger.exception("Fix Fingers TypeError Exception: ", TE)

                next_itr = next_itr + 1

    # Run every few seconds # Thread
    def __check_predecessor(self, timer: int = 7):
        assert (8 > timer > 1), "Timer must be less than 8 seconds for Chord to function properly."
        while True:
            time.sleep((round(random.uniform(timer, 8))))

            if self.predecessor_id is None or self.predecessor_addr is None:
                # No need to check if I am the only node in the network or if I don't have any predecessor
                continue

            response = Node.send_requests(r_addr=self.predecessor_addr, request_type=Node.__CHECK_PRED_REQ)

            if not response:
                self.predecessor_id = None
                self.predecessor_addr = None

    @staticmethod
    def send_data(self, dform: str = 'message'):
        """Use this function to send any data to any of the nodes inside the chord network.
        This library expects you to Monkey-Patch this function and modify it according to your requirements for sending data.
        :param dform: str
        """
        # Can send any amount of data for the user
        # Need to write a loop for handling chunks of large data
        req_type = Node.__SEND_DATA_REQ
        pass

    def leave(self):
        """Leave the chord network."""
        if self.predecessor_addr is not None and self.predecessor_id is not None:
            # Leave request doesn't need to return anything and just insist on closing without housekeeping
            Node.send_requests(r_addr=self.predecessor_addr, request_type=Node.__LEAVE_REQ, lev_req=(self.successor_id, self.successor_addr))
            # self.node_sock.shutdown(socket.SHUT_RDWR)
            # Send to main chord Node about removing this Node from its dict
            Node.send_requests(r_addr=self.m_chord_node_addr, request_type=Node.__M_CHORD_DELETE_REQ, cnd_req=self.id)

        else:  # Only one Node in the network.  Nothing to do.
            pass

        self.__LEAVE = True
        self.node_sock.close()  # This will trigger an exception on the listening for connections thread
        if self.node_sock.fileno() == -1:  # Check if the socket is closed
            sys.exit(0)
        # Just exit
        sys.exit(-1)

    @staticmethod
    def create_node(address: tuple, key_space: int) -> 'Node':
        """Creates a Node object."""
        # Create Node Object
        ip_addr, port = address
        node = Node(port, ip_addr, key_space=key_space)  # Send 'self' object instance of this class to Node class
        return node
