# Chord Protocol

The Chord protocol is a peer-to-peer (P2P) distributed 
hash table (DHT) protocol designed to manage the placement 
and retrieval of data across a decentralized network of nodes
efficiently. It offers a scalable, fault-tolerant, and 
efficient solution for data storage and lookup in distributed
systems, ensuring that even as nodes join or leave the network,
data can still be found and managed correctly.

### Consistent Hashing
Chord uses consistent hashing to assign keys to nodes, which means data and nodes are arranged in a logical ring. Each node and data item is assigned an m-bit identifier, typically derived from hashing their IP address or other identifiers. This identifier determines the node's position in the circular ID space ranging from 0 to \(2^m - 1\). Each key (data item) is stored on the first node whose ID is equal to or follows the key's ID in this circular space.

### Scalability
The protocol ensures that with N nodes in the system, any key lookup operation requires \(O(\log N)\) hops on average, making it highly efficient for large networks. As nodes are added or removed, Chord's structure adjusts dynamically, redistributing keys among nodes with minimal disruption.

### Finger Tables
To achieve efficient lookups, each node maintains a "finger table," which is an array containing information about other nodes in the network. Each entry in this table points to a node that is a specific distance (power of 2) away from the current node. This finger table enables a node to quickly route a query closer to the target key's location, significantly reducing the number of hops required for lookup.

### Key Lookup
When a node wants to find a key, it does not search linearly through the ring. Instead, it uses the information in its finger table to leap closer to the target node, effectively halving the remaining distance to the target in each step. This logarithmic lookup process is what gives Chord its efficiency.

## Operations in Chord

### Join
When a new node joins the network, it must integrate itself into the existing ring structure. It identifies its successor (the node immediately following it on the ring) and informs other nodes to update their finger tables to reflect its presence. The new node also takes over responsibility for some of the keys previously managed by its successor.

### Stabilization
Since nodes can join or leave at any time, Chord has a stabilization protocol that continuously updates finger tables and successor pointers to ensure the ring's integrity. Periodically, nodes verify their successor and predecessor information, correcting any inconsistencies due to network changes.

### Data Transfer
When a node joins or leaves, the responsibility for certain keys must be transferred between nodes to maintain data consistency. Chord handles this transfer efficiently, ensuring minimal disruption to the network.

### Lookup and Routing
When a node receives a query for a specific key, it checks if it is responsible for that key. If not, it uses its finger table to forward the query to the node that is closer to the target key, continuing this process until the correct node is found.

### Failure Handling
Nodes may leave the network unexpectedly. Chord ensures resilience by maintaining multiple successors (successor lists) for each node, which helps in quickly recovering from node failures. If a node fails, other nodes can use their successor lists to route around the failed node and update their structures accordingly.

## Use Cases
The Chord protocol is used in various distributed systems, such as:

- Distributed file systems where data is spread across multiple machines
- Peer-to-peer networks for efficient data retrieval and sharing
- Content distribution networks (CDNs) that need decentralized data access
- Decentralized applications (DApps) that require a resilient and scalable storage mechanism

## References
[Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf)
