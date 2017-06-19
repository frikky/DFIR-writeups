# From SANS: Starting without the questions asked by the author 
http://www.ashemery.com/dfir.html
Me learning to better deal with the data output of volatility \o/

Commands to start off the investigation:
$ volatility -f /tmp/memdump.mem imageinfo
$ export VOLATILITY_LOCATION=file:///tmp/memdump.mem
$ export VOLATILITY_PROFILE=VistaSP1x86

1. Identify Rogue processes - Process initially not part of ../baseline\_proc.txt
Commands used: 
$ volatility pslist
$ volatility pstree
$ volatility dlllist

Maxname seems to be 13 in length
Virtualbox: 
VBoxService.exe - 836
VBoxTray.exe	- 1816
FTK Imager.exe  - 2120  - 816

Other (significant?):
explorer.exe 	- 816

Rogue processes?:
xampp-control.e - 2768 	- 816
mysqld.exe 		- 2804  - 2768 (child of xampp)
httpd.exe 		- 2796 	- 2768
FileZillaServer - 2856	- 2768
httpd.exe 		- 2880 	- 2796 (child of httpd)

The above seem to not be windows native processes.

* Running through the processes to identify command (volatility dlllist):
$ while read -r line; do volatility dlllist -p $line; done < rogue.txt | grep -i "command line"

Where all interesting PID's are already in rogue.txt
Looking at the return the path seems to be the following:
> C:\xampp\\\{filezillaftp|apache|mysql|xampp-control.exe\}

Most likely looking at an FTP server dataleak or similar. // Speculation

2. Analyze Process Objects
Commands:
$ volatility dlllist 
$ volatility getsids
$ volatility modules

Starting out by identifying unique accounts.
$ volatility getsids | uniq -w 18
This shows e.g. multiple svchost.exe's running as NT Authority. Most rogue processes are also running as Administrator, where S-1-5-21 is related to a specific user.

Identifying all loaded DLL's (alternatively $(wc -l) for count):
$ volatility dlllist | grep "^0x" | cut -c 20-37,57- | sort | uniq -i > dll-baseline-1.lst
Shows 809 DLL's - These aren't all unique as it shows differnet processes using the same DLL.

Kernel module listing:
volatility dlllist | grep "^0x" | cut -c 33-37,57- | sort | uniq -i > module-base-1.lst
Shows 130 Kernel Modules.

### The Above hasn't been analyzed yet.
3. Review Network Artifacts
$ volatility netscan | cut -c 12-18,21-40,51-63,88-92,94-120 | uniq -w 20

4. Look for Evidence of Code Injection
5. Check for Signs of Rootkit
6. Dump Suspicious Processes and Drivers

# Author questions
1. What type of attacks has been performed on the box?
2. How many users has the attacker(s) added to the box, and how were they added?
3. What leftovers (files, tools, info, etc) did the attacker(s) leave behind? (assume our team arrived in time and the attacker(s) couldn’t clean and cover their tracks)
4. What software has been installed on the box, and were they installed by the attacker(s) or not?
5. Using memory forensics, can you identify the type of shellcode used?
6. What is the timeline analysis for all events that happened on the box?
7. What is your hypothesis for the case, and what is your approach in solving it?
8. Is there anything else you would like to add?


