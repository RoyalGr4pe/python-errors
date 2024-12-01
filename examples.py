from python_errors.errors import *
from python_errors.config import setup_errors


setup_errors(delete_logs_on_start=True)


@secure_call(rv=7)
def key_error():
    some_dict = {
        "item-1": 1,
        "item-2": 2,
        "item-3": 3,
        "item-4": 4,
        "item-5": 5,
        "item-6": 6,
    }
    some_dict["item-7"]

@secure_array_call()
def array_error(array, other=None):
    array.append(6)


def main():
    key_error_value = key_error()
    print(key_error_value)

    # Finds incorrect type <class 'str'>
    array_error([0, 1, 2, 3, 4, 5, "6"])

    # Catches change in size of the array
    array_error([0, 1, 2, 3, 4, 5])

    # Catches param not being array
    array_error(1, [0, 1, 2, 3, 4, 5])




if __name__ == "__main__":
    main()
