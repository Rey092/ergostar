from typing import Union

from dishka import Provider, Scope, make_container, provide, AnyOf


class A:

    def do_a(self):
        print("A: do_a")


class B:

    def do_b(self):
        print("B: do_b")


class MyProvider(Provider):
    @provide(scope=Scope.APP)
    def get_a(self) -> A:
        return A()

    @provide(scope=Scope.APP)
    def get_b(self) -> B:
        return B()


provider = MyProvider(scope=Scope.APP)
# provider.provide(A)
# provider.provide(B)
provider.provide(B, provides=A)
provider.provide(B, provides=B)

container = make_container(provider)
RESULT = container.get(A)
print(type(RESULT))
RESULT = container.get(B)
print(type(RESULT))
