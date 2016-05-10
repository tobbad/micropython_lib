# micropython_lib
Micropython drivers for diffrent I2C/SPI chips.

## Folder structure:

| Folder  | Content |
|---------|---------|
| boards  | Subfolder with board specific code |
| display | Display driver chips |
| lib     | Generic SPI/I2C library |
| sensor  | Different sensors |
| sound   | Sound chips |
| test    | Testframe work for automatic deploy and test of micropython builds (Work in progress) |
| tools   | Different tools to support micropython code development. |

These drivers just provide the basic support for the sensors and are work in progress.

## Setting up a board
There is a board specific folder in the `boards` subfolder. The name of these board specific folder directly map to a stmhal make build target. Enter such a folder you will find a `trasnfer.sh` script which copies the necessary python-files to a USB-mounted board if run in a BASH shell. The mount location of the board is set in the `TARGET` variable at the top of `transfer.sh`. There is no Microsoft support for that script. 
