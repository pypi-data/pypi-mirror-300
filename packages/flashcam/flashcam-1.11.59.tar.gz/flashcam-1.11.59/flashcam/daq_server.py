#!/usr/bin/env python3
"""
240930 -  two streams (on port 5000 it can have independet labels via mqtt

watch -n 11 ' mosquitto_pub -t "flashcam_daq/widget1port5000" -m `awk "BEGIN { srand($RANDOM); print rand() * 3 }"`'
watch -n 30 ' mosquitto_pub -t "flashcam_daq/widget2port5000" -m `awk "BEGIN { srand($RANDOM); print rand() * 100 }"` '

I need to add UDP

"""

from fire import Fire
from flashcam.version import __version__
from flashcam.mmapwr import mmwrite # for daq
from console import fg, bg
import os
from flashcam import config
import time
import datetime as dt
#
import tdb_io.influx as influx
import sys
import signal
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import logging
import re
import json



logging.basicConfig(
    filename=os.path.expanduser("~/flashcam_daq.log"),
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,

)
logger = logging.getLogger(__name__)


"""
The idea is
 1/ to take care about PORTS and PIPES, accept just a number (ideally)
 2/ use cfg.json to understand the number
 3/  PIPE is defined HERE like /tmp/flashcam_fifo_x001 ....
"""

PRIMARY_PORT = None # on startup - port is correct, with load_config - can change
MAX_PORTS = 6 # this is UNO+Shield limit to plugin

def test():
    #cmd_ls( ip = ip,db = i['name'], series="all", qlimit = qlimit, output =output)
    if influx.check_port() :
        print("i... influx port present localy")
        commavalues = "a=1,b=2"
        influx.influxwrite( DATABASE="local", MEASUREMENT="flashcam",
                 values=commavalues,
                 IP="127.0.0.1"
                 )
    sys.exit(0)


def is_int(n):
    if str(n).find(".")>=0:  return False
    if n is None:return False
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n



import socket
import threading

def is_float(n):
    if n is None:return False
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


########################################################
#
#   recalculate if flashcam knows the calib system.... TEMP_phid HUMI_phid
#
######################################################3

def recalibrate(d, title ):
    """
    d comes as string BUT is sure it is a number; whatever happens, return rounded thing
    """
    res = d
    newtitle = title
    logger.info(f"D...RECAL  {d} ... {type(d)}   /{float(d)}/    /{title}/ ")
    print(f"D... Before : {d}  ->   /{float(d)}/    /{title}/ ")
    # *********************************
    if title.endswith("TEMP_phid"):
        res =  float(d) / 1024* 222.2 - 61.111
        if title != "TEMP_phid": newtitle = title.replace("TEMP_phid", "")
    # ************************************
    elif title.endswith("HUMI_phid"):
        res =  float(d) / 1024* 190.6 - 40.2
        if title != "HUMI_phid": newtitle = title.replace("HUMI_phid", "")
    # ********************************************************************** END
    else:
        res = d
    if len(str(round( float(res), 1))) < 4:
        res = round( float(res), 2)
    else:
        res = round( float(res), 1)
    print(f"D... After  :  {res}   {type(res)}  ")
    if newtitle[-1] == "_" and len(newtitle) > 2:
        newtitle = newtitle[:-1]
    logger.info(f"D...RECALfin  {res} ... {newtitle}")
    return res, newtitle


# #########################################################################
#
#                      Process DATA
#
#############################################################################
def process_data(data, index, CAM_PORT, OVR_LABEL=None):  #no OVR_LABEL!~!!!!
    """
    fit the incomming data into the format template
    AND - possibly recalculate raw data :)!
 "mminput1_cfg": "dial xxx;22;28;5;signal1",
 "mminput2_cfg": "dial xxx;22;28;5;dial2",
 "mminput3_cfg": "dial xxx;22;28;5;tacho3",
 "mminput4_cfg": "dial xxx;22;28;5;box4",
 "mminput5_cfg": "sub xxx;22;28;5;title5"

    """
    global PRIMARY_PORT
    # DATA ---------------------------
    d = None
    try:
        d = data.decode('utf8').strip()
    except:
        d = str(data).strip()
    print(f"i...  {bg.wheat}{fg.black}   receivd: /{d}/  on index /{index}/ CAMPORT={CAM_PORT} {bg.default}{fg.default}")
    #logger.info(f"D...  PDa receivd: /{d}/  on index {index} ")

    # without port - they are normal mminput1 and  mminput1_cfg # ************************
    item_file = f"mminput{index}"
    item_cfg = f"mminput{index}_cfg"
    if PRIMARY_PORT != CAM_PORT: # one more set of conncetors defined in config
        item_file = f"mminput{index+10}"
        item_cfg = f"mminput{index+10}_cfg"

    if not item_file in config.CONFIG:
        print(fg.red, f"X... MMAP file {index} - {item_file} not defined in {config.CONFIG['filename']}  ",  fg.default)
        return
    if not item_cfg in config.CONFIG:
        print(fg.red, f"X... template {index} - {item_cfg} not defined in {config.CONFIG['filename']}  ",  fg.default)
        return

    mmfile = config.CONFIG[ item_file ]
    mmtemplate = config.CONFIG[item_cfg ]

    # ------------------  MMAP file and TEMPLATE defined from here ======================================


    # prepare recalibration, you need to know title/label ....... Also - IF  number => write to INFLUX
    #
    if is_float(d) or is_int(d):
        # extract LABEL/TITLE that is crutial for recalibration
        mytitle = " ".join(mmtemplate.split(" ")[1:]).split(";")[4]

        #if OVR_LABEL is None: # MQTT  override label
        #    #  recalibrate by label
        d, newtitle= recalibrate( d, mytitle ) #  d goes as string returns as float
        #else:
        #    # no recal!
        #    d, newtitle= recalibrate( d, "placeholder" ) #  d goes as string returns as float

        #if OVR_LABEL is not None: newtitle = OVR_LABEL
        #mmtemplate = mmtemplate.replace(mytitle, newtitle ) # FIT THE DATA INTO THE FIELD

        mmtemplate = mmtemplate.replace("xxx", str(d) ) # FIT THE DATA INTO THE FIELD
        #print(f"DEBUG4 {d} ### {mmtemplate} ", flush=True)
        logger.info(f"D...  mmwrite: {mmtemplate}  ")
        # *******************
        mmwrite( mmtemplate, mmfile, debug=True, PORT_override=CAM_PORT )
        # *******************
        print(f"i... SUCCESS  MMWRITE ----- #{CAM_PORT}#  ", bg.white, fg.black, mmtemplate, fg.default, bg.default)

        if influx.check_port():
            #print("i... influx port present localy")
            #if OVR_LABEL is not None: #  override label
            #    commavalues = f"{OVR_LABEL}={d}"
            #else:
            commavalues = f"{mytitle}={d}"
                #if CAM_PORT != PRIMARY_PORT: # RECALIBRATION AND TRUNC Only for main port.....
                #    commavalues = f"{mytitle}_{CAM_PORT}={d}"
            try:
                influx.influxwrite( DATABASE="local",
                                    MEASUREMENT=f"flashcam{CAM_PORT}",
                                    values=commavalues,
                                    IP="127.0.0.1" )
                print(f"i... OK      WRITING  INFLUX => DB:flashcam{CAM_PORT}  ")
                logger.info(f"D...  PDa  InOK /{commavalues}/  on index {index} ")
            except:
                logger.info(f"D...  PDa  InXX /{commavalues}/  on index {index} ")
                print("X... ERROR  WRITING  INFLUX")

    else:# if not float.... make it a box and dont write INFLUX
        mmtemplate = mmtemplate.replace("xxx", d ) # FIT THE DATA INTO THE FIELD
        mmtemplate = mmtemplate.replace("signal", "box" )
        mmtemplate = mmtemplate.replace("dial", "box" )
        mmtemplate = mmtemplate.replace("tacho", "box" )
        logger.info(f"D...  MMAP  /{mmtemplate}/  on index {index} ")
        # *****************
        mmwrite( mmtemplate, mmfile, debug=False, PORT_override=CAM_PORT )#PRIMARY_PORT) # this is a uniquZ
        #
        print(f"i... SUCCESS  MMWRITE ----- #{CAM_PORT}# noINFLUX ", bg.white, fg.black, mmtemplate, fg.default, bg.default)
    print("_____________________________________", dt.datetime.now() )
    pass

############################################################3
#
#
#
#
##############################################################

def serve_port( PORT, TCP=True):  # ++++++++++++++++++++++++++++++++++++++++++++ THREAD
    """
    PORTS ********************************
    watch on PORT
    """
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    s = None
    if TCP:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ok = False
    try:
        s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
        ok = True
    except:
        print(f"X... {bg.orange}{fg.black} DaQ PORT NOT ALLOCATED {PORT} {bg.default}{fg.default} ")

    if not ok:
        try:
            time.sleep(6)
            if TCP:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
            ok = True
        except:
            print(f"X...   {bg.red} DaQ PORT NOT ALLOCATED {PORT} {bg.default} ")

    if not ok: return
    s.listen(5)
    print(f"i...   {bg.blue} Data Acquisition Server started on port {PORT} ;  TCP{TCP} / UDP{not TCP}  {bg.default}")
    while True:


        conn, addr = s.accept() # I hope this is waiting, else 12% of procssor taken by load_config
        with conn:
            data = conn.recv(1024)
            if data:
                config.load_config()
                print(f'i...  {fg.blue}port data Received: {data};  config reloaded{fg.default}')
                # create index in place ; communication port
                process_data(data, PORT - int(PRIMARY_PORT), CAM_PORT=int(PRIMARY_PORT) )


# ************************************************************************
#
# NAMED PIPES
#
# ************************************************************************

def watch_named_fifo(PORT, fifon = '/tmp/flashcam_fifo'):  # ++++++++++++++++++++++++++++++++++++++++++++THREAD
    """
    NAMED PIPES ************
    In client - use `os.path.exists` to check if the named pipe exists and `os.open` with `os.O_NONBLOCK` to check if it's open:
    """
    global PRIMARY_PORT
    fifoname = f"{fifon}_{PORT}"
    print(f"i...   {bg.darkgreen} Data Acquisition PIPE  started on {fifoname}   {bg.default}")
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)
    # Wait for the named pipe to be created
    #while not os.path.exists(fifo):
    #    time.sleep(1)
    with open(fifoname, 'r') as fifo_file:
        while True:
            data = fifo_file.readline().strip() # get what comes to PIPE
            if data:
                logger.info(f"*** fifo-readline data=={data} on PORT {PORT} ")
                print(f'i... {fg.green}named pipe Received: {data};  reloading config{fg.default}')
                config.load_config()
                #
                process_data(data, PORT - int(PRIMARY_PORT), CAM_PORT=int(PRIMARY_PORT) )
                time.sleep(0.1) # it runs all time.......
            else:
                time.sleep(0.1) # it runs all time.......





# ************************************************************************
#
#                                              MQTT --------------------
#
# ************************************************************************

def extract_numbers(s, topic="flashcam_daq"): # JUST widget and port
    #match = re.match(fr'^{topic}/widget(\d+)port(\d+)([A-Za-z]*)$', s)
    match = re.match(fr'^{topic}/widget(\d+)port(\d+)$', s)
    #print("D... ... matching ", match, s)
    if match:
        num1, num2 = match.groups()
        #print( match.groups() )
        return int(num1), int(num2) #, label if label else "dial"
    return None


# Define the callback for when a message is received
def mqtt_on_message(client, userdata, msg):
    global PRIMARY_PORT
    data = msg.payload.decode()
    #print(f"D... MQTT.Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    logger.info(f"*** mqtt         data=={data} on /{msg.topic}/ ")
    print(f"i... MQTT       {fg.violet}Received: {data};  on topic '{msg.topic}' rel-config {fg.default}")
    config.load_config()
    if msg.topic.find("flashcam_daq") >= 0:  # numbers for widget and port
        result = extract_numbers(msg.topic, topic="flashcam_daq")     #= 'flashcam_daq/widget3port5000'
        if result:
            widget, port = result
            #print(f"D....    processing widget {widget} to port {port}  ********************************************")
            process_data(data, widget, CAM_PORT=port )      #PORT - int(PRIMARY_PORT))
            pass
        else:
            print(f"X... {fg.red}MQTT Format is NOT widgetXportY {result}  {fg.default}")

    if msg.topic.find("flashcam_cmd") >= 0 and msg.topic.find("status") >= 0:  #  -------------- just get the number HARDCODED BELLOW
        ok = False
        try:
            data = int(data)
            ok = True
        except:
            ok = False
        if not ok: return
        # no help, no cmdline override....
        CAM_PORT = config.CONFIG['netport'] # always 8000
        CAM_PORT = 5000 # BAD THING, HARDCODED
        STARTUP_PORT = int(config.CONFIG['startupport']) # 0 ... original CONFG value is stored here OR ZERO if Gunicorn
        #if STARTUP_PORT != 0 and CURRENT_PORT != STARTUP_PORT:

        mmfile = f"{os.path.dirname(config.CONFIG['filename'])}/mmapfile"
        print(mmfile)
        print(f"i... {bg.white}{fg.black}MQTT from flashcam_cmd ==  {data}  {fg.default}{bg.default}")
        if data == 0:
            mmwrite( f"fixed_image BEAM_ON_.jpg", mmfile, debug=True, PORT_override=CAM_PORT )
        elif data == 1:
            mmwrite( f"fixed_image BEAM_OFF.jpg", mmfile, debug=True, PORT_override=CAM_PORT )
        elif data == 2:
            mmwrite( f"fixed_image DET_RDY_.jpg", mmfile, debug=True, PORT_override=CAM_PORT )
        elif data == 3:
            mmwrite( f"fixed_image DET_NRDY.jpg", mmfile, debug=True, PORT_override=CAM_PORT )


def mqtt_on_disconnect(client, userdata, rc):
    print("Disconnected. Attempting to reconnect...")
    try:
        client.reconnect()
    except Exception as e:
        print(f"Reconnection failed: {e}")


def watch_mqtt(POPO, MACHINE="127.0.0.1", PORT=1883):  # ++++++++++++++++++++++++++++++++++++++++++++THREAD
    """
    MQTT  ************

    """
    fifoname = f"notnow_{PORT}"
    print(f"i...   {bg.violet} Data Acquisition MQTT started on {fifoname}   {bg.default}")

    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the on_message callback
    client.on_message = mqtt_on_message
    client.on_disconnect = mqtt_on_disconnect

    # Connect to the broker
    client.connect( MACHINE, PORT, 60)

    # Subscribe to a topic  ---   standard flashcam AND +++   trick ++++ IMGSWITCH
    client.subscribe("flashcam_daq/#")
    print(f"i...   {bg.violet} ... subscribing  flashcam_daq/#   {bg.default}")
    client.subscribe("flashcam_cmd/#")
    print(f"i...   {bg.violet} ... subscribing  flashcam_cmd/#   {bg.default}")
    #client.subscribe("telemetrix/#")
    #client.subscribe("telemetix/temp2")

    # Start the loop to procss network traffic and dispatch callbacks
    client.loop_forever()



# ************************************************************************
#
#                                              8100 --------------------
#
# ************************************************************************

#================================================================== SERVER TCP/UDP/========start
def str_is_json(myjson):
    # print("D... my local jsontest:",myjson)
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        print("D... not loadable")
        return False
    return True


def watch_udp_8100():
    """
    echo "ahoj _p1=12_" | nc -u -w 1 127.0.0.1 8100"
    Q=`date +%s.%N` ;echo "merka0 _t=${Q}_p1=123" | nc -u -w 1 127.0.0.1 8100

    """
    UPORT = 8100 # decided long time ago
    print(f"i...   {bg.yellow} Multi-info One-line Acquisition UDP {UPORT}   {bg.default}")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ok = False
    try:
        s.bind(('0.0.0.0', UPORT))  #
        ok = True
    except:
        print(f"X... {bg.orange}{fg.black} UDP {UPORT}  PORT NOT ALLOCATED  {bg.default}{fg.default} ")
    if not ok:
        return
    #s.listen(5)
    print(f"i...   {bg.yellow} Multi-info Data Acquisition Server started on UDP port {UPORT} ;   {bg.default}")

    while True:
        data, address = s.recvfrom(4096)

        print(f" {data.decode('utf8')} from {address}")
        #if res.find("influxmevac ")==0:

        # ORIGINAL VADIM STRING **************************
        r = data.decode().split("influxmevac")[-1].strip()
        r = r.replace("    "," ")
        r = r.replace("   "," ")
        r = r.replace("  "," ")

        measu,*allrest = r.split(" ") # name of measurement - and split

        # the 1st thing in allrest is _
        allrest = "".join(allrest).strip().strip("_").split("_")
        print( fg.gray, "allrest==",allrest, fg.default )

        # results contain measurements fo VADIM
        res = '"fields":{'
        # JOIN ALL VALUES *****************  Joining and publishing  MQTT
        n_flds = 0
        for ar in allrest:
            skip = True
            try:
                var,val = ar.split("=")
                skip = False
            except:
                print(f"X... unable to split /{ar}/  ")
            try:
                res = f'{res}"{var}":{float(val)},'
                n_flds += 1
            except:
                print(f"X... {val} is not possible to interpres as float...")
                pass
            # PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH
            if not skip:
                print("i... publishing...", measu, var, val)
                if measu == "nfslv" and var == "status":
                    publish.single(f"flashcam_cmd/status", val, hostname="localhost") # PUBLISH; I see the whole process takes ~4-5ms
                else:
                    publish.single(f"{measu}/{var}", val, hostname="localhost") # PUBLISH; I see the whole takes ~4-5ms
                if influx.check_port():
                    commavalues = f"{var}={val}"
                    try:
                        influx.influxwrite( DATABASE="local",
                                            MEASUREMENT=f"flashcam_mqtt",
                                            values=commavalues,
                                            IP="127.0.0.1" )
                        print(f"i... OK      WRITING  INFLUX => DB:flashcam_mqtt  ")
                        logger.info(f"D... flashcam_mqtt:  /{commavalues}/  ")
                    except:
                        logger.info(f"X... flashcam_mqtt:  /{commavalues}/  ")
                        print("X... ERROR  WRITING  INFLUX")

        #     # print(f"i... {var} === {val}")
        # # REMOVE THE LAST COMMA
        # if n_flds < 1:
        #     print("X... NO VALUES TO WRITE TO INFLUX")
        # else:
        #     res=f'{res[:-1]}' + '}'
        #     res = 'influxme [{"measurement":"'+measu+'",'+res+'}]'
        #     # string
        #     r = res.split("influxme ")[-1].strip()
        #     print(f"D... {fg.grey}IFM: {r}{fg.default}" )
        #     #------ this is the last resort. Everything ends with list of dicts
        #     if str_is_json( r[1:-1] ): # check if in inner part of [] is json
        #         # print("D... GOOD , JSON inside")
        #         json_body=json.loads(r[1:-1])  # string loaded
        #         json_body=[json_body,]  # made list item
        #         # return this
        #         print("TO SEND2INFLUX", json_body )
        #     else:
        #         print("X...  NO JSON CREATED")
        #     # sendme=True
        time.sleep(0.01)

# ***************************************************
# ***************************************************
#
#                                               MAIN
#
# ***************************************************
# ***************************************************

def main():
    """
    I have :
    PORTS
    and
    NAMED PIPES
    and
    MQTT

    """
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    print()
    def signal_handler(sig, frame):
        print("Exiting with signal handler @bin...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


    # ***************************************************************** PORTS
    print("D... daq command - starting servers - start separatelly in FG")
    daq_threads = []
    for i in range(MAX_PORTS ):  # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1 #1-7  resp 8001-8007
        print(f"D...   starting server {i} - port {P} *****************")
        daq_threads.append( threading.Thread(
            target=serve_port,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads[i].start()

    #***************************************************************** PIPES
    print("D... daq command - starting PIPES - start separatelly in FG")
    daq_threads_FF = []
    for i in range(MAX_PORTS ): # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1
        print(f"D...   starting PIPE {i} - port {P} ********************")
        daq_threads_FF.append( threading.Thread(
            target=watch_named_fifo,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads_FF[i].start()

    #print(fg.violet) **************************************************MQTT
    mqtt_thread = threading.Thread(
        target=watch_mqtt,  args=( P, )  )
    mqtt_thread.start()

    print("****************************** all prepared ")

    #print(fg.violet) ************************************************** UDP 8100
    udp_thread = threading.Thread(
        target=watch_udp_8100,  args=(  )  )
    udp_thread.start()

    print("****************************** all prepared ")

    # ************************************************ JOIN ALL AT THE END
    for i in range(MAX_PORTS ): # 012345 for 6UNO
        daq_threads[i].join()
        daq_threads_FF[i].join()
        mqtt_thread.join()
    exit(0)

if __name__ == "__main__":
    Fire(test)
    Fire(main)
