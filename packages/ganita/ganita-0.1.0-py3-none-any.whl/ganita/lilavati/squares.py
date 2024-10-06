import time
import math

def optimized_lilavati_square(number):
    if number < 10:
        return number * number

    num_str = str(number)
    length = len(num_str)
    result = 0
    
    # Pre-calculate powers of 10
    powers_of_10 = [10 ** i for i in range(length)]

    for i, digit in enumerate(num_str):
        digit = int(digit)
        place_value = powers_of_10[length - i - 1]
        term = digit * place_value
        
        # Square of the term
        result += term * term
        
        # Cross products
        remaining = int(num_str[i+1:]) if i < length - 1 else 0
        result += 2 * term * remaining

    return result

def lilavati_square(number):
    num_str = str(number)
    length = len(num_str)
    result = 0

    for i, digit in enumerate(num_str):
        digit = int(digit)
        place_value = 10 ** (length - i - 1)
        term = digit * place_value
        
        result += term ** 2
        
        for j in range(i + 1, length):
            other_digit = int(num_str[j])
            other_place_value = 10 ** (length - j - 1)
            result += 2 * term * other_digit * other_place_value

    return result

def multiplication_square(number):
    return number * number

def exponentiation_square(number):
    return number ** 2

def pow_square(number):
    return pow(number, 2)

def math_pow_square(number):
    return math.pow(number, 2)

def time_function(func, number, iterations=1000000):
    start_time = time.time()
    for _ in range(iterations):
        result = func(number)
    end_time = time.time()
    return result, end_time - start_time

def main():
    number = 12345
    iterations = 1000000

    methods = [
        ("Lilavati's method", lilavati_square),
        ("Optimized Lilavati's method", optimized_lilavati_square),
        ("Multiplication", multiplication_square),
        ("Exponentiation", exponentiation_square),
        ("pow() function", pow_square),
        ("math.pow() function", math_pow_square)
    ]

    print(f"Calculating square of {number} using different methods:")
    print(f"Each method is run {iterations} times for accurate timing")
    print("-" * 50)

    for method_name, func in methods:
        result, duration = time_function(func, number, iterations)
        print(f"{method_name}:")
        print(f"  Result: {result}")
        print(f"  Time taken: {duration:.6f} seconds")
        print()

if __name__ == "__main__":
    main()