//Code to set up ESP8266 Webserver and basic framework from https://randomnerdtutorials.com/esp8266-web-server/
//detailed code breakdown of almost everything in loop() can be found there.
#include <Adafruit_NeoPixel.h>
#include <ESP8266WiFi.h>

//sets up the pixels strip
#define PIN 12
#define NUMPIXELS 600
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

//sets up wifi
const char* ssid     = "PlaceHolder";
const char* password = "PlaceHolder";

WiFiServer server(80); //opens up webserver on port 80

WiFiClient client = server.available();

String header;
String command; //creates command as a global variable, so that the light mode stays the same after it completes an command
int global_speed = 5;

void setup() {
  Serial.begin(115200);

  
  // configures the pixels strip
  pixels.begin();
  pixels.clear();
  pixels.show();
  pixels.setBrightness(50);


  //sets up wifi
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED ) {delay(500);} // forces the board to wait until the wifi is connected
  server.begin();  
}
void loop() {
  // put your main code here, to run repeatedly:
  WiFiClient client = server.available();
  if (client) {              
    String currentLine = "";
    int count=0;
    while (client.connected()) {
      Serial.println("a"); //used for debugging
      if (count >10) {break;}
      count +=1;
      if (client.available()){
        count=0;
        Serial.println("b");//used for debugging
        char c = client.read();
        header += c;
        if (c=='\n') 
        {
          if (currentLine.length()==0) 
          {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            client.println("<!DOCTYPE html><html>");
            if (header.indexOf("/com") >=0) 
            {
              command = header;//.substring(0,header.indexOf(" HTTP"));
              client.println(command);
              client.println();
            }
            else if (header.indexOf("/bright") >=0) 
            {
              int starting = header.indexOf("/bright")+8;
              int brightness = header.substring(starting,starting+3).toInt();
              if (brightness <=100) 
              {
                pixels.setBrightness(brightness);
                client.println("BRIGHTNESS OK, SET TO " + String(brightness));
              }
              else {client.println("BRIGHTNESS OUT OF RANGE. BRIGHTNESS REJECTED!");}
            }
            client.print("OK!");
            client.print("</html>");
            client.println();
            break;
            }
          else {currentLine="";}
        } 
        else if (c != '\r') {
          currentLine+=c;}
      }
    }
    header="";
    client.stop();
  }
 else {}
 if (command.indexOf("/rainbows") >=0) {rainbows();} 
 else if (command.indexOf("/rainbowcycle") >= 0) {rainbowCycle();}
 else if (command.indexOf("/christmas") >=0) {christmas1();}
 else if (command.indexOf("/improvedrainbow") >=0) {improvedRainbow();}
 else if (command.indexOf("/static" >= 0)) {//recieves in format of /static/rrrgggbbb
  int starting = command.indexOf("/static") + 8;
  int r = command.substring(starting,starting+3).toInt();
  int g = command.substring(starting+3,starting+6).toInt();
  int b = command.substring(starting+6,starting+9).toInt();
  staticColor(r,g,b);
  }
 
 //if (command.indexOf("GET /off") >=0) {pixels.clear();pixels.show();} //removed as you could just set the colors to 000000000
}
//below are the light functions:
//List of functions and purposes
// staticColor() takes an r g b value and sets the strip color to that value
// rainbows() moves the entire strip through a rainbow.
// rainbowCycle() moves the entire strip through a cycle of each color possible. takes the wait peramiter
// improvedRainbow() same concept as rainbowCycle but makes the colors look truer with wizardry and magic
// christmas1() alternates each light between red and green for 1 second. No peramiters.


//Sets the entire strip a single color
void staticColor(int r, int g, int b) {
  for (int i=0; i < NUMPIXELS; i++){
    pixels.setPixelColor(i,pixels.Color(r,g,b));
    }
    pixels.show();
  }

//rainbow method which moves the entire strip through a rainbow
void rainbows() {
  int wait = 100 / global_speed;
  for(long firstPixelHue = 0; firstPixelHue < 1*65536; firstPixelHue += 256) {
    for(int i=0; i<pixels.numPixels(); i++) {
      int pixelHue = firstPixelHue + (i * 65536L / pixels.numPixels());
      pixels.setPixelColor(i, pixels.gamma32(pixels.ColorHSV(pixelHue)));
    }
    pixels.show(); // Update strip with new contents
    delay(wait);  // Pause for a moment
  }
}

void rainbowCycle() { //cycles through every r g b color value in a rainbow effect. wait is time between changing colors
  int wait = global_speed;
  staticColor(255,0,0);
  for (int g=0; g < 255; g++) {staticColor(255,g,0); delay(wait); }
  for (int r=255; r >=0; r--) {staticColor(r,255,0); delay(wait); }
  for (int b=0; b < 255; b++) {staticColor(0,255,b); delay(wait); }
  for (int g=255; g >=0; g--) {staticColor(0,g,255); delay(wait); }
  for (int r=0; r < 255; r++) {staticColor(r,0,255); delay(wait); }
  for (int b=255; b >=0; b--) {staticColor(255,0,b); delay(wait); }
}

void improvedRainbow() { // From Adafruit's neopixel example guide
  int wait = 100/ global_speed;
  for(long pixelHue =0; pixelHue < 65536; pixelHue +=128) {
    pixels.fill(pixels.gamma32(pixels.ColorHSV(pixelHue)));
    pixels.show();
    delay(wait);
  }
}
void twoShift(int r1,int g1, int b1, int r2, int g2, int b2) {
  //WIP
  }

void christmas1() {
  int distance=3;
  int values[3][3] = {{255,0,0},{0,255,0},{255,255,255}};
  for (int times=0;times <3; times++) {
    int i=0;
    while (i <NUMPIXELS) {
        if ((i % (distance *3)) >=distance*6) {
          pixels.setPixelColor(i,values[times % 3][0],values[times % 3][1],values[times % 3][2]);}
        else if ((i % (distance *3)) >=distance*3) {
          pixels.setPixelColor(i,values[(times + 1) % 3][0],values[(times + 1) % 3][1],values[(times + 1) % 3][2]);}
        else if ((i % (distance *3)) >=0) {
          pixels.setPixelColor(i,values[(times+2) % 3][0],values[(times+2) % 3][1],values[(times+2) % 3][2]);}
      i++;
    }
    delay(1000);
  }
  pixels.show();
  }
