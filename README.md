# Intro
Start by installing pip and python3. 

# Dependencies
I use the pycryptodome package which can be installed with:
```
pip install pycryptodome
```

# Running Experiments
Navigate into the unziped folder and then copy and paste the code below for the steps. If you get an error that a port is already being used, change the ports specified (for example to 10003 and 10004) so that Mallory's first port matches input for Bob and her second port matches input for Alice.

## Part 1

**Run Gen to generate new key files.**
```
python3 Gen.py
```
**Start Bob, Mallory, and Alice in "no-cryptography" configuration.**
Open 3 terminal windows. In window 1 for Bob type:
```
python3 Bob.py localhost 10000
```
In window 2 for Mallory type:
```
python3 Mallory.py localhost 10000 localhost 10001
```
In window 3 for Alice type:
```
python3 Alice.py localhost 10001
```

**Send messages from Alice to Mallory to Bob.**
In Alice's window enter a message at the prompt and hit enter.

**Use Mallory to delete a message.**
After Mallory receives the message, follow the instructions to type d then enter to delete the message.

**Use Mallory to modify a message.**
First send another message from Alice. Then follow the instructions in Mallory's window to type m for modify and enter the new message to send.

## Part 2

**Start Bob, Mallory, and Alice in "Enc-only" configuration.**
Open 3 terminal windows. In window 1 for Bob type:
```
python3 Bob.py localhost 10000 --enc
```
In window 2 for Mallory type:
```
python3 Mallory.py localhost 10000 localhost 10001
```
In window 3 for Alice type:
```
python3 Alice.py localhost 10001 --enc
```
**Send messages from Alice to Mallory to Bob.**
Enter a message in Alice's window. In Mallory's window follow the instructions to hit enter to forward the message.

## Part 3

**Start Bob, Mallory, and Alice in "Mac-only" configuration.**
Open 3 terminal windows. In window 1 for Bob type:
```
python3 Bob.py localhost 10000 --mac
```
In window 2 for Mallory type:
```
python3 Mallory.py localhost 10000 localhost 10001 
```
In window 3 for Alice type:
```
python3 Alice.py localhost 10001 --mac
```

**Send messages from Alice to Mallory to Bob.**
Follow the prompts to send messages from Alice to Mallory, then press enter to send messages from Mallory to Bob.

**Use Mallory to replay an old message.**
Send a message from Alice to Mallory. Then at the prompt, enter "r" into Mallory and specify the message number of the message you want to replay. 

**Use Mallory to delete a message and pass the next message through.**
Send a message from Alice to Mallory. Then at the prompt, enter "d" into Mallory to delete the message. Send another message and hit enter in Mallory's window.

**Use Mallory to modify a message.**
Send a message from Alice to Mallory. Then at the prompt, enter "m" into Mallory and specify the new message contents. Hit enter to send.

## Part 4

Start Bob, Mallory, and Alice in "Enc-then-Mac" configuration.

```
python3 Bob.py localhost 10000 --mac --enc
```
In window 2 for Mallory type:
```
python3 Mallory.py localhost 10000 localhost 10001
```
In window 3 for Alice type:
```
python3 Alice.py localhost 10001 --mac --enc
```
**Send messages from Alice to Mallory to Bob.**
Follow the prompts to use the same process to send your message.
