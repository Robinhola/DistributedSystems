# Purrfect

Purrfect is a perfect fault detector, using a reliable communication channel, it tries to detect the malfunction of a distant computer.

Purrfect uses the following hypothesis:
  - It needs to run on top of a reliable communication channel.
  
## Functioning

Purrfect uses TCP or CanalPlus to "ping" a distant machine. If the specified timeout is reached, then Purrfect declares the distant machine faulty.
Purrfect will try to connect back to the faulty machine to detect when it is back online.

## Usage

./purrfect [TCP|C+] target_IP:PORT frequencyofpings timeout

frequencyofpings is in milliseconds as well as timeout.

This allows the user to declare a machine faulty as quickly or as slowly as it can.

## Known issues

**Purrfect does not exist yet!**




