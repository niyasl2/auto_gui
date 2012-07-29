import os,sys,subprocess,re
ROUTE_DISPLAY = "route PRINT"
ue_addr_ipv4 = "172.22.1.100"
ROUTE_ADD = " route ADD 172.22.1.0 MASK 255.255.255.0 "
print "\nRouting packets"
print "Starting a subprocess to execute the command: %s" % ROUTE_DISPLAY
sys.stdout.flush()
p = subprocess.Popen(ROUTE_DISPLAY, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#print PipeFromCmd.read(-1)
l_split = [None]
# for line in p.stderr: ### RV - NOT WORKING ANYMORE ?????? -> DUE TO VPN and new network
    # print "Error:", line
for list in p.stdout:
    list_icera = re.search("NVIDIA", list)
    if list_icera != None:
        l_split = list.split()
        match = re.search(re.compile('([0-9]+)(\S+)'),l_split[0])
        if match:
            l_split[0] = match.group(1)
        print "The NVIDIA interface is", l_split[0]
        break
sys.stdout.flush()
# Check that the interface is found
if l_split[0] != None:
    # Add the interface identity to the command route
    cmd = ROUTE_ADD + ue_addr_ipv4  + " IF " + l_split[0]
    print "Starting a subprocess to execute the command: %s" % cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for line in p.stdout:
        print line
    for line in p.stderr:
        print "Error:", line