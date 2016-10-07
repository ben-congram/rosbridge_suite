import fnmatch
from rosbridge_library.capability import Capability


class UnadvertiseService(Capability):

    #unadvertise_service_msg_fields = [(True, "service", (str, unicode))]

    services_glob = None

    def __init__(self, protocol):
        # Call superclass constructor
        Capability.__init__(self, protocol)

        # Register the operations that this capability provides
        protocol.register_operation("unadvertise_service", self.unadvertise_service)

    def unadvertise_service(self, message):
        # parse the message
        service_name = message["service"]

        if self.services_glob is not None:
            self.protocol.log("info", "Unadvertise service glob match? "+topic)
            match = False
            for glob in self.services_glob:
                if (fnmatch.fnmatch(service_name, glob)):
                    self.protocol.log("info", "Yes, with glob: "+glob)
                    match = True
                    break
            if match:
                self.protocol.log("info", "Continuing service unadvertisement...")
            else:
                self.protocol.log("info", "Cancelling service unadvertisement...")
                return
        else:
            self.protocol.log("info", "No service security glob, not checking service unadvertisement...")

        # unregister service in ROS
        if service_name in self.protocol.external_service_list.keys():
            self.protocol.external_service_list[service_name].service_handle.shutdown("Unadvertise request.")
            del self.protocol.external_service_list[service_name]
            self.protocol.log("info", "Unadvertised service %s." % service_name)
        else:
            self.protocol.log("error", "Service %s has no been advertised externally." % service_name)
