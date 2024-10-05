
## Version 0.3.0

This is the first major version of the code that is in a stable enough state for
use by other people. The code has been tested on the standard MCNP tallies when
binned. It has not been tested on unbinned tallies or tallies that have DE/DF
cards. Additionally, it is unable to process tallies that are binned by multiple
variables. It works best if each named tally is only for a single surface /
cell / detector point.

Soon there will be functionality to process Table 126 and the particle creation/
loss tables.

There are no plans at the moment to parse KCODE calculations.
