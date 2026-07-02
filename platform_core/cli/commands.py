from doctor import doctor


def execute(command):

    if command == "doctor":
        doctor()

    elif command == "init":
        print("Initialization Complete.")

    elif command == "validate":
        print("Validation Pending.")

    elif command == "build":
        print("Build Pending.")

    else:
        print("Unknown Command")
