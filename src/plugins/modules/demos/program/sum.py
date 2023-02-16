def demo_sum(numbers):
    sum = 0
    for i in range(len(numbers)):
        sum = sum + numbers[i]
    return sum

if __name__ == "__main__":
    import argparse
    import sys
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('numbers', nargs='+', type=int)
        args = parser.parse_args()
        sum = demo_sum(args.numbers)
        sys.stdout.write(str(sum))
    except Exception as e:
        sys.stderr.write(str(e))