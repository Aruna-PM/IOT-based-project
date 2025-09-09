#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>            // Install Library "Keypad" by Mark Stanley, Alexander
#include <Servo.h> // Include the Servo library

Servo myServo; // Create a Servo object

#define IRSensor 10 // Arduino
#define servo_pin 11  //PWM Pin on Arduino

LiquidCrystal_I2C lcd(0x27, 16, 2);  // Check your I2C address (can be 0x3F or 0x27)

const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns

char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {5, 4, 3}; //connect to the column pinouts of the keypad

//Create an object of keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

int show = 0;
int done=1;
int keyentry = 0;
int plastic=0;
String phoneNumber = "";
int pos = 0;

void setup() {
  Serial.begin(9600); // Baud rate must match the Python script
  myServo.attach(servo_pin); // Attach the servo to pin
  myServo.write(90); // Set the servo to the default position (90 degrees)
  
  lcd.init();         // Initialize the LCD
  //Lcd_Display("*** WELCOME ***",0,0,1,0,2000);

  Lcd_Display("Plastic Waste",0,0,1,0,0);
  Lcd_Display("Managemnt System",1,0,0,0,3000);

  Lcd_Display("Run App.py",0,0,1,0,0);
  Lcd_Display("Trying to Conect",1,0,0,1,5000);

  pinMode(IRSensor, INPUT); // IR Sensor pin INPUT

  String receivedData = Data_Received_From_Python_Wait();
  if (receivedData.equals("CONNECTED")) {
    Lcd_Display(receivedData,0,0,1,0,2000); // Print data on the first row of the LCD
  }
}

void loop() 
{
  //Lcd_Display("Plastic Waste",0,0,1,0,0);
  //Lcd_Display("Managemnt System",1,0,0,0,3000);

  if(!Get_IR_Status() && !show) // Object detected
  {
    // Send a message to Python
    Serial.println("Turn_ON_Camera");

    Lcd_Display("   WELCOME   ",0,0,1,0,1000);
    
    // Sending Command to ON Laptop Webcam
    Lcd_Display("Powering Webcam",0,0,1,0,0);
    Lcd_Display("Please Wait...",1,0,0,0,2000);

    String receivedData = Data_Received_From_Python_Wait();
      if (receivedData.equals("CAMERA_ON")) {
      Lcd_Display(receivedData,0,0,1,0,2000); // Print data on the first row of the LCD
    }
    Lcd_Display("Plz Show waste",0,0,1,0,0);
    Lcd_Display("into Camera",1,0,0,0,5000);
    show = 1;
  }

  if(show)
  {
    String receivedData = Data_Received_From_Python_Wait();
      if (receivedData.equals("Plastic")) {
      Lcd_Display(receivedData,0,0,1,0,2000); // Print data on the first row of the LCD
      plastic = 1;
    }
    else if(receivedData.equals("Non-Plastic")) {
      plastic = 0;
    }
    done = 1;
  }

  if(show && done && (keyentry!=1))
  {
    if(plastic)
    {
      myServo.write(0); // For Plastic
	    delay(3000);
	    myServo.write(90); // 90° Default
	  
	    Lcd_Display("Thank You !!",0,0,1,0,1000);
      Lcd_Display("Enter Phone No.",0,0,1,0,0);
      Lcd_Display("to get Reward.",1,0,0,0,1000);
      keyentry=1;
    }
    else
    {
      myServo.write(180); // For Non-Plastic
      delay(3000);
      myServo.write(90); // 90° Default
	  
      Lcd_Display("Thank You !!",0,0,1,0,2000);
      Lcd_Display("Collect Plastic",0,0,1,0,0);
      Lcd_Display("to get reward !!",1,0,0,0,2000);
      
      // Send a message to Python
      Serial.println("Thanks");
    }
  }

  if(keyentry==1)
  {
    //keyentry=0;
    //Lcd_Display("Enter Phone No.",0,0,1,0,0);
    show = 0;
    done=1;
    plastic=0;
    pos = 0;
    Keypad_LCD();

    if (keyentry == 2)
    {
      // Send a message to Python
      Serial.println(phoneNumber);
      phoneNumber = "";
    }
    String phoneNumber = "";
  }
  else
  {
    //Lcd_Scroll("Plastic Waste Management System",0,300);
    Lcd_Display("Please Stand ",0,0,1,0,0);
    Lcd_Display("infrnt of Sensor",1,0,0,0,2000);
    
    show = 0;
    done=1;
    keyentry = 0;
    plastic=0;
    phoneNumber = "";
    pos = 0;
  }
}

String Data_Received_From_Python_Wait() 
{
  while(1)
  {
    // Check if data is received from Python
    if (Serial.available() > 0) {
      String receivedData = Serial.readStringUntil('\n'); // Read until new line
      receivedData.trim(); // Remove any whitespace/newline characters from the beginning or end
      return receivedData;
    }
  }
}

int Get_IR_Status()
{ // Read pin status
  if(digitalRead(IRSensor))
    return 1;
  else
    return 0; 
}

void Lcd_Display(String message, int row, int col, boolean clear, boolean backlightoff, int delay_time)
{   
  if(clear)
    lcd.clear(); //Clear Full LCD Screen

  lcd.backlight();    // Turn on the LCD backlight

  lcd.setCursor(col,row);
  lcd.print(message);
  delay(delay_time);

  if(backlightoff)
    lcd.noBacklight(); // Turn off the LCD backlight
}

void Keypad_LCD()
{
  //Lcd_Display("waiting",0,0,1,0,2000);
  char key = keypad.getKey();
  //Lcd_Display("Done",0,0,1,0,2000);
    
  if (key) 
  {
    if (key == '#') 
    {
      // Submit phone number
      if (phoneNumber.length() == 10)
      {
        Lcd_Display("Submitted.",0,0,1,0,0);
        Lcd_Display("Thank You!!",1,0,0,0,1000);
        Lcd_Display("Check Reward at",0,0,1,0,0);
        Lcd_Display("www.MyReward.com",1,0,0,0,1000);

        keyentry=2;
      } 
      else 
      {
        Lcd_Display("Invalid Length!",0,0,1,0,0);
        Lcd_Display("Enter 10 Digits",1,0,0,0,2000);
        Lcd_Display("Enter Phone No:",0,0,1,0,0);

        phoneNumber = ""; // Reset for next entry
      }
      
    } 
    else if (key == '*') 
    {
      // Clear last character
      if (phoneNumber.length() > 0) 
      {
        phoneNumber.remove(phoneNumber.length() - 1);
        Lcd_Display("Phone No: ",0,0,1,0,0);
        Lcd_Display(phoneNumber,1,0,0,0,0);
      }
      else
      {
        Lcd_Display("Invalid Entry!",0,0,1,0,1000);
        Lcd_Display("Enter Phone No:",0,0,1,0,0);
      }
    } 
    else 
    { // Add digit to phone number if less than 10 digits
      if (phoneNumber.length() < 10) 
      {
        phoneNumber += key;
        Lcd_Display("Phone No: ",0,0,1,0,0);
        Lcd_Display(phoneNumber,1,0,0,0,0);
      }
    }
  }
  //delay(50);
}
