#!/usr/bin/env python

import argparse
import sys
import logging

from d7a.alp.command import Command

from d7a.phy.channel_id import ChannelID
from d7a.system_files.factory_settings import FactorySettingsFile

from modem.modem import Modem

from util.logger import configure_default_logger


def received_command_callback(cmd):
  logging.info(cmd)
  if cmd.execution_completed:
      sys.exit(0)

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
argparser.add_argument("-o", "--offset", help="offset of gain", default=0, type=int, required=False)
argparser.add_argument("-lr", "--low_rx", help="rx bandwidth for low rate", default=10468, type=int, required=False)
argparser.add_argument("-nr", "--normal_rx", help="rx bandwidth for normal rate", default=78646, type=int, required=False)
argparser.add_argument("-hr", "--high_rx", help="rx bandwidth for high rate", default=125868, type=int, required=False)
config = argparser.parse_args()
configure_default_logger(config.verbose)


modem = Modem(config.device, config.rate, unsolicited_response_received_callback=received_command_callback)
modem.connect()

print("gain set to {}, rx low {}, normal {} and high {}".format(config.offset, config.low_rx, config.normal_rx, config.high_rx))

fsFile = FactorySettingsFile(gain=config.offset, rx_bw_low_rate=config.low_rx, rx_bw_normal_rate=config.normal_rx,
                             rx_bw_high_rate=config.high_rx)

print( '[{}]'.format(', '.join(hex(byte) for byte in list(fsFile))))

modem.execute_command(
  alp_command=Command.create_with_write_file_action(
    file_id=1,
    data=list(fsFile),
  )
)

# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     sys.exit(0)
