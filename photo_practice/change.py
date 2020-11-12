import os


def main():
    for i in range(10, 13):
        for j in range(1, 31):
            os.rename('t' + '0' + str(i) + '.' + str(j) + '.png', 'p' + str(i) + '.' + str(j) + '.png')


if __name__ == '__main__':
    main()