from multi_worker import MultiWorker
import time


def test_multi_worker(target):
    print(target)
    time.sleep(1)
    yield True

def main():
    i = 0
    # test code begin
    test_list = []
    for target in range(88):
        test_list.append({
            'sample': target
        })
    # test code end
    workers = MultiWorker(test_list)
    for item in workers.start(test_multi_worker, 3) :
        if item:
            i += 1
        if i > 11:
            break
    print('main is end')


if __name__ == "__main__" :
    main()
