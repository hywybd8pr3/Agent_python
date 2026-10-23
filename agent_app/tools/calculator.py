def calculate(a:float,b:float) -> str:

    if type(a) not in (int,float) or type(b) not in (int,float):
        raise TypeError('a和b必须是数字')
    return str(a+b)

