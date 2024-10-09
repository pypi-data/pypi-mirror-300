from .utils import *
import math
# ACL_FUNC_VISIBILITY aclTensor * aclCreateTensor(
#     const int64_t * viewDims,
#     uint64_t viewDimsNum,
#     aclDataType dataType,
#     const int64_t * stride,
#     int64_t offset,
#     aclFormat format,
#     const int64_t * storageDims,
#     uint64_t storageDimsNum,
#     void * tensorData)
libnnopbase.aclCreateTensor.argtypes = [
    ctypes.c_void_p,  # viewDims
    ctypes.c_uint64,  # viewDimsNum
    ctypes.c_int,    # dataType
    ctypes.c_void_p,  # stride
    ctypes.c_int64,  # offset
    ctypes.c_int,    # format
    ctypes.c_void_p,  # storageDims
    ctypes.c_uint64,  # storageDimsNum
    ctypes.c_void_p,  # tensorData
]
libnnopbase.aclCreateTensor.restype = ctypes.c_void_p
libnnopbase.aclDestroyTensor.argtypes = [ctypes.c_void_p]
libnnopbase.aclDestroyTensor.restype = ctypes.c_int


class AclNDTensor:
    def __init__(self, np_array: np.ndarray):
        self.np_array = np_array
        self.op_runner = None
        self.data_bytes_size = np_array.size * np_array.itemsize
        self.mem_size = int(
            math.ceil(np_array.size * np_array.itemsize / 256) * 256)
        if self.mem_size > 0:
            self.device_ptr, ret = acl.rt.malloc(self.mem_size, 0)
            print_ret("AclNDTensor malloc", ret)
            assert ret == 0
            ret = acl.rt.memcpy(
                self.device_ptr,
                self.mem_size,
                np_array.ctypes.data,
                self.data_bytes_size,
                1,
            )
            print_ret("AclNDTensor memcpy", ret)
            assert ret == 0
        else:
            self.device_ptr = 0
        self.shape = np.array(np_array.shape, dtype=np.int64)
        self.shape_size = len(np_array.shape)
        self.acl_dtype = numpy_dtype_2_acl_dtype(np_array.dtype)
        self.ptr = libnnopbase.aclCreateTensor(
            self.shape.ctypes.data,
            self.shape_size,
            self.acl_dtype,
            0,
            0,
            2,
            self.shape.ctypes.data,
            self.shape_size,
            self.device_ptr
        )
        assert (self.ptr != 0)
        self.need_copy_to_cpu = False

    def __str__(self) -> str:
        return str(self.to_cpu())

    def __del__(self):
        if self.ptr != 0:
            ret = libnnopbase.aclDestroyTensor(self.ptr)
            self.ptr = 0
            print_ret("aclDestroyTensor", ret)
            assert ret == 0
        if self.device_ptr != 0:
            ret = acl.rt.free(self.device_ptr)
            self.device_ptr = 0
            print_ret("acl.rt.free错误", ret)
            assert ret == 0

    def to_cpu(self):
        if self.op_runner is not None:
            self.op_runner.sync_stream()
        if self.need_copy_to_cpu:
            ret = acl.rt.memcpy(
                self.np_array.ctypes.data,
                self.data_bytes_size,
                self.device_ptr,
                self.data_bytes_size,
                2,
            )
            assert ret == 0
            self.need_copy_to_cpu = False
        return self.np_array
