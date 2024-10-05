# fct-kiwi

## Brief

The fct-kiwi package offers a object oriented API to the balena API, it helps the developer to effortless optimize API request load and the program's memory by managing a program-global data structure which manages each resource requested to the Balena Cloud.

## Basics

### Authentication

Before starting using the libraries, you will need to authenticate into your balena account using an API key:

#### Option 1 environment variable

Add your API key to the env named `BALENA_API_KEY`

#### Option 2 using the authenticate class method

```python3
from fct_kiwi import Balena

Balena.authenticate(balena_api_key)
```

you can always check if your API key is loaded using the `Balena.id_authenticated()` method

```python3
if not Balena.is_authenticated():
    print("Your Balena API key is not loaded yet", file=stderr)
```

### Resources

[Balena resources](https://docs.balena.io/reference/api/resources/device/) are mapped into classes, which are children of the `Resource` base class; we will use their respective methods to manage the resources.

This approach is much simpler and powerful than using the web API directly, for instance, let's say you want to list the devices belonging to a fleet's id.
By using the web API, you would have to handle the following request:

```bash
curl -X GET \
"https://api.balena-cloud.com/v6/device?\$filter=belongs_to__application%20eq%20'<FLEET ID>'" \
-H  "Content-Type: application/json"  \
-H "Authorization: Bearer <AUTH_TOKEN>"
```

After proper configuration, this would be the equivalent using the package:
```python3
devices = Device.fromFleet(fleet_id=000)
```

in this example, `Device` is a class with inherited properties from `Resource`.

Resource classes are ORM like objects, that's because balena resources are tables of arelational database, thus, when we fetch a resource by using class methods like `Device.fromFleet` or updating existing ones with methods like `devices.update()`, the data returned from the web API is updated into a data structure in the class scope, which you can check by using `Resource.get_registry()`.

```python3
from fct_kiwi import Device

print(Device.get_registry()) # Check the registry before fetching a new resource

device = Device(8026455)     # Get a device using it's id

print(Device.get_registry()) # The device is not resistered if the object is created using it's consturctor

Device.register(device)      # Register the device manually
print(Device.get_registry()) # The device is not resistered if the object is created using it's consturctor and it's id (which is rare to know beforehand)

device.update()              # fetch the device resource on balena cloud
device2 = Device.fromDeviceName(device['device_name']) # Trying to fetch the same device
                            # fromDeviceName runs Device.register internallt

print(Device.get_registry()) # The registry still has only one device
                             # The device name is prefered when printing a resource group instead of the device id if available 
                             # Now device and device2 are references to the same Device type object
```

if you run the code above, expect a response like the following:

```bash
None
None
<ResourceGroup[Device]>: [0000000] 
<ResourceGroup[Device]>: [kiwibot4U063]
```

### Resource not found

Sometimes we will request a resource that doesn't exist in balena Cloud, in this cases, any try to fetch this resource will raise an `ResourceNotFound` exception, which you can import from the package.

```python3
from fct_kiwi import ResourceNotFound
```

You can create personalized resource groups in the following manner:

Example: ResourceGroup that contains all fleet service variables for a given service id
```python3
from fct_kiwi import FleetServiceEnv, ResourceGroup

serv_envs = ResourceGroup(FleetServiceEnv)
serv_envs.filter=f"service eq {1....0}"
serv_envs.update()

print(serv_envs)
```

### Accessing resource information

Each resource object is a row of a table on a database; it works like a dictionary on python, so you can access the resource fields just like if it was a dictionary:

```python3
print(device['device_name'])
print(device.keys())
print(device.values())
```
These methods are a shortcut to access to the real dictionary saved in the object, if you need to access it directly, it is saved in:
```python3
device.data: dict
```
Every Resource has diferent fields, when working with them, have in hand the [official resources documentation](https://docs.balena.io/reference/api/resources/device/)

### Foreign resources

Each resource comes with one or more foreign keys refering to other resources, this means a sole call to `device.update()` will also fetch other resources related to the device:

For example, the `device` resource contains fields called `belongs_to__application` and  `is_running__release` which are foreign keys to other resources, when fetching the device default table, their information will also be updated in their respective data structure:

```python3
from fct_kiwi import Device, Resource

device = Device(0000000)     # Get a device using it's id
Device.register(device)      # Register the device manually
device.update()              # fetch the device resource on balena cloud

# Trick to print all registrers
for cls in Resource.__subclasses__():
    print(cls.get_registry())
```

output

```bash
Nonebeter
None
None
None
None
None
<ResourceGroup[Device]>: [kiwibot4U063] 
None
<ResourceGroup[Fleet]>: [1....2] 
<ResourceGroup[Release]>: [3....0] 
```

you can access foreign resources from the origiginal one, for instance, to access the fleet of a device, you could just call the `get_fleet()` method:

```python3
fleet = device.get_fleet()
```

### Resource Group

ResourceGroup is a class that contains an up to date data structure containing all devices that fulfill a common condition. It is better understandable with an example:

```python3
devices = Device.fromFleet(fleet_id=<fid>) # Returns a resource group
```

`Devices.fromFleet()` returns a resource group with all devices that belong to the fleet specifiedwith the parameter `fleet_id`, now you can use `devices.update()` each time you want to sync the information of the devices with Balena cloud.

#### updating resource groups

It is better to use the `update` method in a resource group than to loop through a list of devices calling the Resource scoped `update` method, since resource group fetches the entire resource group in a single request instead of looping through every resource.

If a resource contained in a resource group is deleted (for instance, using the `delete() method`), this resource will be removed from all existing resource groups. For this reason, if you are looping through a resource group while it is possible that a resource is deleted, then you would need to make a copy of the data structure and loop through the copy instead, here an example:

```python3
for device in list(devices.values()):
    # may call device.delete()
```

### Available resources

Currently, the package has mapped the following resources into classes:

* `Device`
* `DeviceEnv`
* `DeviceServiceEnv`
* `DeviceTag`
* `Fleet`
* `FleetEnv`
* `FleetServiceEnv`
* `Release`
* `Service`
* `ServiceInstall`

These are not near all resources Balena offers, but these are the ones necessary to do some fleet and devices management, including release updates and envs.


## Envs

In Balena, there are 4 kind of environment variables:

1. Those which are attached to a device: `DeviceEnv`
2. Those which are attached to a service installed in a device: `DeviceServiceEnv`
3. Those which are attached to a fleet: `FleetEnv`
4. Those which are attached to a service belonging to a fleet: `FleetServiceEnv`

Devices belonging to a fleet load all the fleet variables by default and then overwrites those with matching names in the device variables.

### Deleting envs

fetch the variables you want to delete and call the `delete()` method, here is an one-liner:
```python3
DeviceEnv.fromDeviceAndName(<DEVICE ID>, <VARIABLE NAME>).delete()
```
note: you can use `delete()` with resource groups to delete several resources at once.

### Changing and creating device variables

If the variable already exists:

```python3
success = device.overwrite_env(var_name, new_value)
```
Note: `new_value` is always of type string, it will be later parsed to int or bool by Balena cloud during the request performed.

`overwrite_env` all the service and environment variables of both the device and fleet where the device belongs; envs matching `var_name` and overwrites it's value, if there is not a variable matching `var_name`, then the call fails and the method returns `False`

If the variable doesn't exist, or it is repeated between two or more services, this call won't be of much help. If you know the name of the service where the variable belongs, whe highly recommend you to use `set_env()`:

```python3
success = set_env(var_name, new_value, service_name="*")
```

The variable of the specified service name is changed, if it is a `DeviceEnv` rather than a `DeviceServiceEnv`, pass `None` or `"*"` as the parameter. If the variable with those specifications doesn't exist, it will create it.

Returns False on error.

### Changing fleet variables

fleets support `set_env()` method:

```python3
success = set_env(var_name, new_value, service_name="*")
```

Having variables gathered in 4 different classes can make scripts get large, so we tried to keep it simple by including the `set_env` method, here is an implementation of `set_fleet_env` you can try:

```python3
from fct_kiwi import ResourceNotFound, Fleet, FleetEnv, FleetServiceEnv, Service

def set_fleet_env(fleet_name: str, name: str, value: str, service_name: str | None = "*") -> bool:

    # Getting the fleet object
    try:
        fleet: Fleet = Fleet.fromAppName(fleet_name, select="id");
    except ResourceNotFound:
        print (f"fleet of name {fleet_name} doesn't exist")
        return False
    if fleet.id is None:
        return False  # Unexpected error
    
    # Handle FleetEnv
    if service_name is None or service_name == "*":
        try:
            env = FleetEnv.fromFleetAndName(fleet.id, name)
            env.patch({"value": value})
        except ResourceNotFound:
            # The variable doesn't exist, then create it
            FleetEnv.new({"application": fleet.id, "name": name, "value": value})

    # Handle FleetServiceEnv
    else:
        # Getting Service
        try:
            service = Service.fromFleetAndName(
                    fleet_id=fleet.id,
                    service_name=service_name)
            if service.id == None:
                return False # Unexpected error
        except ResourceNotFound:
            print (f"service of name {service_name} doesn't exist")
            return False

        try:
            env = FleetServiceEnv.fromServiceAndName(service_id=service.id, name=name)
            env.parch({"value": value})
        except ResourceNotFound:
            # The variable doesn't exist, then create it
            FleetEnv.new({"service": service.id, "name": name, "value": value})

    return True
```
