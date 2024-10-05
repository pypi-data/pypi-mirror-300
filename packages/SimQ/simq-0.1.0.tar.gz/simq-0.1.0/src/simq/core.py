import simpy


class GGCQueue:
    def __init__(
        self,
        env,
        name,
        num_servers,
        service_time_dist,
        inter_arrival_dist,
        routing_strategy=None,
    ):
        self.env = env
        self.name = name
        self.server = simpy.Resource(env, capacity=num_servers)
        self.service_time_dist = service_time_dist
        self.inter_arrival_dist = inter_arrival_dist
        self.routing_strategy = routing_strategy

    def customer(self, customer_id, queue_system):
        arrival_time = self.env.now
        queue_system.event_log.append(
            {
                "customer": customer_id,
                "action": "arrival",
                "queue": self.name,
                "time": arrival_time,
            }
        )

        # Request a server
        with self.server.request() as request:
            yield request

            wait_time = self.env.now - arrival_time
            queue_system.event_log.append(
                {
                    "customer": customer_id,
                    "action": "service_start",
                    "queue": self.name,
                    "time": self.env.now,
                }
            )

            # Service time is sampled from the distribution
            service_time = self.service_time_dist.sample(self)
            yield self.env.timeout(service_time)

            queue_system.event_log.append(
                {
                    "customer": customer_id,
                    "action": "service_finish",
                    "queue": self.name,
                    "time": self.env.now,
                }
            )

            # Decide the next action based on routing strategy
            if self.routing_strategy:
                yield self.env.process(
                    self.routing_strategy(customer_id, self, queue_system)
                )
            else:
                queue_system.event_log.append(
                    {
                        "customer": customer_id,
                        "action": "leave_system",
                        "queue": self.name,
                        "time": self.env.now,
                    }
                )

    def generate_customers(self, queue_system):
        """Generate customers for this queue based on its inter-arrival time distribution."""

        while True:
            inter_arrival_time = self.inter_arrival_dist.sample(self)
            yield self.env.timeout(inter_arrival_time)

            # Get a new unique customer_id from the queue system
            customer_id = queue_system.get_next_customer_id()
            self.env.process(self.customer(customer_id, queue_system))


class QueueSystem:
    """Queue system manages multiple queues and tracks customer IDs"""

    def __init__(self, env, queues):
        self.env = env
        self.queues = queues
        self.customer_id_counter = 0
        self.event_log = []

    def start_customer_generation(self):
        """Start customer generation for each queue"""
        for queue in self.queues:
            self.env.process(queue.generate_customers(self))

    def get_next_customer_id(self):
        """Increment the customer ID counter and return the next unique ID"""
        self.customer_id_counter += 1
        return self.customer_id_counter
