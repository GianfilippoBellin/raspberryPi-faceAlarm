from Models.Connections import *
from Models.Detectors import DetectorFace, DetectorPedestrian

ID_CAMERA = 1


def init():
    # Load Call configurations
    c = ConfigurationsConnection()
    c.saveConfigurations()


if __name__ == '__main__':
    init()

    #DetectorPedestrian().find()
    DetectorFace().find()

    print("\n|Finish|")
