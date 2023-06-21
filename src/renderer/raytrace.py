import renderer.scene as sc
import ctypes as ct


def raytrace(scene: sc.Scene, maxBounces, raysPerPixel):
    
    a = (sc.Vertex * 6)()

    libc = ct.CDLL("libc.so.6")

    libc.malloc.restype = ct.c_void_p
    libc.malloc.argtypes = [ct.c_size_t]

    for i in range(len(a)):
        a[i].position = (1.0, 2.0, 3.0)
        a[i].normal = (6.9, 7.9, 4.2)
        a[i].textureCoord = (1.1, 1.2, 1.3)

    b = libc.malloc(6 * ct.sizeof(sc.Vertex))

    ct.memmove(b, a, 6 * ct.sizeof(sc.Vertex))
    
    array = ct.cast(b, ct.POINTER(sc.Vertex))

    

    for i in range(6):
        print(list(array[i].position), list(array[i].normal), list(array[i].textureCoord), sep='\n')

    pass
