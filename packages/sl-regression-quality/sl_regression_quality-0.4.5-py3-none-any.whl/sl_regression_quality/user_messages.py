from .global_constants import CYAN,  RESET, BLUE, GREEN


def parameters_messages(accuracy,resolution,sensitivity,range):
    
    print(f'2.1) Accuracy value:'+GREEN+ f'{round(accuracy,6)}'+RESET)
    print(f'2.2) Resolution value:' +GREEN+ f'{round(resolution,6)}'+RESET)
    print(f'2.3) Sensitivity value:' +GREEN+ f'{round(sensitivity,6)}'+RESET)
    print(f'2.4) Dynamic range:' +GREEN+ f'{round(range,6)}'+RESET)
    print(BLUE+'===='*20+RESET)