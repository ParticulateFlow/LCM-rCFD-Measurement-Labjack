from datetime import datetime
import yaml
from pathlib import Path

class Configuration():
    def __init__(self, pathToConfigFiles: Path) -> None:
        self.pathToConfigFiles = pathToConfigFiles
        self.read_files()
       
    def read_files(self):
        with open(str(self.pathToConfigFiles/'labjack.yml'), "r") as ymlfile:
            self.labjack = yaml.safe_load(ymlfile)

        with open(str(self.pathToConfigFiles/'experiment.yml'), "r") as ymlfile:
            self.experiment = yaml.safe_load(ymlfile)  

    def save(self, pathToSave: Path, basename: str = 'Experiment_configuration') -> None:
        self.read_files()
        filename = str(pathToSave / f'{basename}.txt')
        with open(filename,'w') as f:
            # Header
            f.write(f'+'*25 + '\n')
            f.write('LCM Experiment Parameter \n'.upper())
            f.write(f'+'*25 + '\n')
            # Datetime information
            f.write('\nDate and Time: \n'.upper())
            f.write(f'-'*30 + '\n')
            f.write(f'Date: ' + datetime.now().strftime(r'%d.%B.%Y') + '\n')
            f.write(f'Time: ' + datetime.now().strftime(r'%H:%M') + ' Uhr\n')

            # Setup information
            f.write('\nSettings: \n'.upper())
            f.write(f'-'*30 + '\n')
            f.write(f'Inlet: ' + self.experiment['INLET'] + '\n') #ring, one side
            f.write(f'Outlet: ' + self.experiment['OUTLET'] + '\n') #middle, top, bottom
            f.write(f'Thermostat: ' + str(self.experiment['THERMOSTAT']) + '\n') #middle, top, bottom

            # comment
            f.write('\nComment: \n'.upper())
            f.write(f'-'*30 + '\n')
            f.write(self.experiment['COMMENT'] + '\n') #ring, one side

            # Measurement information
            f.write('\nMeasurement information: \n'.upper())
            f.write(f'-'*30 + '\n')
            f.write(f'Sample Rate: ' + str(self.experiment['SAMPLE_RATE']) + '\n')


            # Measurement information
            f.write('\nLabjack information: \n'.upper())
            f.write(f'-'*30 + '\n')

            for section in self.labjack:
                f.write(f'{section}:\n')
                for sensor, channel in self.labjack[section].items():
                    f.write(f'\t {sensor}: {channel}\n')


if __name__ == '__main__':
    configPath = Path(__file__).parent.parent.absolute() / 'configs'

    conf = Configuration(pathToConfigFiles=configPath)

    print(conf.experiment)
    print(conf.labjack)

    conf.save(pathToSave=configPath, basename='test_config')

    print('Done')