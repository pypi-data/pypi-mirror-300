#ifndef MAIN_H
#define MAIN_H

#include <iostream>
#include <iomanip>
#include <exception>

#include "../../src/quantity.h"
#include "../../src/nostd/nostd.h"
#include "../../src/lists/lists.h"
#include "../../src/calc/calc.h"

void display_unit_systems();
void display_prefixes();
void display_base_units();
void display_derived_units();
void display_constants();
void display_quantities();
#ifdef UNITS_TEMPERATURES
void display_temperature_units();
#endif
#ifdef UNITS_LOGARITHMIC
void display_logarithmic_units();
#endif
void display_info(std::string expr);
void display_lists(std::deque<std::string>& convert);
  
#endif // MAIN_H
