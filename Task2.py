import sys
import time


class CacheValue:

    def __init__(self, key, value, create_at):
        self.key = key
        self.value = value
        self.create_at = create_at


class CacheFibonacci:

    def __init__(self, live_time, max_count, max_memory, enable_logging):
        self.live_time = live_time
        self.max_count = max_count
        self.max_memory = max_memory
        self.enable_logging = enable_logging
        self.cached_values = []

    def cache(self, key, value):
        if len(self.cached_values) < self.max_count:
            cache_value = CacheValue(key, value, time.time())
            if sys.getsizeof(cache_value) < self.max_memory:
                self.cached_values.append(cache_value)

    def find_cache_value(self, key):
        cache = next((x for x in self.cached_values if x.key == key), None)
        if cache is not None:
            if time.time() > cache.create_at + self.live_time:
                if self.enable_logging:
                    print('Значение не найдено в кэше')
                self.cached_values.remove(cache)
                return None
            else:
                if self.enable_logging:
                    print('Значение найдено в кэше')
                return cache
        else:
            if self.enable_logging:
                print('Значение не найдено в кэше')
            return None


def cache(live_time=10, max_count=10, max_memory=10, enable_logging=True):
    def cache_fun(fun):
        _cache = CacheFibonacci(live_time, max_count, max_memory, enable_logging)

        def inner(*args):
            start = time.time() * 1000
            x = args[0]
            cached_value = _cache.find_cache_value(x)
            if cached_value is not None:
                if _cache.enable_logging:
                    print(f'Выполнено за {(time.time() * 1000 - start):.10f} ms')
                return cached_value.value
            else:
                fibonacci = fun(*args)
                _cache.cache(x, fibonacci)
                if _cache.enable_logging:
                    print(f'Выполнено за {(time.time() * 1000 - start):.10f} ms')
                return fibonacci

        return inner

    return cache_fun


@cache(1, 5, 50, True)
def get_fibonacci(x):
    i = 0
    fib1 = 1
    fib2 = 1
    while i < x - 2:
        fib_sum = fib1 + fib2
        fib1 = fib2
        fib2 = fib_sum
        i = i + 1
    return fib2


def main():
    get_fibonacci(20000)
    time.sleep(2)
    get_fibonacci(20000)
    get_fibonacci(20000)
    get_fibonacci(20000)
    get_fibonacci(30000)


if __name__ == '__main__':
    main()
