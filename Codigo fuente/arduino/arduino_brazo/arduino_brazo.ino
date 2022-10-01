
#include <Servo.h> 
#include <stdlib.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo base;
Servo pinza;
Servo giromano;
#define cerrado 1550
#define abierto 800

int i=1;    // digital sensor
int j=0;
char cadena1[10];         // incoming serial byte
char z_servo1[4]; 
char z_servo2[4]; 
char z_servo3[4]; 
char base_servo[4];
char mano[4];
int z1;
int z2;
int z3;
int zbase;
int zbaseb;
int zbasei;
int hand;
String cadena2;
int i1=800;
int i2=2350;
int i3=1600;


void setup()
{
  // nuetros servos van desde 700 a 2450 useg
  Serial.begin(115200);
  Serial.setTimeout(700); 
  servo1.attach(9);
  servo2.attach(12);
  servo3.attach(11);
  giromano.attach(8);
  base.attach(13);
  pinza.attach(10);
  giromano.writeMicroseconds(635);
  pinza.writeMicroseconds(cerrado);    
  servo1.writeMicroseconds(800);
  servo2.writeMicroseconds(2350);  // posicion descanso
  servo3.writeMicroseconds(1600);    
  base.writeMicroseconds(1500);
  Serial.flush();
 
}

void irinicio()
{
    z1=800;
    z2=2350;                           // posicion de descanso
    z3=1600;   
    zbasei=1500;
    while (i1!=z1||i2!=z2||i3!=z3){
      if (i1!=z1) {
      if (i1<z1) { i1++;}
      else {i1--;}
      servo1.writeMicroseconds(i1);
      delayMicroseconds(500);}
      if (i2!=z2) {
      if (i2<z2) { i2++;}
      else {i2--;}
      servo2.writeMicroseconds(i2);
      delayMicroseconds(500);}
      if (i3!=z3) {
      if (i3<z3) { i3++;}
      else {i3--;} 
      servo3.writeMicroseconds(i3);
      delayMicroseconds(500);}}
    while (zbase!=zbasei){
      if (zbase!=zbasei) {
      if (zbase<zbasei) { zbase++;}
      else {zbase--;} 
      base.writeMicroseconds(zbase);
      delayMicroseconds(500);}}
}

void levantar()
{
    z1=800;
    z2=2350;                           // posicion de descanso
    z3=1600;
    while (i1!=z1||i2!=z2||i3!=z3){
      if (i1!=z1) {
      if (i1<z1) { i1++;}
      else {i1--;}
      servo1.writeMicroseconds(i1);
      delayMicroseconds(500);}
      if (i2!=z2) {
      if (i2<z2) { i2++;}
      else {i2--;}
      servo2.writeMicroseconds(i2);
      delayMicroseconds(500);}
    if (i3!=z3) {
      if (i3<z3) { i3++;}
      else {i3--;} 
      servo3.writeMicroseconds(i3);
      delayMicroseconds(500);}
    }
}

void irbasurero()
{
    z1=1600;
    z2=1600;                           // posiciones del basurero
    z3=1600;   
    zbaseb=2450;
    while (zbase!=zbaseb){
      if (zbase!=zbaseb) {
      if (zbase<zbaseb) { zbase++;}
      else {zbase--;} 
      base.writeMicroseconds(zbase);
      delayMicroseconds(500);}} 
    while (i1!=z1||i2!=z2||i3!=z3){
    if (i1!=z1) {
      if (i1<z1) { i1++;}
      else {i1--;}
      servo1.writeMicroseconds(i1);
      delayMicroseconds(500);}
    if (i2!=z2) {
      if (i2<z2) { i2++;}
      else {i2--;}
      servo2.writeMicroseconds(i2);
      delayMicroseconds(500);}
    if (i3!=z3) {
      if (i3<z3) { i3++;}
      else {i3--;} 
      servo3.writeMicroseconds(i3);
      delayMicroseconds(500);}}
}

void ir()
{
    base.writeMicroseconds(zbase);
    while (i1!=z1||i2!=z2||i3!=z3){
    if (i1!=z1) {
      if (i1<z1) { i1++;}
      else {i1--;}
      servo1.writeMicroseconds(i1);
      delayMicroseconds(500);}
    if (i2!=z2) {
      if (i2<z2) { i2++;}
      else {i2--;}
      servo2.writeMicroseconds(i2);
      delayMicroseconds(500);}
    if (i3!=z3) {
      if (i3<z3) { i3++;}
      else {i3--;} 
      servo3.writeMicroseconds(i3);
      delayMicroseconds(500);}}
}

void loop()
{

 
if (Serial.available() > 0){
    delay(1);
    Serial.readBytes(cadena1,2);
 


if(strcmp(cadena1,"co")==0){
           Serial.flush();
           Serial.println("conectados");
           for (j=0;j<=9;j++){   // bucle para borrar cadena
           cadena1[j]='\0'; }
       }

if(strcmp(cadena1,"bu")==0){
    Serial.flush();
    Serial.println("busco");
    //delay(1);
    Serial.readBytes(z_servo1,3);
    
    Serial.readBytes(z_servo2,3);
    
    Serial.readBytes(z_servo3,3);

    Serial.readBytes(base_servo,3);
    delay(1);
    Serial.println("buscando");
    z1=atoi(z_servo1);
    z2=atoi(z_servo2);
    z3=atoi(z_servo3);
    zbase=atoi(base_servo);
    z1=map(z1, 0, 180, 650, 2350);
    z2=map(z2, 0, 180, 650, 2350);
    z3=map(z3, 0, 180, 650, 2350);
    zbase=map(zbase, 0, 180, 650, 2350);
    Serial.flush();
    if (z1!=650&&z2!=650&&z3!=650&&zbase!=650) {
    pinza.writeMicroseconds(abierto);
    ir();
    delay(500);
    pinza.writeMicroseconds(cerrado);
    delay(500);
    levantar();
    irbasurero();
    pinza.writeMicroseconds(abierto);
    delay(500);
    pinza.writeMicroseconds(cerrado);    
    delay(100);
    irinicio();
    }
                                }
                                
if(strcmp(cadena1,"ir")==0){
    Serial.flush();
    Serial.println("voy");
    //delay(1);
    Serial.readBytes(z_servo1,3);
    
    Serial.readBytes(z_servo2,3);
    
    Serial.readBytes(z_servo3,3);

    Serial.readBytes(base_servo,3);
    
    Serial.readBytes(mano,3);  
    z1=atoi(z_servo1);
    z2=atoi(z_servo2);
    z3=atoi(z_servo3);
    zbase=atoi(base_servo);
    hand=atoi(mano);
    z1=map(z1, 0, 180, 650, 2350);
    z2=map(z2, 0, 180, 650, 2350);
    z3=map(z3, 0, 180, 650, 2350);
    zbase=map(zbase, 0, 180, 650, 2350);
    if (z1!=650&&z2!=650&&z3!=650&&zbase!=650) {
      if (hand==1){
      pinza.writeMicroseconds(abierto);
      }
      else{pinza.writeMicroseconds(cerrado);}
    ir();
    //delay(1000);
        }
                                }
 
Serial.flush();
}


//delay(2000);
for (j=0;j<=9;j++){   // bucle para borrar cadena
cadena1[j]='\0';
}


}


