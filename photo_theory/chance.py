import os


def main():
    for i in range(9, 10):
        for j in range(14, 80):
            os.rename('t' + str(i) + '.' + str(j) + '.png', 't' + '0' + str(i) + '.' + str(j) + '.png')


if __name__ == '__main__':
    main()