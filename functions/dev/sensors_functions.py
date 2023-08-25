from labjack import ljm

def readPT100(handle: ljm, channel: str, T_min:int = 0, T_max:int = 150) -> float:
    '''function for reading PT100
    Measurement range:
        T_min -> Temperature in Grad Celsius for 0V
        T_max -> Temperature in Grad Celsius for 10V
        
    returns T in Grad Celsius
    '''
    k = (T_max-T_min) / 10 # slope
    d = T_min # offset
    U = ljm.eReadName(handle, channel) # voltage
    return k*U + d

def readFlowMeter(handle: ljm, channel: str, R_shunt:int = 470, mdot_min:int = 0, mdot_max: int = 2000) -> float:
    '''function for reading Flowmeter
    Measurement range:
        mDot_min -> massflow in ml/min for 4mA
        mDot_max -> massflow in ml/min for 20mA

    returns: m_dot in ml/min
    '''
    k = (mdot_max-mdot_min)/(16*1e-3) # slope
    d = mdot_min - k*4*1e-3 # offset

    I = ljm.eReadName(handle, channel)/R_shunt # current
    if I < 4*1e-3: I = 4*1e-3 # correct no flow
    return k*I + d

def readWarmCold(handle: ljm, channel:str) -> str:
    U = ljm.eReadName(handle, channel) # voltage

    if U <= 1: # False
        return "Warm"
    else:
        return "Cold"


if __name__ == '__main__':
    import yaml
    labjackT7Pro = ljm.openS("T7", "USB", "ANY")
    print(f"T_warm = {readPT100(handle=labjackT7Pro, channel='AIN0'):.1f}{chr(176)}C") 

    print(f"mDot_warm = {readFlowMeter(handle=labjackT7Pro, channel='AIN11'):.1f}ml/min")
    print(f"mDot_cold = {readFlowMeter(handle=labjackT7Pro, channel='AIN13'):.1f}ml/min")

    print(readWarmCold(handle=labjackT7Pro,channel="AIN10"))

    ## Second Test
    import sys
    from pathlib import Path

    filename = Path(__file__).parent.parent / "configs" / 'labjack.yml'
    print(filename)
    # my labjack T7-Pro
    labjackT7Pro = ljm.openS("T7", "USB", "ANY")

    # Open configuration file
    with open(filename, "r") as ymlfile:
        config = yaml.safe_load(ymlfile)

    print("System Temperatures")
    print("-"*15)
    for key, value in config["PT100"]['Setup'].items():
        print(f"{key}\t= {readPT100(handle=labjackT7Pro, channel=value):.1f}{chr(176)}C")

    print("\nBox Temperatures")
    print("-"*15)
    for key, value in config["PT100"]['Box'].items():
        print(f"{key}\t= {readPT100(handle=labjackT7Pro, channel=value):.1f}{chr(176)}C")

    print("\nSystem Mass flow")
    print("-"*15)
    for key, value in config["Flowmeter"].items():
        print(f"{key} = {readFlowMeter(handle=labjackT7Pro, channel=value):.1f}ml/min")
