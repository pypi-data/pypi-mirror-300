import socket
import sys
import hashlib
from collections import deque, OrderedDict
import threading
import pickle
from loguru import logger
import uuid
from contextlib import contextmanager
from cryptography.fernet import Fernet

# Self Imports
from libChord import node


# Global Variables
# BUFFER = 4096
GLOBAL_LOOPBACK_IP = "127.0.0.1"


def get_hash(key, key_space) -> int:
    """Generates a hash value with the specified key space."""
    val = hashlib.sha1(key.encode())
    return int(val.hexdigest(), 16) % key_space


def get_uid() -> str:
    """Generates a unique random UUID. (Testing)"""
    unique_code = str(uuid.uuid1())
    return unique_code


def join(port: int, ip_addr: str, testing: bool = False) -> 'node.Node':  # The ip_addr and port is for the connection to be made
    """To make a node join the already instantiated chord network."""

    # [INFO] This entire join network function does four connections to the Nodes.
    # 1. For getting initial details such as enKey and key space for Node object creation # Not Encrypted
    # All subsequent connections are Encrypted after this point #
    # 2. Get all the subsequent details from the same consulting Node with Encryption
    # 3. Contact my successor to say that I am its predecessor
    # 4. Make a connection to the main Chord Node to update its Node dictionary

    # Type Error Enforcing
    assert isinstance(port, int), f"Expected port to be int, got {type(port).__name__}"
    assert isinstance(ip_addr, str), f"Expected ip_addr to be str, got {type(ip_addr).__name__}"

    # Request Types #Private
    __GET_INIT_DETS = 100
    # _LOOKUP_REQ = 111
    _JOIN_REQ = 222
    _M_CHORD_UPDATE_REQ = 233
    # _LEAVE_REQ = 999

    # Create a Node object for the joining machine
    my_ip_addr, my_port = node.get_ip_port(testing=testing)

    # Part-1. A request to ask the provided Node for its Key Space and enKey before joining the network
    # Initial Details Request
    try:
        init_dets = node.Node.send_requests(r_addr=(ip_addr, port), request_type=__GET_INIT_DETS)
        enKey = init_dets.get("enKey")
        node_keySpace = init_dets.get("node_keySpace")
    except socket.error as E:
        # Error. NTD. Exit.
        logger.error(f"Error: {E}")
        raise ValueError("The Node with the specified IP Address and Port might not be responding. Try again.")

    join_node = node.Node.create_node(address=(my_ip_addr, my_port), key_space=node_keySpace)

    # Part-2. Get Successor for Joining Node
    # Lookup Request
    try:  # Get one packaged dictionary instead of so many loose variables
        dets_dict = node.Node.get_successor(port=port, ip_addr=ip_addr, join_node_id=join_node.id)  # Send only the id, not the node obj
        successor_id = dets_dict.get("fid")
        successor_addr = dets_dict.get("faddr")
        m_chord_node_addr = dets_dict.get("m_chord_addr")
        m_chord_M = dets_dict.get("node_M")
        m_chord_hub = dets_dict.get("centralHub")
    except ValueError as E:
        # Error. NTD. Exit.
        del join_node  # Delete Node object
        logger.error(f"Error: {E}")
        raise ValueError("Something went wrong in communicating with nodes. Try again.")

    if successor_addr is None:
        # Error. NTD. Exit.
        del join_node  # Delete Node object
        raise ValueError("Something went wrong in communicating with nodes. Try again.")

    # Part-3. After receiving the Node's successor, we should contact it to say I am its predecessor
    # Join Request
    # successor_addr is a (tuple)
    success = node.Node.send_requests(r_addr=successor_addr, request_type=_JOIN_REQ, j_req=(join_node.id, join_node.address))

    if success:
        join_node.successor_id = successor_id
        join_node.successor_addr = successor_addr
        join_node.successor_list.append((successor_id, successor_addr))
        join_node.m_chord_node_addr = m_chord_node_addr
        join_node.node_M = m_chord_M
        join_node.isCentralHub = m_chord_hub
        join_node._enKey = enKey
        join_node.node_keySpace = node_keySpace
    else:
        # Error. NTD. Exit.
        del join_node  # Delete Node object
        raise ValueError("Something went wrong in communicating with nodes. Try again.")

    # This is part-4 of joining. Send request to main Chord Node for adding this Node in its dict.
    cnu_req = (join_node.id, join_node.address)  # Send Node object
    cnu_update_success = node.Node.send_requests(request_type=_M_CHORD_UPDATE_REQ, r_addr=m_chord_node_addr, cnu_req=cnu_req)

    if cnu_update_success:
        logger.success("Main Chord Node updated successfully.")
    else:
        # Error. CTA. Could retry.
        logger.exception("Something went wrong with main Chord Node update.")
        raise SystemExit("Main Central Hub that initiated this network might've left.")

    # Node successfully joined the network; Need to start listening for connections.
    join_node.start_listen()
    return join_node


# MAIN CHORD (CHILD CLASS) # This serves as a database to the Node class.
class Chord:
    """For initializing a chord network. Creates a chord network object.
    Chord is a singleton class, meaning there can only be one Chord instance per machine."""

    # Singleton Instance #Private
    __instance = None

    # Loopback IP #Non-private
    LOOPBACK_IP = "127.0.0.1"

    # Singleton Instance Limit
    def __new__(cls, network_name: str, port: int = None, ip_addr: str = None, M: int = 9, central_hub: bool = True, testing: bool = False):
        if cls.__instance is None:
            cls.__instance = super(Chord, cls).__new__(cls)
        return cls.__instance

    def __init__(self, network_name: str, port: int = None, ip_addr: str = None, M: int = 9, central_hub: bool = True, testing: bool = False):
        # Type Error Enforcing
        assert isinstance(port, (int, type(None))), f"Expected port to be int or None, got {type(port).__name__}"
        assert isinstance(ip_addr, (str, type(None))), f"Expected ip_addr to be str or None, got {type(ip_addr).__name__}"
        assert isinstance(network_name, str), f"Expected network_name to be str, got {type(network_name).__name__}"
        assert isinstance(M, int), f"Expected M to be int, got {type(M).__name__}"
        assert isinstance(central_hub, bool), f"Expected central_hub to be boolean, got {type(central_hub).__name__}"

        if ip_addr is None or port is None:
            ip_addr, port = node.get_ip_port(testing=testing)

        # Central Hub
        self.__central_hub = central_hub

        # Class vars
        self.__NETWORK_NAME = network_name
        self.__KEY_SPACE = pow(2, M)
        self.__M = M

        # Central Hub Dictionary
        self.__CHORD_DICT = {}

        self.timeout = 300  # Manual timeout

        # Encryption
        self.__enKey = Chord.__generate_key()

        # Create Node Object
        self.node = node.Node(chord_obj=self, port=port, ip_addr=ip_addr)  # Send 'self' object instance of this class to Node class

        self.__IP_ADDRESS = self.node.ip_addr
        self.__PORT = self.node.port
        self.__ID = self.node.id
        self.__ADDRESS = (self.__IP_ADDRESS, self.__PORT)

        if (self.__PORT != 0) and (self.__ID is not None):
            # Add Node to Chord dict
            self.__setitem__(self.__ID, self.node.address)

    @staticmethod
    def __generate_key():
        """Generate a cryptographic Fernet key for secure socket transmissions. (Testing)"""
        key = Fernet.generate_key()
        return key

    @staticmethod
    def __encrypt(key, data):
        """Encrypt data using Fernet. (Testing)"""
        # For Fernet encryption
        cipher = Fernet(key)
        # Serialize the data with pickle
        serialized_data = pickle.dumps(data)
        # Encrypt the serialized data
        encrypted_data = cipher.encrypt(serialized_data)
        return encrypted_data

    @property
    def IP_ADDRESS(self):
        """You can only access the IP address but can't modify it."""
        return self.__IP_ADDRESS

    @property
    def PORT(self):
        """You can only access the Port but can't modify it."""
        return self.__PORT

    @property
    def ID(self):
        """You can only access the ID but can't modify it."""
        return self.__ID

    @property
    def ADDRESS(self):
        """You can only access the Address but can't modify it."""
        return self.__ADDRESS

    @property
    def NETWORK_NAME(self):
        """Getter: This will get the network name."""
        return self.__NETWORK_NAME

    @NETWORK_NAME.setter
    def NETWORK_NAME(self, value):
        """Setter: This will set the network name."""
        self.__NETWORK_NAME = value

    @property
    def central_hub(self):
        """Getter: This will return the central hub type."""
        return self.__central_hub

    @property
    def _M(self):
        # I don't want user to access this
        return self.__M

    @property
    def CHORD_DICT(self):
        """Returns the chord dictionary of Nodes that are currently in the network."""
        # User can access this
        return self.__CHORD_DICT

    @property
    def KEY_SPACE(self):
        return self.__KEY_SPACE

    @property
    def _enKey(self):
        # I don't want user to access this
        return self.__enKey

    def __setitem__(self, key, value):
        """Set a node ID as key and its Node class object instance as its value."""
        self.__CHORD_DICT[key] = value

    def __delitem__(self, key):
        """Delete an element from dict with node ID as key."""
        del self.__CHORD_DICT[key]

    def listen(self, timeout: int = 300) -> None:
        """Start accepting incoming connections to add to your newly created chord network."""
        assert isinstance(timeout, int), f"Expected timeout to be int, got {type(timeout).__name__}"
        if timeout <= 10:
            raise ValueError("Timeout must be greater than or equal to 10")
        self.timeout = timeout
        # Initiate node listening thread function for incoming connections
        self.node.start_listen(timeout)
