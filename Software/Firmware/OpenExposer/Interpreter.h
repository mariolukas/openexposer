#ifndef PROCESSCONTROLLER_H
#define PROCESSCONTROLLER_H

extern int sofar;
extern char buffer[MAX_SERIAL_BUFFER];

void help();
void ready();
void processCommand();

#endif
