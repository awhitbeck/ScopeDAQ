import pyvisa
rm = pyvisa.ResourceManager()
print 'all resources:',rm.list_resources()
inst = rm.open_resource(rm.list_resources()[0])
print 'first resource info',inst.query("*IDN?")
