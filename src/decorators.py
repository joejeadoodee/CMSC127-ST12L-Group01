def screen(func):
  
    def wrapper():
        print()
        print("-" * 10)
        func()
    return wrapper