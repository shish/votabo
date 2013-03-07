from dogpile.cache import make_region

fast = make_region()
slow = make_region()
