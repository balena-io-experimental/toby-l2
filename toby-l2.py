import gi
import threading

gi.require_version('ModemManager', '1.0')

from gi.repository import Gio, ModemManager

CMD_TIMEOUT = 25

connection = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)

manager = ModemManager.Manager.new_sync(connection, Gio.DBusObjectManagerClientFlags.DO_NOT_AUTO_START, None)

for obj in manager.get_objects():
    modem = obj.get_modem()

    manufacturer = modem.get_manufacturer()
    drivers = modem.get_drivers()

    if manufacturer == 'u-blox' and 'rndis_host' in drivers:
        print('u-blox RNDIS enabled modem found')

        rndis_optimization = modem.command_sync('AT+UDCONF=67', CMD_TIMEOUT, None)

        print('RNDIS optimisation reported:', rndis_optimization)

        if rndis_optimization == '+UDCONF: 67,1':
            print('Disable RNDIS optimizations and reset the modem')

            modem.command_sync('AT+UDCONF=67,0', CMD_TIMEOUT, None)
            modem.reset_sync(None)


threading.Event().wait()
