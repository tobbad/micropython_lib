#!/bin/sed -f
/\(^#define\)/!d
s/[[:space:]]*([[:space:]]*uint[0-9]\+_t[[:space:]]*)[[:space:]]*//g
s/^#define[[:blank:]]\+\([A-Za-z0-9_]\+\)[[:blank:]]\+\((\)*\([0-9A-Fa-fxX.]\+\([[:blank:]]*<<[[:blank:]]\+[0-9]\+\)*\)[[:blank:]]*\()\)*[[:blank:]]*\(.*\)/\1 = const(\3) \6/g
s/\/\*/#/g
s/\/\//#/g
s/!<//g
s/\*\///g
s/[[:blank:]]*$//g