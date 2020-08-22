import argparse
import board
import busio
import digitalio
import adafruit_max31855


class Thermocouple():
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("-p", "--cs-pin", action="store",
                                 help="CS PINの接続先(BCM). Default: 5", default=[5], type=int, nargs='*')
        self.parser.add_argument("--verbose",  action='store_true', help="詳細な出力.")

    def measure(self):
        '''熱電対の温度を測定
        '''

        self.args = self.parser.parse_args()
        pins = self.args.cs_pin
        verbose = self.args.verbose

        temps = []
        for i in range(len(pins)):
            spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
            cs = eval("digitalio.DigitalInOut(board.D%s)" % pins[i])
            max31855 = adafruit_max31855.MAX31855(spi, cs)

            temps.append(max31855.temperature)

        self.__output(pins, temps, verbose)

    def __output(self, pins, temps, verbose):
        for i in range(len(pins)):
            if verbose:
                print(f"cs-pin{pins[i]}: {temps[i]} ℃")
            else:
                print(f"{temps[i]} ", end='')
            
        if not verbose:
            print()


if __name__ == "__main__":
    thermocouple = Thermocouple()
    thermocouple.measure()