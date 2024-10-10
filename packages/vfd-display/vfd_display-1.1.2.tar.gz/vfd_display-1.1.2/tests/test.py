from vfd_display import VfdDisplay

vfd = VfdDisplay(port='/dev/ttyUSB0', enabled=True)
vfd.write_line("Hello, World!", line=1, column=1)
