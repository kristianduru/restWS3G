'''
SMS using AT Commands on 3G modem serial connection
RESTful Webservice 

'''

from flask import Flask, request
import serial
import time

app = Flask(__name__)


def sendSMS(message, recipient):
    SerialPort = serial.Serial("/dev/ttyUSB1",baudrate=9600,timeout=10)
    SerialPort.write('AT+CMGF=1\r')
    time.sleep(1)
    SerialPort.write('AT+CMGS="'+recipient+'"\r\n')
    time.sleep(1)
    SerialPort.write(message+"\x1A")
    time.sleep(1)
    SerialPort.close()

def getBalance():
    SerialPort = serial.Serial("/dev/ttyUSB1",baudrate=9600,timeout=10)
    SerialPort.write('AT+CUSD=1,"*111#",15\r')

    for count in range(1,7): # reads relevant num of lines
        balanceData = SerialPort.readline()
        if (balanceData.startswith('SALDO:')):
            balance = balanceData 
    
    SerialPort.close()

    return balance

@app.route("/sms/api/v1/send/<recipient>", methods=['POST'])
def send(recipient):
    message = request.form['message']
    sendSMS(message, recipient)

    sendFormLink = "<a href='/sms/api/v1/send/'>DEBUG SendForm</a>"
    return "Did sendSMS() here with message : %s  recipient %s <br><br> %s" % (message, recipient, sendFormLink)

@app.route("/sms/api/v1/balance")
def balance():
    return getBalance()


@app.route("/sms/api/v1/send/")
def sendForm():
    return '''
           DEBUG form action is /sms/api/v1/send/+467000000 which is the number to send to DEBUG
           <form action="/sms/api/v1/send/+4670000000" method="POST">
                 <p><input type=text name=message>
                 <p><input type=submit value=submit>
           </form>
           '''

if __name__ == "__main__":
    app.run(debug=True)
