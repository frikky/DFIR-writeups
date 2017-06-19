# Based on the library example

import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace 
import volatility.plugins.taskmods as taskmods

registry.PluginImporter()
config = conf.ConfObject()

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

config.parse_options()
config.PROFILE = "VistaSP1x86"
config.LOCATION = "file:///tmp/memdump.mem"

p = taskmods.PSList(config)
for process in p.calculate():
    print "%s" % process
