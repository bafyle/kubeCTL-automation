import sys

def extract_deployment_name(data: str) -> str:
    return data.strip().split()[0]


def get_user_input_in_integer(min: int, max: int) -> int:
    while True:
        try:
            sys.stdin.flush()
            sys.stdout.flush()
            output = int(input())
            if output > max or output < min:
                raise ValueError
            return output
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        except ValueError:
            print("Invalid input: not valid number or out of pounds")
