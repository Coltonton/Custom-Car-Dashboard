#include <Arduino.h>
#include <EEPROM.h>
#include <Nextion.h>
#include "RTClib.h"
#include <Subbielib.h>
#include <SPI.h>
#include "mcp_can.h"
#include <mcp_can_dfs.h>

#include <Canbus.h>
#include <defaults.h>
#include <global.h>
#include <mcp2515.h>
#include <mcp2515_defs.h>

/* Notes
Possible bug in setings? set Day Brightness to 0?
intergrate a way to set cruise activatable off when in manual
[] Do Alerts
[] Finish Error Cruise
[] Finish Page Loops
[] Make Sure Checks are optimized
[] Add CAN
[] Clean Up & Orginize
[] Check Everything
[] Test
[] Find Whats wrong
[] Test
[] Find Whats wrong
[] Test
[] Find Whats wrong
[] Check Bugs 
[] Youre done!!!!
[] Now Work On Hardware & Install
[] Come Acrross Bugs
[] Squash Bugs
*/

//============================================================================================================================
//======Vars==================================================================================Vars============================
//============================================================================================================================
// EEPROM--------------------
int FuelAddr  = 0;
int HellaAddr = 5;
int TrainAddr = 10;
//int DistAddr  = 15;
int DayAddr = 20;
int NteAddr = 25;
//Vars-----------------------
int currentPage   = 0;
int lastPage      = 0;
int lastDrivePage = 0;
//CAN------------------------
const int spiCSPin = 53;
MCP_CAN CAN(spiCSPin);

//Pins-----------------------
int txnotifyPin   = 11;
int rxnotifyPin   = 12;

//Strings--------------------
String cmd;

//Brightness-----------------
uint32_t number   = 0;
char temp[10]     = {0};

//Error Page-----------------
int ErrorPage     = 0;

//Time-----------------------
RTC_PCF8523 rtc;

byte Hour = 0;
byte Minn = 0;
byte HourSett;
byte MinnSett;

//Settings
int newHella     = 5;
int newTrain     = 5;
int BrightVal    = 0;

//Code Vars
byte FuelVal;
byte HellVal;
byte TrainVal;
byte DayVal;
byte NteVal;
char currentGear  = 'P';
int Manual;
int ManualGear;
int MPH;
int Headlights    = 0;
int ErrorCount    = 0;
int Brakes;
int FollowingCar;
int CruiseActive;     //0/Off 1/Adaptive Active 2/Standard Active
int CruiseActivatable;
int StandardCruiseActive;
int StandardCruiseActivatable;
int CruiseSpeed;
int DistVal;
int ESError;
int Radar;
int IceWarning;
int BSML;
int BSMR;
int BSMOff;
int SRFOff;
int Gearable;
int ParkingBrake;

//CAN Vars

int CANFuel;
char CANcurrentGear  = 'P';
int CANManual;
int CANManualGear;
int CANMPH;
int CANHeadlights    = 0;
int CANErrorCount    = 0;
int CANBrakes;
int CANFollowingCar;
int CANCruiseActive;
int CANCruiseActivatable;
int CANStandardCruiseActive;
int CANStandardCruiseActivatable;
int CANCruiseSpeed;
int CANDistVal;
int CANESError;
int CANRadar;
int CANIceWarning;
int CANBSML;
int CANBSMR;
int CANBSMOff;
int CANSRFOff;
int CANGearable;
int CANParkingBrake;

int EyeSight  =  0;



//============================================================================================================================
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++Begin Code++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Begin Code++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//============================================================================================================================
void setup() {
  Serial.begin(9600);
  Serial3.begin(9600);
  nexInit();
  delay(2000);

  pinMode(txnotifyPin, OUTPUT);
  pinMode(rxnotifyPin, INPUT);



  //park 1
    Pb0.attachPop(Pb0PopCallback, &Pb0);
  //Main 2
  //Cruise 3
  //Error 4
  //About 5
    ABn0.attachPop(ABn0PopCallback, &ABn0);
    ABb0.attachPop(ABb0PopCallback, &ABb0);
    ABb1.attachPop(ABb1PopCallback, &ABb1);
    ABb2.attachPop(ABb2PopCallback, &ABb2);
    ABb3.attachPop(ABb3PopCallback, &ABb3);
  //Menu 13
    MEb0.attachPop(MEb0PopCallback, &MEb0);
    MEb1.attachPop(MEb1PopCallback, &MEb1);
    MEb2.attachPop(MEb2PopCallback, &MEb2);
    MEb3.attachPop(MEb3PopCallback, &MEb3);
    MEb4.attachPop(MEb4PopCallback, &MEb4);
    MEb5.attachPop(MEb5PopCallback, &MEb5);
  //POPO 14
  //Gauges 15
  //Error Menu 16
    ERb0.attachPop(ERb0PopCallback, &ERb0);
    ERq4.attachPop(ERq4PopCallback, &ERq4);
    ERq5.attachPop(ERq5PopCallback, &ERq5);
  //OBDII 17
    OBb0.attachPop(OBb0PopCallback, &OBb0);
    OBb1.attachPop(OBb1PopCallback, &OBb1);
  //Arduino Settings 18
    ASb0.attachPop(ASb0PopCallback, &ASb0);
    ASb1.attachPop(ASb1PopCallback, &ASb1);
    ASb2.attachPop(ASb2PopCallback, &ASb2);
    ASb3.attachPop(ASb3PopCallback, &ASb3);
    ASb4.attachPop(ASb4PopCallback, &ASb4);
    ASb5.attachPop(ASb5PopCallback, &ASb5);
    ASb6.attachPop(ASb6PopCallback, &ASb6);
    ASb7.attachPop(ASb7PopCallback, &ASb7);
    ASb8.attachPop(ASb8PopCallback, &ASb8);
    ASb9.attachPop(ASb9PopCallback, &ASb9);
    ASb10.attachPop(ASb10PopCallback, &ASb10);
  //Nextion Settings 19
    NSb0.attachPop(NSb0PopCallback, &NSb0);
    NSb1.attachPop(NSb1PopCallback, &NSb1);
    NSb2.attachPop(NSb2PopCallback, &NSb2);
  //Speed 20
    Sn2.attachPop(Sn2PopCallback, &Sn2);
  //Drawing  21
    DRb0.attachPop(DRb0PopCallback, &DRb0);
  //Credits  22
    CRb0.attachPop(CRb0PopCallback, &CRb0);

  //CheckCAN
  if /*while*/ (CAN_OK != CAN.begin(CAN_500KBPS)) { //Dont Forget To Revert
    Serial.println("CAN BUS Init Failed");
    delay(100);
  }
  Serial.println("CAN BUS  Init OK!");

  //Start Boot
  FuelVal  = EEPROM.read(FuelAddr);
  HellVal = EEPROM.read(HellaAddr);
  TrainVal = EEPROM.read(TrainAddr);
  DayVal   = EEPROM.read(DayAddr);
  NteVal   = EEPROM.read(NteAddr);
  Serial.println("Fuel = ");
  Serial.println(FuelVal, DEC);
  Serial.println("Hella = ");
  Serial.println(HellVal, DEC);
  Serial.println("Train = ");
  Serial.println(TrainVal, DEC);
  Serial.println("Day Brightness = ");
  Serial.println(DayVal, DEC);
  Serial.println("Night Brightness = ");
  Serial.println(NteVal, DEC);
  //EEPROM.write(DayAddr, 100);
  //                      Y   M  D      H        M      S
  //rtc.adjust(DateTime(2019, 4, 2, 11, 59, 0));

  TimeInt();
  PBoot();
}

void loop() {
  if (currentPage == 1) {
    PPark();
  }
  else if (currentPage == 2) {
    PMain();
  }
  else if (currentPage == 3) {
    PCruise();
  }
  else if (currentPage == 4) {
    PESError();
  }
  else
  {
    CheckGear();
  }
}

//============================================================================================================================
//--Sub Loops=================================================================================Sub Loops=======================
//============================================================================================================================
void PBoot() {    //0
  B.show();
  TimeInt();
  SetBrightness(); 
  currentPage = 0;
  lastPage = 0;
  
  delay(100);
  Bvar1.setValue(FuelVal);
  Bvar5.setValue(HellVal);
  Bvar6.setValue(TrainVal);
  Bvar11.setValue(DistVal);
  delay(6000);
 
  P.show();
  UpdateTime();
  lastDrivePage = 1;
  currentPage = 1;
  lastPage = 0;
  loop();
}

void PPark(){     //1 
  CheckPPark();
  nexLoop(nex_listen_list1);
  PPark();
}

void PMain(){     //2
  currentPage = 2;
  CheckPMain();
}

void PCruise(){   //3
  currentPage = 3;
  CheckPCruise();
}

void PESError(){    //4
  currentPage = 4;
  CheckPESError();
}

void PAbout(){    //5
  nexLoop(nex_listen_list5);
  CheckTime();
  if (currentPage == 5){
    delay(100);
    PAbout();
  }
  else if (currentPage != 5){
    /* code */
  }
}

void PWarning(){  //6  //Todo
  //Code Here
}

//                //7-12 NA

void PMenu(){     //13
  nexLoop(nex_listen_list5);
  delay(100);
  PMenu();
}

void PPopo(){     //14
  //Code Here
}

void PGauge(){    //15  //Todo
  // put your code here
}

void PErrorMenu(){//16
  nexLoop(nex_listen_list5);
  delay(100);
  PErrorMenu();
}

void PObd(){      //17
  nexLoop(nex_listen_list5);
  delay(100);
  PObd();
}

void PArduino(){  //18
  nexLoop(nex_listen_list5);
  delay(100);
  PArduino();
}

void PNexSett(){  //19
  nexLoop(nex_listen_list5);
  NSh0.getValue(&number);
  delay(250);
  PNexSett();
}

void PSpeed(){    //20  //Todo
  nexLoop(nex_listen_list5);
  delay(100);
  PSpeed();
}

void PDrawing(){  //21
  nexLoop(nex_listen_list5);
  delay(100);
  PDrawing();
}

void PCredits(){  //22
  nexLoop(nex_listen_list5);
  delay(100);
  PCredits();
}


//============================================================================================================================
//--Callbacks=================================================================================Callbacks=======================
//============================================================================================================================
//Page Park (1)---------------------------------------Page Park (1)
void Pb0PopCallback(void *ptr){   //About
  Serial.println("Pressed Park B0 (About)");
  lastPage = 1;
  currentPage = 5;
  PAbout();
}

//Page Main (2)---------------------------------------Page Main (2)

//Page Cruise (3)-------------------------------------Page Cruise (3)

//Page ESError (4)------------------------------------Page ESError

//Page About (5)--------------------------------------Page About (5)
void ABn0PopCallback(void *ptr){  //Speed
  Serial.println("Pressed About N0 (Speed)");
  lastPage  = 5;
  PSpeed();
}
void ABb0PopCallback(void *ptr){  //Menu
  Serial.println("Pressed About B0 (menu)");
  lastPage  = 5;
  PMenu();
}
void ABb1PopCallback(void *ptr){  //Drawing
  Serial.println("Pressed About B1 (Drawing)");
  lastPage  = 5;
  PDrawing();
}
void ABb2PopCallback(void *ptr){  //Credits
  Serial.println("Pressed About B2 (Credits)");
  lastPage  = 5;
  PCredits();
}
void ABb3PopCallback(void *ptr){  //Back
  Serial.println("Pressed About B3 (Going Back to ");
  if (lastDrivePage == 1) {
    Serial.print("Park)");
    lastDrivePage = 1;
    currentPage = 1;
    lastPage  = 5;
    UpdateTime();
    PPark();
  }
  else if (lastDrivePage == 2) {
    Serial.print("Main)");
    lastDrivePage = 2;
    currentPage = 2;
    lastPage  = 5;
    PMain();
    UpdateTime();
  }
  else if (lastDrivePage == 3) {
    Serial.print("Cruise)");
    lastDrivePage = 3;
    currentPage = 3;
    lastPage  = 5;
    PCruise();
    UpdateTime();
  }
  else if (lastDrivePage == 4) {
    Serial.print("Error)");
    lastDrivePage = 4;
    currentPage = 4;
    lastPage  = 5;
    PESError();
    UpdateTime();
  }
}

//Page Menu (14)--------------------------------------Page Menu (14)
void MEb0PopCallback(void *ptr){  //Back
  Serial.println("Pressed Menu B0 (Going Back to ");
  if (lastDrivePage == 1)
  {
    Serial.print("Park)");
    lastDrivePage = 1;
    currentPage = 1;
    lastPage  = 5;
    PPark();
  }
  else if (lastDrivePage == 2)
  {
    Serial.print("Main)");
    lastDrivePage = 2;
    currentPage = 2;
    lastPage  = 5;
    PMain();
  }
  else if (lastDrivePage == 3)
  {
    Serial.print("Cruise)");
    lastDrivePage = 3;
    currentPage = 3;
    lastPage  = 5;
    PCruise();
  }
  else if (lastDrivePage == 4)
  {
    Serial.print("Error)");
    lastDrivePage = 4;
    currentPage = 4;
    lastPage  = 5;
    PESError();
  }
}
void MEb1PopCallback(void *ptr){  //Errors
  Serial.println ("Going To Errors Menu");
  ShowNextErrors();
  PESError();
}
void MEb2PopCallback(void *ptr){  //Gauges
  Serial.println ("Going To Gauges");
  PGauge();
}
void MEb3PopCallback(void *ptr){  //OBD
  Serial.println ("Going To OBDII Menu");
  PObd();
}
void MEb4PopCallback(void *ptr){  //Arduino
  Serial.println ("Going To Arduino Settings");
  DateTime now = rtc.now();
  ASn0.setValue(now.hour());
  HourSett = now.hour();
  ASn1.setValue(now.minute());
  MinnSett = now.minute();
  ASvar4.setValue(HourSett);
  ASvar5.setValue(MinnSett);
  if (TrainVal == 1){
    ASb1.Set_background_color_bco(63488); //On Selected
    ASb2.Set_background_color_bco(31);    //Off Off
  }
  if (HellVal >> 0){
    if (HellVal == 1){
      ASb3.Set_background_color_bco(31);
      ASb4.Set_background_color_bco(63488);
    }
    else if (HellVal == 2){
      ASb3.Set_background_color_bco(31);
      ASb5.Set_background_color_bco(63488);
    }
    
    
  }
  else{
    /* code */
  }
  PArduino();
}
void MEb5PopCallback(void *ptr){  //NexSett
  Serial.println ("Going To Nextion Settings");
  if (Headlights == 0){
    NSh0.setValue(DayVal);
  }
  else{
    NSh0.setValue(NteVal);
  }
  PNexSett();
}

//Page Gauges (15)------------------------------------Page Gauges (15) //todo

//Page Error Menu (16)--------------------------------Page Error Menu (16)
void ERb0PopCallback(void *ptr){  //Back
  Serial.println("Going Back To Menu From Error Menu");
  PMenu();
}
void ERq4PopCallback(void *ptr){  //Page +
  ErrorPage --;
  Serial.println("Going Back A Page = ");
  Serial.println(ErrorPage);
}
void ERq5PopCallback(void *ptr){  //Page -
  ErrorPage ++;
  Serial.println("Going Forward A Page = ");
  Serial.println(ErrorPage);
}

//Page OBD (17)---------------------------------------Page OBD (17)
void OBb0PopCallback(void *ptr){  //Back
  Serial.println("Going Back To Menu From OBDII");
  PMenu();
}
void OBb1PopCallback(void *ptr){  //Add OBDII Clear Func
  Serial.println("Clearing Codes!");
}

//Page Arduino (18)-----------------------------------Page Arduino (18)
void ASb0PopCallback(void *ptr){  //Back           
  Serial.println("Going Back To Menu From Arduino Settings");
  if (newTrain != 5 || newHella != 5) {
    ArdSend();
    ArdSaveT();
    ArdSaveH();
    newTrain = 5;
    newHella = 5;
  }
  else{
    /* code */
  }
  PMenu();
}
void ASb1PopCallback(void *ptr){  //Train Horn On
  Serial.println("Train Horn set to On");
  newTrain = 1;
}
void ASb2PopCallback(void *ptr){  //Train Horn Off
  Serial.println("Train Horn set to Off");
  newTrain = 0;
}
void ASb3PopCallback(void *ptr){  //Hella Off
  Serial.println("Hella Lights Off");
  newHella = 0;
}
void ASb4PopCallback(void *ptr){  //Hella Auto
  Serial.println("Hella Lights Auto");
  newHella = 1;
}
void ASb5PopCallback(void *ptr){  //Hella On
  Serial.println("Hella Lights On Untill Restart");
  newHella = 2;
}
void ASb6PopCallback(void *ptr){  //Hour+
  HourSett ++;
 
  if (HourSett >= 24)
  {
    HourSett = 0;
  }
  Serial.println("Hout +");
  Serial.println(HourSett);
}
void ASb7PopCallback(void *ptr){  //Hour-
  HourSett -= 1;
  if (HourSett == 255)
  {
    Serial.println("restart");
    HourSett = 23;
  }
  Serial.println("Hout -");
  Serial.println(HourSett);
}
void ASb8PopCallback(void *ptr){  //Min+
  MinnSett ++;
  if (MinnSett >= 60)
  {
    MinnSett = 0;
  }
  Serial.println("Minn +");
  Serial.println(MinnSett);
}
void ASb9PopCallback(void *ptr){  //Min-
  MinnSett --;
  if (MinnSett == 255)
  {
    MinnSett = 59;
  }
  Serial.println("Minn -");
  Serial.println(MinnSett);
}
void ASb10PopCallback(void *ptr){ //Set
  //                      Y   M  D      H        M      S
  rtc.adjust(DateTime(2019, 4, 2, HourSett, MinnSett, 0));
  Serial.println("Set Time");
}


//Page Next Sett(19)----------------------------------Page Next Sett(19)
void NSb0PopCallback(void *ptr){  //Back
  Serial.println("Going Back To Menu From Nextion Settings");
  SaveBrightness();
  PMenu();
}
void NSb1PopCallback(void *ptr){  //Restart
  Serial.println("Restarting");
  SaveBrightness();
  currentPage   = 0;
  lastDrivePage = 0;
  lastPage      = 0;
  currentGear   = 'P';
  PBoot();
}
void NSb2PopCallback(void *ptr){  //Recal
  Serial.println("Recal In Process Please Complete In 40 Seconds!!");
  SaveBrightness();
  delay(40000);
  currentPage   = 0;
  lastDrivePage = 0;
  lastPage      = 0;
  currentGear   = 'P';
  PBoot();
}

//Page Speed (20)-------------------------------------Page Speed (20)
void Sn2PopCallback(void *ptr){   //Back
  Serial.println("Going Back To About Form Speed Only");
  PMenu();
}
//Page Drawing (21)-----------------------------------Page Drawing (21)
void DRb0PopCallback(void *ptr){  //Back
  Serial.println ("Going Back To About From Drawing");
  PAbout();
}

//Page Credits (22)-----------------------------------Page Credits (22)
void CRb0PopCallback(void *ptr){  //Back
  Serial.println ("Going Back To About From Credits");
  PAbout();
}

//============================================================================================================================
//===Functions================================================================================Functions=======================
//============================================================================================================================
//---Brightness------------------------------------------------------
void SaveBrightness(){    //Save Brightness Setting
  NSh0.getValue(&number);
  if (number != DayVal && Headlights == 0)
  {
    Serial.println("Brightness = ");
    Serial.println(number);
    Serial.println(" /Day");
    DayVal = number;
    EEPROM.write(DayAddr, DayVal);
  }

  else if (number != NteVal && Headlights == 1)
  {
    Serial.println("Brightness = ");
    Serial.println(number);
    Serial.println(" /Night");
    NteVal = number;
    EEPROM.write(NteAddr, NteVal);
  }
  else
  {
    /* return */
  }
}
void SetBrightness(){     //Set Brightness
  if (Headlights == 0) {
    Serial.println("Changing To Day Bright!");
    
    cmd += "dim=";
    cmd += DayVal;
    SndCmd(); 
    cmd.remove(7);
  }
  else if (Headlights == 1) {
    Serial.println("Changing To Night Bright!");

    cmd += "dim=";
    cmd += NteVal;
    SndCmd();
    cmd.remove(7);
  }
}

//---Time------------------------------------------------------------
void TimeInt(){           //Start RTC
  Serial.println("Time Int");
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  if (! rtc.initialized()) {
    Serial.println("RTC is NOT running!, Setting AutoMagicly");
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // January 21, 2014 at 3am you would call:
    //rtc.adjust(DateTime(2014, 1, 21, 11, 59, 0));
  }
}
void UpdateTime(){        //Update Time On Screen Anywhere
  DateTime now = rtc.now();
  Hour = now.hour();
  Minn = now.minute();
  if (Hour > 12){
    Hour -= 12;
    Serial2.print("n4.val=");
    Serial2.print(Hour);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial.println(" ");
    Serial.print("n4.val=");
    Serial.print(Hour);

    Serial2.print("n5.val=");
    Serial2.print(Minn);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial.println(" ");
    Serial.print("n5.val=");
    Serial.print(Minn);
  }
  else if (Hour == 0){
    Hour = 12;
    Serial2.print("n4.val=");
    Serial2.print(Hour);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial.println(" ");
    Serial.print("n4.val=");
    Serial.print(Hour);

    Serial2.print("n5.val=");
    Serial2.print(Minn);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial.println(" ");
    Serial.print("n5.val=");
    Serial.print(Minn);
  }
  else{
    Serial2.print("n4.val=");
    Serial2.print(Hour);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial.println(" ");
    Serial.print("n4.val=");
    Serial.print(Hour);

    Serial2.print("n5.val=");
    Serial2.print(Minn);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial2.write(0xff);
    Serial.println(" ");
    Serial.print("n5.val=");
    Serial.print(Minn);
  }
}

//---Nxt Errors------------------------------------------------------
void ShowNextErrors(){    //Show Proper Elements For Errors
  

  if (ErrorCount == 1) {
    Serial.println("1");
    Serial2.print("vis q0,1"); //Box1
    SndNxt();
    Serial2.print("vis t0,1"); //Box1 txt
    SndNxt();
  }
  else if (ErrorCount == 2) {
    Serial.println("2");
    Serial2.print("vis q0,1"); //Box1
    SndNxt();
    Serial2.print("vis t0,1"); //Box1 txt
    SndNxt();
    Serial2.print("vis q1,1"); //Box2
    SndNxt();
    Serial2.print("vis t1,1"); //Box2 txt
    SndNxt();
  }
  else if (ErrorCount == 3) {
    Serial.println("3");
    Serial2.print("vis q0,1"); //Box1
    SndNxt();
    Serial2.print("vis t0,1"); //Box1 txt
    SndNxt();
    Serial2.print("vis q1,1"); //Box2
    SndNxt();
    Serial2.print("vis t1,1"); //Box2 txt
    SndNxt();
    Serial2.print("vis q2,1"); //Box3
    SndNxt();
    Serial2.print("vis t2,1"); //Box3 txt
    SndNxt();
  }
  else if (ErrorCount == 4) {
    Serial.println("4");
    Serial2.print("vis q0,1"); //Box1
    SndNxt();
    Serial2.print("vis t0,1"); //Box1 txt
    SndNxt();
    Serial2.print("vis q1,1"); //Box2
    SndNxt();
    Serial2.print("vis t1,1"); //Box2 txt
    SndNxt();
    Serial2.print("vis q2,1"); //Box3
    SndNxt();
    Serial2.print("vis t2,1"); //Box3 txt
    SndNxt();
    Serial2.print("vis q3,1"); //Box4
    SndNxt();
    Serial2.print("vis t3,1"); //Box4 txt
    SndNxt();
  }

}

//---Ard Settings----------------------------------------------------
void ArdSend(){           //Send Carduino Data
  Serial.println("Waiting To Send Data To Carduino");
  digitalWrite(txnotifyPin, HIGH);
  delay(250);
  if (digitalRead(rxnotifyPin) == HIGH) {
    Serial.println(newTrain);
    Serial.println(newHella);
    Serial3.print(newTrain);
    Serial3.print(newHella);
    ArdSent();
  }
  else if (digitalRead(rxnotifyPin) == LOW)
  { 
    ArdSend();
  }
}
void ArdSent(){           //Wait For Command Recived
  if (digitalRead(rxnotifyPin) == LOW)
  {
    Serial.println("Comands Recived");
  }
  else if (digitalRead(rxnotifyPin) == HIGH)
  {
    Serial.println("Waiting For Command Comformation");
    delay(250);
    digitalWrite(txnotifyPin, LOW);
    ArdSent();
  } 
}
void ArdSaveT(){          //Save new Train Horn val
  if (newTrain < 5)
  {
    TrainVal = newTrain;
    EEPROM.write(TrainAddr, TrainVal);
    Serial.println("Wrote ");
    Serial.println(TrainVal);
    Serial.println("To EEPROM Train");
    //Serial3.println
    newTrain = 5;
  }
  else {
    Serial.println("No Change!");
  }
  
}
void ArdSaveH(){          //Save New Hella Value
  if (newHella < 5)
  {
    HellVal = newHella;
    EEPROM.write(HellaAddr, HellVal);
    Serial.println("Wrote ");
    Serial.println(HellVal);
    Serial.println("To EEPROM Hella");
    newHella = 5;
  }
   else {
    Serial.println("No Change!");
  }
}

//---Nxt Serial Commands---------------------------------------------
void SndCmd(){            //Send String Command
  Serial.println(cmd);
  Serial2.print(cmd);
  Serial2.write(0xff);
  Serial2.write(0xff);
  Serial2.write(0xff);
}
void SndNxt(){            //Send Nextion End Comm Bytes
  Serial2.write(0xff);
  Serial2.write(0xff);
  Serial2.write(0xff);
}

//--NEXUI------------------------------------------------------------
void SetFuel(){
  FuelVal = CANFuel;
  Serial2.print("va1.val=");
  Serial2.print(FuelVal);
  SndNxt();
  Serial2.print("n1.val=");
  Serial2.print(FuelVal);
  SndNxt();
  if (FuelVal <= 25){
    Serial2.print("n1.pco=64577");
    SndNxt();
    Serial2.print("vis q6,1");
    SndNxt();
  }
  else{
    Serial2.print("n1.pco=33808");
    SndNxt();
    Serial2.print("vis q6,0");
    SndNxt();
  }
  EEPROM.update(FuelAddr, FuelVal);
}
void SetPOPO(){
  if (Radar == 1){
    Serial2.print("vis q3,1");
    SndNxt();
    delay(50);
    Serial2.print("vis q4,0");
    SndNxt();
  }
  else if (Radar == 2){
    Serial2.print("vis q3,0");
    SndNxt();
    delay(50);
    Serial2.print("vis q4,1");
    SndNxt();
  }
  else{
    Serial2.print("vis q3,0");
    SndNxt();
    delay(50);
    Serial2.print("vis q4,0");
    SndNxt();
  }
  
  
}
void SetIce(){
  if (IceWarning == 1)
  {
    Serial2.print("vis q5,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q5,0");
    SndNxt();
  }
  
  
}
void SetSpeed(){
  Serial2.print("n0.val=");
  Serial2.write(MPH);
  SndNxt();
}
void SetGear(){
  Serial2.print("t0.txt=");
  Serial2.write(currentGear);
  SndNxt();
}
void SetManualGear(){
  if (currentPage == 2 || currentPage == 4) {
    Serial2.print("t0.txt=");
    Serial2.write(ManualGear);
    SndNxt();
  }
  else if (currentPage == 1 || currentPage == 3) {
    if (currentPage == 1) {
      M.show();
      currentPage = 2;
      lastDrivePage = 1;
      delay(100);
      Serial2.print("t0.txt=");
      Serial2.write(ManualGear);
      SndNxt();
      loop();
    }
    if (currentPage == 3) {
      M.show();
      currentPage = 2;
      lastDrivePage = 3;
      CruiseActive = 0;
      delay(100);
      Serial2.print("t0.txt=");
      Serial2.write(ManualGear);
      SndNxt();
      loop();
    }
  }
}
void SetGearStuff(){
  if (currentGear == 'P' && (CANcurrentGear == 'R' || CANcurrentGear == 'N' || CANcurrentGear == 'D')) {//See If Put Into Gear
    currentGear = CANcurrentGear;
    if (EyeSight == 0) {
      M.show();
      delay(100);
      SetGear();
      currentPage = 2;
      lastDrivePage = 1;
      loop();
      }
    else {
      I.show();
      delay(100);
      SetGear();
      currentPage = 4;
      lastDrivePage = 1;
      loop();
    }
  }
  else if (CANcurrentGear == 'P' && (currentGear == 'D' || currentGear == 'N' || currentGear == 'R')) { //See If In Park From Drive Gears
    currentGear = CANcurrentGear;
    P.show();
    currentPage = 1;
    if (EyeSight == 0) {
      lastDrivePage = 2;
    }
    else {
      lastDrivePage = 4;
    }
    loop();
  }
  else {
    //No Change
  }
}
void SetCruiseSpeed(){
  Serial2.print("n2.val=");
  Serial2.print(CruiseSpeed);
  SndNxt();
}
void SetCruiseDist(){
  if (DistVal == 1) {
  Serial2.print("vis q23,1");
  SndNxt();
  Serial2.print("vis q24,0");
  SndNxt();
  Serial2.print("vis q25,0");
  SndNxt();
  Serial2.print("vis q26,0");
  SndNxt();
  }
  else if (DistVal == 2) {
    Serial2.print("vis q23,1");
    SndNxt();
    Serial2.print("vis q24,1");
    SndNxt();
    Serial2.print("vis q25,0");
    SndNxt();
    Serial2.print("vis q26,0");
    SndNxt();
  }
  else if (DistVal == 3)
  {
    Serial2.print("vis q23,1");
    SndNxt();
    Serial2.print("vis q24,1");
    SndNxt();
    Serial2.print("vis q25,1");
    SndNxt();
    Serial2.print("vis q26,0");
    SndNxt();
  }
  else if (DistVal == 4)
  {
    Serial2.print("vis q23,1");
    SndNxt();
    Serial2.print("vis q24,1");
    SndNxt();
    Serial2.print("vis q25,1");
    SndNxt();
    Serial2.print("vis q26,1");
    SndNxt();
  }
}
void SetStandardCruiseActivatable(){
  if (CruiseActivatable = 1) {
    Serial2.print("vis q7,1");
    SndNxt();
    Serial2.print("vis q8,1");
    SndNxt();
    Serial2.print("vis n2,1");
    SndNxt();
    Serial2.print("n2.val=");
    Serial2.print(CruiseSpeed);
    SndNxt();
  }
  else {
    Serial2.print("vis q7,0");
    SndNxt();
    Serial2.print("vis q8,0");
    SndNxt();
    Serial2.print("vis n2,0");
    SndNxt();
  }
}
void SetCruiseActivatable(){
  if (CruiseActivatable = 1)
  {
    Serial2.print("vis q7,1");
    SndNxt();
    Serial2.print("vis q8,1");
    SndNxt();
    Serial2.print("vis n2,1");
    SndNxt();
    Serial2.print("n2.val=");
    Serial2.print(CruiseSpeed);
    SndNxt();
  }
  else;
  {
    Serial2.print("vis q7,0");
    SndNxt();
    Serial2.print("vis q8,0");
    SndNxt();
    Serial2.print("vis n2,0");
    SndNxt();
  }
}
void SetFollowingCar(){
  if (FollowingCar == 1)
  {
    Serial2.print("vis q11,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q11,0");
    SndNxt();
  }
}
void SetHeadlights(){
  if (Headlights == 1)
  {
    Serial2.print("vis q22,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q22,0");
    SndNxt();
  }
}
void SetBrakes(){
  if (Brakes == 1)
  {
    Serial2.print("vis q15,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q15,0");
    SndNxt();
  }
}
void SetBSDL(){
  if (BSML == 1)
  {
    Serial2.print("vis q14,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q14,0");
    SndNxt();
  }
}
void SetWarning(){
  if (ErrorCount >> 0)
  {
    Serial2.print("vis q13,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q13,0");
    SndNxt();
  }
}
void SetBSDR(){
  if (BSMR == 1)
  {
    Serial2.print("vis q16,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q16,0");
    SndNxt();
  }
}
void SetBSDOff(){ 
  if (BSMOff == 1)
  {
    Serial2.print("vis q17,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q17,0");
    SndNxt();
  }
} 
void SetSRFOff(){
  if (SRFOff == 1)
  {
    Serial2.print("vis q18,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q18,0");
    SndNxt();
  }
}
void SetGearable(){
  if (Gearable == 1)
  {
    Serial2.print("vis q20,1");
    SndNxt();
    Serial2.print("vis q21,0");
    SndNxt();
  }
  else if (Gearable == 2)
  {
    Serial2.print("vis q20,0");
    SndNxt();
    Serial2.print("vis q21,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q20,0");
    SndNxt();
    Serial2.print("vis q21,0");
    SndNxt();
  }
}
void SetParkingBrake(){
  if (ParkingBrake == 1)
  {
    Serial2.print("vis q22,1");
    SndNxt();
  }
  else
  {
    Serial2.print("vis q22,0");
    SndNxt();
  }
}


//============================================================================================================================
//===Checks===================================================================================Checks==========================
//============================================================================================================================
void CheckPPark(){
  CheckGear();
  CheckBrightness();
  CheckTime();
  CheckFuel();
  CheckBSMOff();
  CheckSRFOff();
  CheckAlerts();
  CheckParkinBrake();
}
void CheckPMain(){
  CheckGear();
  CheckMPH();
  CheckCruise();
  CheckCruiseActivatable(); 
  CheckEyeSight();  
  CheckMPH();
  CheckTime();
  CheckFuel();
  CheckHeadlights();
  CheckMPH();
  CheckBrakes();
  CheckAlerts();
  CheckBSML();
  CheckBSMR();
  CheckMPH();
  CheckBSMOff();
  CheckSRFOff();
  CheckGearAbility();
  CheckParkinBrake();
}
void CheckPCruise(){
  CheckGear();
  CheckMPH();
  CheckCruise();
  CheckDistance();
  CheckSetSpeed();
  CheckFollowingCar();
  CheckEyeSight(); 
  CheckTime();
  CheckFuel();
  CheckHeadlights();
  CheckBrakes();
  CheckAlerts();
  CheckBSML();
  CheckBSMR();
  CheckBSMOff();
  CheckSRFOff();
  CheckBrakeHold();
}
void CheckPESError(){
  CheckGear();
  CheckMPH();
  CheckCruise();
  CheckCruiseActivatable();
  CheckEyeSight();  
  CheckTime();
  CheckFuel();
  CheckAlerts();
  CheckBSML();
  CheckBSMR();
  CheckBSMOff();
  CheckSRFOff();
  CheckGearAbility();
  CheckParkinBrake();
}
void CheckPPOPO(){ //FUture 
  //
}
void CheckPGauges(){ //TODo
  //
}
void CheckPSpeed(){
  CheckMPH();
}
void CheckChecks(){      //Check All -update
  CheckTime();
  CheckBrightness();
}
//------------------------------------------------------
void CheckAlerts(){  //TODO

}
//------------------------------------------------------
void CheckBrightness(){   //ADD CAN
  if (Headlights != CANHeadlights){
    Headlights = CANHeadlights;
    SetBrightness();
  }
  else{
    /* code */
  }
   
}
void CheckTime(){
  DateTime now = rtc.now();
  if (now.minute() != Minn || now.hour() != Hour){
    Serial.println(" ");
    Serial.print("Time Change");
    UpdateTime();
  }
  else{
    //nothing
  }
}
void CheckFuel(){         //ADD CAN
  //Do CAN Magic, Get Fuel
  if (FuelVal != CANFuel){
    FuelVal = CANFuel;
    SetFuel();
  }
  else{
    //Nothing
  }
  
}
void CheckGear(){         //ADD CAN
  //do can stuff here to find gear assign to CancurrentGear, Manual, Manual Gear
  tCAN GearMessage;
  if (mcp2515_check_message()) {
    //if (mcp2515_get_message(&GearMessage)); {
      //if(GearMessage.id == 0x166); {    
       // CANcurrentGear = GearMessage.data[3], HEX) & 0x1 ;
        //Serial.print(GearMessage.header.length,DEC);
        //Serial.print(CANESError);
      //}
    //}
  }
  
  if ((Manual == 0) && (currentGear != CANcurrentGear)) {
    ManualGear = 0;
    SetGearStuff();
  }
  else if ((Manual == 1) && (ManualGear != CANManualGear)){
    ManualGear = CANManualGear;
    currentGear = 'Z',
    SetManualGear();
  }
  else {
    //nothing
  }
}
void CheckMPH(){          //ADD CAN
  //DO CAN read for Speed
  if (MPH != CANMPH) {
    MPH = CANMPH;
    SetSpeed();
  }
  else{
    //Do Nothing
  }
}
void CheckPOP0(){         //Future Implimation
 //
}
void CheckTemp(){         //Future Implimation
  //
}
void CheckCruise(){       //ADD CAN
  //DO CAN Magic To Check Can Status 0/Off 1/Adaptive Active 2/Standard Active
  if (CANCruiseActive == 1 && CruiseActive == 0) {
    CruiseActive == CANCruiseActive;
    C.show();
    currentPage = 3;
    lastDrivePage = 2;
    loop();
  }
  else if (CANCruiseActive == 0 && CruiseActive == 1) {
    M.show();
    currentPage = 2;
    lastDrivePage = 3;
    loop();
  }
  else if (CANCruiseActive == 2 && CruiseActive == 0) {
    CruiseActive == CANCruiseActive;
    C.show();
    currentPage = 3;
    lastDrivePage = 2;
    delay(100);
    Serial2.print("vis q7,1"); //Display Standard Cruise icon
    SndNxt();
    loop();
  }
  else if (CANCruiseActive == 0 && CruiseActive == 2) {
    M.show();
    currentPage = 2;
    lastDrivePage = 3;
    loop();
  }
  else {
    //Do Nothing
  }
}
void CheckErrorCruise(){  //ADD CAN
  //DO CAN Magic To Check Can Status //0/Off 1/Active
  if (CANStandardCruiseActive == 1 && StandardCruiseActive == 0) {
    CruiseActive == CANCruiseActive;
    Serial2.print("vis p27,0");
    SndNxt();
    Serial2.print("vis p7,1");
    SndNxt();
  }
  else if (CANStandardCruiseActive == 0 && StandardCruiseActive == 1 && StandardCruiseActivatable == 0) {
    CruiseActive == CANCruiseActive;
    Serial2.print("vis p27,0");
    SndNxt();
    Serial2.print("vis p7,0");
    SndNxt();
  }
  else if (CANCruiseActive == 0 && CruiseActive == 2 && CruiseActivatable == 1) {
    CruiseActive == CANCruiseActive;
    Serial2.print("vis p27,1");
    SndNxt();
    Serial2.print("vis p7,0");
    SndNxt();
  }
  else {
    //Do Nothing
  }
}
void CheckStandardCruiseActivatable(){
  //Do Can Magic To See If Cruise ON then check cruise speed
  if (CANStandardCruiseActivatable != StandardCruiseActivatable)
  {
    CruiseActivatable = CANCruiseActivatable;
    CruiseSpeed = CANCruiseSpeed;
    SetStandardCruiseActivatable();
  }
  else
  {
    //Nothing
  }
  
}
void CheckCruiseActivatable(){ //ADD CAN
  //Do Can Magic To See If Cruise ON then check cruise speed
  if (CANCruiseActivatable != CruiseActivatable){
    CruiseActivatable = CANCruiseActivatable;
    CruiseSpeed = CANCruiseSpeed;
    SetCruiseActivatable();
  }
  else{
    //Nothing
  }
}
void CheckDistance(){     //ADD CAN
  //Do Can Magic
  if (DistVal != CANDistVal){
    SetCruiseDist();
  }
  else{
    //Nothing
  }
}
void CheckSetSpeed(){     //ADD CAN
  //Can Magic
  if (CruiseSpeed != CANCruiseSpeed){
    CruiseSpeed = CANCruiseSpeed;
    SetCruiseSpeed();
  }
  else{
    //Nothing
  }
}
void CheckFollowingCar(){ //ADD CAN
  //Can Magic
  if (FollowingCar != CANFollowingCar){
    FollowingCar = CANFollowingCar;
    SetFollowingCar();
  }
  else{
    //Nothing
  }
}
void CheckEyeSight(){     //Check CAN
  /*tCAN ESErrorMessage;
  if (mcp2515_check_message()) {
    if (mcp2515_get_message(&ESErrorMessage)) {
      if(ESErrorMessage.id == 0x166); {    
        CANESError = ESErrorMessage.data[3],HEX) & 0x1;
        Serial.print(ESErrorMessage.header.length,DEC);
        Serial.print(CANESError);
      }
    }
  }*/

  if (ESError != CANESError) {
    ESError = CANESError;
    if (ESError == 1) {
      I.show();
      currentPage = 4;
      loop();
    }
    else {
      M.show();
      currentPage = 2;
      loop();
    }
  }
  else {
    //NUll
  }
  
}
void CheckHeadlights(){   //ADD CAN
  //Can Magic
  if (Headlights != CANHeadlights){
    Headlights = CANHeadlights;
    SetHeadlights();
  }
  else{
    //Nothing
  }
}
void CheckBrakes(){       //ADD CAN
  //Can Magic
  if (Brakes != CANBrakes){
    Brakes = CANBrakes;
    SetBrakes();
  }
  else{
    //Nothing
  }
}
void CheckBrakeHold(){    //Future
 //
}
void CheckGearAbility(){  //ADD CAN see how to add in auto?
  if (Manual = 1){
    //Can Magic
    //See If Change gear possible
    if (Gearable != CANGearable){
     Gearable = CANGearable;
      SetGearable();
    }
    else{
     //Nothing
    }
  }
}
void CheckBSML(){         //ADD CAN
  //Can Magic
  if (BSML != CANBSML){
  BSML = CANBSML;
  SetBSDL();
  }
  else{
    //Nothing
  }
}
void CheckBSMR(){         //ADD CAN
  //Can Magic
  if (BSMR != CANBSML){
  BSMR = CANBSML;
  SetBSDR();
  }
  else{
    //Nothing
  }
}
void CheckBSMOff(){       //ADD CAN
  //Can Magic
  if (BSMOff != CANBSMOff){
  BSMOff = CANBSMOff;
  SetBSDOff();
  }
  else{
    //Nothing
  }
}
void CheckSRFOff(){       //ADD CAN
  //Can Magic
  if (SRFOff != CANSRFOff){
  SRFOff = CANSRFOff;
  SetSRFOff();
  }
  else{
    //Nothing
  }
}
void CheckParkinBrake(){  //ADD CAN
  //Can Magic
  if (ParkingBrake != CANParkingBrake){
  ParkingBrake = CANParkingBrake;
  SetParkingBrake();
  }
  else{
    //Nothing
  }
}


/*
tone(8,2200, 100);
 delay(70);
 noTone(8);
 delay(70);

tCAN ESErrorMessage;
  if (mcp2515_check_message()) {
    if (mcp2515_get_message(&ESErrorMessage)) {
      if(ESErrorMessage.id == 0x620) {    
        Serial.print("ID: ");
        Serial.print(ESErrorMessage.id,HEX);
        Serial.print(", ");
        Serial.print("Data: ");
        Serial.print(ESErrorMessage.header.length,DEC);
        for(int i=0;i<ESErrorMessage.header.length;i++) {	
          Serial.print(ESErrorMessage.data[i],HEX);
          Serial.print(" ");
        }
        Serial.println("");
      }
    }
  }
  
  */