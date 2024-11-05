# pip install notify2

import notify2
import dbus

notify2.init('Test')
n = notify2.Notification('Hello', 'This is a test')
n.show()
