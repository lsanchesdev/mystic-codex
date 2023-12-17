# Imports
import ctypes
import struct
import constants.memory as MemoryBook

# Define necessary Windows API functions
OpenProcess = ctypes.windll.kernel32.OpenProcess
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
CloseHandle = ctypes.windll.kernel32.CloseHandle
WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory


class Memory:
    def __init__(self, codex):
        self.codex = codex
        self.process = {
            'id': codex.grappler.getProcessID(),
            'base_memory': codex.grappler.getBaseAddress()
        }

    def readFromBase(self, address, size, is_pointer=False):
        return self.read((self.process['base_memory'] + address), size, is_pointer)

    def read(self, address, size=4, is_pointer=False):
        if not is_pointer:
            buffer = ctypes.create_string_buffer(size)
            bytesRead = ctypes.c_size_t()
            processHandle = OpenProcess(MemoryBook.MEMORY_SYSTEM_PROCESS_ALL_ACCESS, False, self.process['id'])

            if not processHandle:
                raise Exception("Could not open process")

            try:
                if ReadProcessMemory(processHandle, address, buffer, size, ctypes.byref(bytesRead)):
                    # Assuming little-endian
                    if size == 2:
                        return struct.unpack('<H', buffer.raw)[0]  # '<H' is for a 2-byte unsigned integer
                    elif size == 4:
                        return struct.unpack('<I', buffer.raw)[0]  # '<I' is for a 4-byte unsigned integer
                    elif size == 8:
                        return struct.unpack('<d', buffer.raw)[0]  # '<d' is for a 4-byte unsigned float
                    elif size == 16:
                        # Unpack string
                        unpacked_string = struct.unpack('16s', buffer.raw)[0]
                        # Decode string and remove excess bytes
                        return unpacked_string.decode('latin1').split('\x00', 1)[0]
                    else:
                        return buffer.raw
                else:
                    raise Exception("Could not read process memory")
            finally:
                CloseHandle(processHandle)
        else:
            return self.read(address, size)

    def write(self, address, data, size):
        processHandle = OpenProcess(MemoryBook.MEMORY_SYSTEM_PROCESS_ALL_ACCESS, False, self.process['id'])
        if not processHandle:
            raise Exception("Could not open process")

        try:
            # Create empty packed data variable
            packed_data = None

            # Convert data to bytes if it's not already
            if not isinstance(data, bytes):
                if size == 2:
                    packed_data = struct.pack('<H', data)
                elif size == 4:
                    packed_data = struct.pack('<I', data)
                elif size == 8:
                    packed_data = struct.pack('<d', data)
                elif size == 16:
                    packed_data = data.encode('utf-8')  # Assuming UTF-8 encoding
                else:
                    raise ValueError("Unsupported data size")

            size = len(packed_data)
            bytesWritten = ctypes.c_size_t()
            if not WriteProcessMemory(processHandle, address, packed_data, size, ctypes.byref(bytesWritten)):
                raise Exception("Could not write process memory")
        finally:
            CloseHandle(processHandle)

    def readList(self, index, base_address, first_element_address):
        # Read the list content from the base address
        list_content = self.read(base_address, 4)

        # Read current, next, and alternate addresses from the first element address
        current_address = self.read(first_element_address, 4)
        next_address = self.read(first_element_address + 4, 4)
        alternate_address = self.read(first_element_address + 12, 4)

        # Calculate the offset and adjust if negative
        offset = current_address - next_address
        if offset < 0:
            offset += 3

        # Adjust the offset based on the index
        offset = offset // 4
        offset += index

        # Determine the final address to read from
        if offset >= 0:
            address_divisor = offset // list_content
        else:
            address_divisor = (offset + 1) // list_content - 1

        if address_divisor == 0:
            final_address = current_address + index * 4
        else:
            next_address = self.read(alternate_address + address_divisor * 4, 4)
            final_address = (offset - list_content * address_divisor) * 4 + next_address

        # Read and return the value from the final address
        return self.read(final_address, 4)