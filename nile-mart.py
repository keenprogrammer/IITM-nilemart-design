DELIVERY_MAP_CONFIG = '../config/delivery_map.txt'
ORDER_BATCH_CONFIG = '../config/order_batch.txt'

NORMAL_DELIVERY = 'Normal'
PREMIUM_DELIVERY = 'PREMIUM'
TO_SIGN = "->"


class Order:
    def __init__(self, id, item_name, customer, order_date, city, delivery_date, delivery_type):
        self._id = id
        self._item_name = item_name
        self._customer = customer
        self._order_date = order_date
        self._city = city
        self._delivery_date = delivery_date
        self._delivery_type = delivery_type

    def __str__(self):
        return f'ID - {self.id}, Item Name - {self.item_name}, Order Date - {self.order_date}, Customer - {self.customer}, City - {self.city}, Delivery Date - {self.delivery_date}, Delivery Type - {self.delivery_type}'

    @property
    def id(self):
        return self._id

    @property
    def item_name(self):
        return self._item_name

    @property
    def order_date(self):
        return self._order_date

    @property
    def customer(self):
        return self._customer

    @property
    def city(self):
        return self._city

    @property
    def delivery_date(self):
        return self._delivery_date

    @property
    def delivery_type(self):
        return self._delivery_type

    def dispatch(self, delivery_route):
        print(f'Dispatching order {order}')
        delivery_route.process_order(self)


class OrderBatch:
    def __init__(self):
        self._order_batch = []

    def __str__(self):
        pass

    def read_config(self, order_batch_config):
        with open(order_batch_config, 'r') as obatch_file:
            obatch_lines = [obatch_line.rstrip() for obatch_line in obatch_file]

        for order_entry in obatch_lines:
            order_details = order_entry.split('-')
            order = Order(order_details[0], order_details[1], order_details[2], order_details[3], order_details[4],
                          order_details[5], order_details[6])

            self._order_batch.append(order)

    def get_orders(self):
        return self._order_batch


class DeliveryMap:
    def __init__(self):
        self._destinations = []
        self._delivery_map = {}

    def __str__(self):
        pass

    def read_config(self, delivery_map_config):
        with open(delivery_map_config, 'r') as dmap_file:
            dmap_lines = [dmap_line.rstrip() for dmap_line in dmap_file]

        for line in dmap_lines:
            destination, deliveryType, stages = line.split(' ')
            destTuple = (destination, deliveryType)
            self._destinations.append(destTuple)
            stages = stages.split(',')
            self._delivery_map[destTuple[0] + TO_SIGN + destTuple[1]] = stages
        print(f'(Destinations : DeliveryType) {self._destinations}')

    def get_destinations(self):
        return self._destinations

    def routing_map(self):
        return self._delivery_map

    def get_stages(self, delivery_center):
        return self._delivery_map[delivery_center]


class DeliveryStage:
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination
        self._next_stage = None

    @property
    def next_stage(self):
        return self._next_stage

    @next_stage.setter
    def next_stage(self, successor):
        self._next_stage = successor

    def process_order(self, order):
        pass


class TrainDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Train from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Train Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


class FlightDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Flight from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Flight Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


class TruckDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Truck from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Truck Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


'''Added new DeliveryMethod as Boat'''


class BoatDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Boat from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Boat Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


'''Added new DeliveryMethod as ship'''


class ShipDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Ship from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Ship Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


'''Factory class to create delivery method
1. scalability -  there is addition in deliveryMethod changes won't impact DeliverySystem
2. maintainability - single place to make changes in case of logic failure
'''


class DeliveryStageFactory:
    def __init__(self):
        pass

    @staticmethod
    def createDeliveryMethod(deliveryMethod, source, destination):
        if deliveryMethod == 'truck':
            return TruckDispatch(source, destination)
        elif deliveryMethod == 'train':
            return TrainDispatch(source, destination)
        elif deliveryMethod == 'flight':
            return FlightDispatch(source, destination)
        elif deliveryMethod == 'boat':
            return BoatDispatch(source, destination)
        elif deliveryMethod == 'ship':
            return ShipDispatch(source, destination)


class DeliveryRoute:
    def __init__(self, stage_list, destination):
        self._stage_list = stage_list
        self._destination = destination

    def __str__(self):
        route = ','.join(str(stage) for stage in self._stage_list)
        return f'Route to {self._destination} : {route}\n'

    def process_order(self, order):
        self._stage_list[0].process_order(order)


class DeliverySystem:
    def __init__(self):
        self.delivery_centers = []
        self.stage_routes = {}

    def populate_route(self, center, stages):
        stage_list = []

        deliverySystemFactory = DeliveryStageFactory()
        for stage in stages:
            source, deliveryMethod, destination = stage.split('-')
            stage_list.append(deliverySystemFactory.createDeliveryMethod(deliveryMethod, source, destination))

        for i in range(0, len(stage_list) - 1):
            stage_list[i].next_stage = stage_list[i + 1]

        route = DeliveryRoute(stage_list, center)
        print(route)

        return route

    def configure(self, deliveryMapInputs):
        delivery_map = DeliveryMap()
        delivery_map.read_config(deliveryMapInputs)

        self.delivery_centers.extend(delivery_map.get_destinations())

        for center in self.delivery_centers:
            stages = delivery_map.get_stages(center[0] + TO_SIGN + center[1])
            route = self.populate_route(center, stages)
            self.stage_routes[center[0] + TO_SIGN + center[1]] = route

    def get_route(self, destination):
        return self.stage_routes[destination]


'''class to create object of DeliverySystem 
1. Client dont have to worry about input of file
2. DeliverySystem can not be updated once created client is responsible to call refreshDeliverySystem(self, mapConfig)
in case of update to refresh the deliverySystem
'''


class DeliverySystemFactory:
    def __init__(self, deliveryMapInputs):
        self.deliverySystem = DeliverySystem()
        self.deliverySystem.configure(deliveryMapInputs)

    ''' return already created object it wont create one'''

    def getDeliverySystem(self):
        if self.deliverySystem is None:
            return None
        else:
            return self.deliverySystem

    '''method to re-create delivery system if there is any update'''

    def refreshDeliverySystem(self, deliveryMapInputs):
        self.deliverySystem = DeliverySystem()
        self.deliverySystem.configure(deliveryMapInputs)
        return self.deliverySystem


# Client Context
deliverySystemFactory = DeliverySystemFactory(DELIVERY_MAP_CONFIG)

order_batch = OrderBatch()
order_batch.read_config(ORDER_BATCH_CONFIG)

orders = order_batch.get_orders()

for order in orders:
    route = deliverySystemFactory.getDeliverySystem().get_route(order.city + TO_SIGN + order.delivery_type)
    order.dispatch(route)
    print('\n')
