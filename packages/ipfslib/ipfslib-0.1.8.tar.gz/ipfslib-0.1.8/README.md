# ipfslib - Python IPFS Library
Simple wrapper for IPFS Kubo RPC API in Python

## Installation
    py -m pip install ipfslib

## Connect to API
First you need to create an object of the Connect class. For most usecases you don't need to specify any parameter as it's taking IPFS standard values:

    import ipfslib
    api = ipfslib.Connect()

If your API doesn't run on 127.0.0.1:5001, you can specify your own API endpoint:

    import ipfslib
    api = ipfslib.Connect("127.0.0.1", 5001)

## Interacting with IPFS
There are some tools to interact with the IPFS network. But as this library is still in development some of the functions could change in behaviour any time.

---
### IPFS.add()
Adding files to IPFS is simple.

    import ipfslib
    api = ipfslib.Connect()

    cid = ipfslib.IPFS.add(api, "helloworld.txt")
    print(cid)

This function can take the parameter `mode`. If `'t'` is passed, the file is opened in read mode (r). If `'b'` is passed, then the file is opened in read byte mode (rb).

---
### IPFS.cat()
Getting files from IPFS by the IPFS-Path. IPFS-Paths start with `/ipfs/` or `/ipns/`.

    import ipfslib
    api = ipfslib.Connect()

    path = "/ipfs/QmQrXZ4iXdEKQMiQT6GRg2Wy3vxb9exR25sYdaqoHwWWuR"
    text = ipfslib.IPFS.cat(api, path)

    print(text)

This function can also take a `mode` Parameter. It can either be set to `'t'` for "Text Mode", which returns a string in plain text. The other mode is `'b'`, which returns a string with byte data. This can be useful to retreive imagages from IPFS.

    import ipfslib
    api = ipfslib.Connect()

    path = "/ipfs/bafkreibih73gfbpgkmskacqtlsr4vtp47lmx24skh7jv27bnhsmhtivbeq"
    data = ipfslib.IPFS.cat(api, path, mode='b')

    with open('cat.png', 'wb') as img:
        img.write(data)

---

### IPFS.get()
With this function you can retreive data from an IPFS content identifier (CID).

    import ipfslib
    api = ipfslib.Connect()

    cid = "QmQrXZ4iXdEKQMiQT6GRg2Wy3vxb9exR25sYdaqoHwWWuR"
    text = ipfslib.IPFS.get(api, cid)

    print(text)

This function can also take the `mode` parameter, which can be either set to `'t'` or `'b'`. Read *IPFS.cat()* above to learn more.

---
### IPFS.rem()
Remove files from being provided to IPFS by their CID.

    import ipfslib
    api = ipfslib.Connect()

    cid = "QmQrXZ4iXdEKQMiQT6GRg2Wy3vxb9exR25sYdaqoHwWWuR"
    ipfslib.IPFS.rem(cid)

---
### IPFS.resolve()
Resolve IPNS names to get the CID they're pointing to.

    import ipfslib
    api = ipfslib.Connect()

    ipns_name = "k51qzi5uqu5dk37cdlr3ztr4457txgqmukmiex8ohkzyeeqpwfph2e21sks16s"
    cid = ipfslib.IPFS.resolve(api, ipns_name)

    print(cid)

## Interacting with IPNS Keys
Most of these tools can be used while offline, except of course `ipfslib.Key.publish()`.

---
### Key.generate()
This let's you generate a new IPNS Key.

    import ipfslib
    api = ipfslib.Connect()

    ipns_name = ipfslib.Key.generate(api, "test_key")

    print(ipns_name)

---
### Key.list()
Returns a list with dictionaries for every key. Each entry in the list has two keys (`Name` and `Id`). `Name` is the local name under which the key is stored. `Id` is the public IPNS Name of the key.

    import ipfslib
    api = ipfslib.Connect()

    keys = ipfslib.Key.list(api)

    # Get the IPNS name of the Key with the name "test_key"
    for key in keys:
        if key['Name'] == 'test_key':
            ipns_name = key['Id']
            break
    
    print(ipns_name)

---
### Key.publish()
This let's you link a CID to your IPNS Name.

    import ipfslib
    api = ipfslib.Connect()

    cid = "QmQrXZ4iXdEKQMiQT6GRg2Wy3vxb9exR25sYdaqoHwWWuR"

    ipfslib.Key.publish(api, cid, key_name='test_key')

If no key name is given to publish to, it will automatically publish to the 'self' key, which is your node's main key.

---
### Key.rename()
This let's you rename your IPNS keys locally. 

    import ipfslib
    api = ipfslib.Connect()

    old_name = "test_key"
    new_name = "project_key"

    ipfslib.Key.rename(api, old_name, new_name)

---

## Note
That's actually it for Version 0.1, thank you for considering to use my library. You can check out my blog to find out how I made this.

Blog: https://blog.remboldt.eu/ipfslib/  
GitHub: https://github.com/remboldt/ipfslib/
