/** version.h -- version and copyright information **/

/***********************************************************************
 * This code is part of MAXE, a helper program for maximum entropy method
 *
 * Copyright (C) 2025 E.P.Csirmaz, L.Csirmaz
 * https://github.com/csirmaz/information-inequalities-5
 *
 * This program is free, open-source software. You may redistribute it
 * and/or modify under the terms of the GNU General Public License (GPL).
 *
 * There is ABSOLUTELY NO WARRANTY, use at your own risk.
 ***********************************************************************/

/* Name of this program */
#ifndef PROG
  #ifdef USETHREADS
    #define PROG		maxeth
  #else
    #define PROG		maxe
  #endif
#endif
#define PROGNAME		mkstringof(PROG)

/* Version and copyright */
#define VERSION_MAJOR	1
#define VERSION_MINOR	3
#ifdef USETHREADS
#define VERSION_STRING	"threaded version " mkstringof(VERSION_MAJOR.VERSION_MINOR) "T"
#else
#define VERSION_STRING	"version " mkstringof(VERSION_MAJOR.VERSION_MINOR)
#endif

#define COPYRIGHT	\
"Copyright (C) 2025 E.P.Csirmaz, L.Csirmaz\n"\
"https://github.com/csirmaz/information-inequalities-5"

/* EOF */

