#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"
using namespace std::chrono;

Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
BufferedSerial pc(USBTX, USBRX); //tx,rx
BufferedSerial uart(D1, D0);     //tx,rx
BufferedSerial xbee(D10, D9);
BBCar car(pin5, pin6, servo_ticker);
DigitalInOut ping(D11);
Timer t;
float val;

int main()
{
    //while (1)
    //{
    //    xbee.write("K\r\n", 3);
    //    ThisThread::sleep_for(1s);
    //}
    uart.set_baud(9600);

    char buf[256], outbuf[256];
    FILE *devin = fdopen(&uart, "r");
    FILE *devout = fdopen(&uart, "w");
    while (1)
    {
        memset(buf, 0, 256);
        for (int i = 0;; i++)
        {
            char recv = fgetc(devin);
            printf("%c", recv);
            if (recv == '2')
            {
                xbee.write("too left!\r\n", 12);
            }
            else if (recv == '4')
            {
                xbee.write("great!\r\n", 9);
            }
            else if (recv == '6')
            {
                xbee.write("too right!\r\n", 13);
            }
            else if (recv == '\n')
            {
                printf("\r\n");
                break;
            }
            buf[i] = fputc(recv, devout);
        }
        RPC::call(buf, outbuf);
    }
}
