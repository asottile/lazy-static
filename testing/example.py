# pytest will realize all attrs of a test module so this has to be separate
from lazy_static import lazy


@lazy
def for_test_1() -> int:
    print('computing')
    return 5


for_test_2 = lazy(lambda: print('computing') or 6)
