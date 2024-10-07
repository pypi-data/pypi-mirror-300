*Related to : [[Functionnalities]]*
```python
from yamcs.client import YamcsClient

import struct

  

client = YamcsClient("localhost:8090")

processor = client.get_processor("myproject", "realtime")

  

command = processor.issue_command("/MIB/JCC45006", args={"JCPD0009": 3, "JCPD0010": "EiPrRe"}, dry_run=True)

print(f"MIB cmd binary: {command.binary.hex()}")

  

raw_tc = processor.issue_command("/TEST/RAW_TC", args={"data": command.binary})

print(f"raw_cmd binary: {raw_tc.binary.hex()}")

  

pus_data = command.binary[9:]

pus_tc = processor.issue_command("/TEST/PUS_TC", args={"apid": 1, "type": 5, "subtype": 5, "ackflags": 0, "data": pus_data})

print(f"pus_cmd binary: {pus_tc.binary.hex()}")

  

#make a writable copy

pus_data = bytearray(command.binary[9:])

struct.pack_into('>H', pus_data, 0, 0xABCD)

pus_tc = processor.issue_command("/TEST/PUS_TC", args={"apid": 1, "type": 5, "subtype": 5, "ackflags": 0, "data": pus_data})

print(f"modified binary: {pus_tc.binary.hex()}")
```