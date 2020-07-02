import pyvisa
rm = pyvisa.ResourceManager()
print 'all resources:',rm.list_resources()
inst = rm.open_resource(rm.list_resources()[0])
print 'first resource info',inst.query("*IDN?")

inst.write('ACQuire:STOPAfter SEQ')
inst.write('ACQuire:SEQuence:NUMSEQuence 100')
inst.write('ACQuire:STATE ON')
