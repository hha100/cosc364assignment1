class RIPEntry:
    """ A class to create RIP routing table entries with an inbuilt list to hold its values"""

    def __init__(self, destination, costs, next_hop):
        """ Initialise the RIP routing table entry values"""
        
        self.destination = destination
        self.costs = costs
        self.next_hop = next_hop
        self.flag = 0
        self.came_from = None

    def __str__(self):
        """ String method prints the values of the routing table entry when called"""
        
        return 'RIP Entry:\n  Destination: {0}\n  Cost: {1}\n  Next Hop: {2}\n  Route Change Flag: {3}\n  Came From Router: {4}'.format(self.destination, self.costs, self.next_hop, self.flag, self.came_from)

    def get_info(self):
        """ Returns the values of the routing table entry"""
        
        return self.destination, self.costs, self.next_hop, self.flag, self.came_from



class RoutingTable:
    """ A class to create a routers RIP routing table with a list to hold instances of the RIPEntry class"""

    def __init__(self, config_file):
        """ Initialise the routing tables entry list and a variable for the name of the config file used"""
        
        self.config_file = config_file
        self.entries = []

    def add_to_table(self, entry):
        """ Appends a RIPEntry to the routing table list"""
        
        self.entries.append(entry)

    def get_table(self):
        """ Returns the routing table list of RIPEntry instances"""
        
        return self.entries

    def update_entry(self, current_entry, replacement_entry):
        """ Updates a routing table entry with new values"""
        
        destination, costs, next_hop, flag, came_from = replacement_entry.get_info()
        self.entries[current_entry].costs = costs
        self.entries[current_entry].came_from = came_from
        self.entries[current_entry].next_hop = next_hop
        self.entries[current_entry].flag = flag

    def remove_entry(self, destination):
        """ Removes a routing entry from the table"""
        
        # Iterate through the entries list
        for index in range(len(self.entries)):
            
            # Find the entry with the destination matching the one given
            if self.entries[index].destination == destination:
                
                # Remove this entry from the routing table and exit the for loop
                self.entries.pop(index)
                break


# Now we want to create the initial Routing Table, using the output ports from the config file
def init_table(config_filename, output_ports):
    """ Initialises the routing table using neighbouring routers from the output ports list"""
    
    # Create an instance of the RoutingTable class using the name of the config file given
    rip_table = RoutingTable(config_filename)
    
    # Iterate through the output ports
    for index in range(len(output_ports)):
        
        # Create a RIPEntry instance for each neighbouring router and add it to the routing table
        port = output_ports[index]
        entry = RIPEntry(port[2], port[1], port[2])
        rip_table.add_to_table(entry)
    
    # Return the routing table
    return rip_table
