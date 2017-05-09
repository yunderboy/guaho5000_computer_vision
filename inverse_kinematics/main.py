from claw import Claw
from control import Stepper

claw = Claw()


stepper = Stepper('4', 63.209, -36.941, 0)
speeds = float(input("Hastighed yo?  "))
a = int(input("0 for manuel og 1 for koordinater:  "))
if a == 0:
    while True:
        steps = input("Yo, hvor meget skal vi move i step?  ")
        dirs = int(input("Dir plox? 0=OP,tilbage,venstre and 1=NED,frem,højre :  "))
        motor = str(input("Motor: higher, lower, rot:  "))
        print ("Moving ({}), speed ({}), dir({}), motor ({})".format(steps, speeds, dirs, motor))
        stepper.move(motor, steps, dirs, speeds)
elif a == 1:
    while True:
        score = list(map(float, input("Skriv, x, y, z:  ").split()))
        print(score)
        cl = input("[C]lose/[O]pen else nothing : ")
        stepper.main(score)
        if cl.upper() == "C":
            claw.forward(150)
            
        elif cl.upper() == 'O':
            claw.backwards(150)