from controller import controller

print("Development purposes only.")
controller = controller()

while True:
    prompt = input("CMD: ")
    print(controller.evaluate(input=prompt))
