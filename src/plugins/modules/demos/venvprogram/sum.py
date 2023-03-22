def sum(numbers):
    result = 0
    for i in range(len(numbers)):
        result = result + numbers[i]
    return result

if __name__ == "__main__":
    import argparse
    import sys
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('numbers', nargs='+', type=int)
        args = parser.parse_args()
        sum = sum(args.numbers)
        sys.stdout.write(str(sum))
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(str(e))