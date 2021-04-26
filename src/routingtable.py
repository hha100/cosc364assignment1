class RIPEntry:
    """
    From the RIPv2 spec,
    Each entry in the routing table should have at least the following info:
    -IPv4 address of destination
    -Metric representing total cost of getting a datagram from that router to the destination (sum of costs associated with the networks traversed to get to destination)
    -IPv4 address of next router along path to destination (AKA "next hop"). Not needed if destination is on one of the directly connected networks
    -Flag to indicate that info about the route has changed recently. (AKA "route change flag")
    -Various timers associated with route (?)
    -Subnet mask if all extensions are implemented. We are not implementing any extensions, therefore subnet mask is not needed
    -WIP: We need garbage collection
    """

    # Initialise variables
    def __init__(self, destination, costs, next_hop):
        self.destination = destination
        self.costs = costs
        self.next_hop = next_hop
        self.flag = 0
        self.came_from = None

    # Dunder method, setting the string to be printed when an instance of the object is called
    def __str__(self):
        return 'RIP Entry: \n    Destination: {0} \n    Cost: {1} \n    Next Hop: {2} \n    Route Change Flag: {3} \n Came From Router: {4}'.format(
            self.destination, self.costs, self.next_hop, self.flag, self.came_from)

    def get_info(self):
        return self.destination, self.costs, self.next_hop, self.flag, self.came_from

    def get_destination(self):
        return self.destination()

    def get_costs(self):
        return self.costs

    def get_came_from(self):
        return self.came_from


class RoutingTable:
    """
    Routing Table displays all the RIP Entries
    """

    def __init__(self, config_file):
        self.config_file = config_file
        self.entries = []

    def add_to_table(self, entry):
        self.entries.append(entry)

    def get_table(self):
        return self.entries

    def update_entry(self, current_entry, replacement_entry):
        # ToDo: Add checks to make sure the data is valid. Maybe separate it out into a single validator function?
        destination, costs, next_hop, flag, came_from = replacement_entry.get_info()
        self.entries[current_entry].costs = costs
        self.entries[current_entry].came_from = came_from
        self.entries[current_entry].next_hop = next_hop
        self.entries[current_entry].flag = flag
        print("Entry updated. Entry was: {0} \n Entry is now {1}".format(current_entry, self.entries[current_entry]))

    def remove_entry(self, destination):
        for entry in self.entries:
            if entry.destination == destination:
                self.entries.remove(entry)
                print("Removed entry {}".format(entry))
                break


# Now we want to create the initial Routing Table, using the output ports from the config file

def init_table(config_filename, output_ports):
    rip_table = RoutingTable(config_filename)
    for index in range(len(output_ports)):
        port = output_ports[index]
        entry = RIPEntry(port[2], port[1], port[2])
        rip_table.add_to_table(entry)
    return rip_table