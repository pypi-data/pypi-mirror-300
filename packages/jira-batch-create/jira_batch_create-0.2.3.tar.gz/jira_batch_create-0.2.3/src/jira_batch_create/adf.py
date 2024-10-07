import json
from cffi import FFI

def get_description_in_adf_format(**kwargs):
    description = kwargs.get("value")
    ffi = FFI()
    lib = ffi.dlopen("htmltoadf.dll")
    ffi.cdef("char * convert(char *);")
    desc = description.encode('utf-8')
    converted_text = json.loads(ffi.string(lib.convert(desc)).decode('utf-8'))
    return converted_text
