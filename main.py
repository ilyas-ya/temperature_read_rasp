import Adafruit_DHT
import time
sensor = Adafruit_DHT.DHT11
DHT11_pin = 23

# Function for converting decimal to binary
def float_bin(my_number, places = 3):
    my_whole, my_dec = str(my_number).split(".")
    my_whole = int(my_whole)
    res = (str(bin(my_whole))+".").replace('0b','')
 
    for x in range(places):
        my_dec = str('0.')+str(my_dec)
        temp = '%1.20f' %(float(my_dec)*2)
        my_whole, my_dec = temp.split(".")
        res += my_whole
    return res
 
 
 
def IEEE754(n) :
    # identifying whether the number
    # is positive or negative
    sign = 0
    if n < 0 :
        sign = 1
        n = n * (-1)
    p = 30
    # convert float to binary
    dec = float_bin (n, places = p)
 
    dotPlace = dec.find('.')
    onePlace = dec.find('1')
    # finding the mantissa
    if onePlace > dotPlace:
        dec = dec.replace(".","")
        onePlace -= 1
        dotPlace -= 1
    elif onePlace < dotPlace:
        dec = dec.replace(".","")
        dotPlace -= 1
    mantissa = dec[onePlace+1:]
 
    # calculating the exponent(E)
    exponent = dotPlace - onePlace
    exponent_bits = exponent + 127
 
    # converting the exponent from
    # decimal to binary
    exponent_bits = bin(exponent_bits).replace("0b",'')
 
    mantissa = mantissa[0:23]
 
    # the IEEE754 notation in binary    
    final = str(sign) + exponent_bits.zfill(8) + mantissa
 
    # convert the binary to hexadecimal
    hstr = '%0*X' %((len(final) + 3) // 4, int(final, 2))
    a = '0x'+ hstr[0:2]
    b = '0x'+ hstr[2:4]
    c = '0x'+ hstr[4:6]
    d = '0x'+ hstr[6:8]
    
    return (a,b,c,d)

while True:

    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)
    if humidity is not None and temperature is not None:
        print('Temperature={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        with open('sensor.txt',"w") as myfile:
            for x in range(4):
                myfile.write(str(IEEE754(temperature)[x]) + '\n')

    else:
        ('Failed to get reading from the sensor. Try again!')
    time.sleep(1)
