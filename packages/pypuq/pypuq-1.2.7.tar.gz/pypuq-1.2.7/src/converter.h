#ifndef PUQ_CONVERTER_H
#define PUQ_CONVERTER_H

#include <bitset>
#include <memory>
#include <sstream>

#include "nostd/nostd.h"
#include "value/value.h"

namespace puq {

class ConvDimExcept: public std::exception {
private:
  std::string message;
public:
  ConvDimExcept(std::string m) : message(m) {}
  ConvDimExcept(const BaseUnits& bu1, const BaseUnits& bu2) { //const Dimensions& dim1, const Dimensions& dim2) {
    Dimensions dim1 = bu1.dimensions();
    Dimensions dim2 = bu2.dimensions();
    std::stringstream ss;
    ss << "Incompatible physical dimensions: " << bu1.to_string() << " (";
    ss << ((dim1.to_string(Dformat::PHYS)=="") ? "1" : dim1.to_string(Dformat::PHYS));
    ss << ") -> " << bu2.to_string() << " (";
    ss << ((dim2.to_string(Dformat::PHYS)=="") ? "1" : dim2.to_string(Dformat::PHYS));
    ss << ")" << std::endl;
    ss << "Suggested conversions: ";
    std::string mgs = dim1.to_string(Dformat::PHYS);
    std::string mks = dim1.to_string(Dformat::PHYS|Dformat::MKS);
    std::string cgs = dim1.to_string(Dformat::PHYS|Dformat::CGS);
    if (mgs=="") {
      ss << "1";
    } else {
      ss << mgs;
      if (mgs!=mks) ss << ", " << mks;
      if (mgs!=cgs && mks!=cgs) ss << ", " << cgs;
    }
    for (auto unit1: UnitSystem::Data->DimensionMap) {
      if (Dimensions(1,unit1.second.dimensions) != dim1) continue;
      if (unit1.first==mgs || unit1.first==mks || unit1.first==cgs) continue;
      ss << ", " << unit1.first;
    }
    message = ss.str();
  }
  const char * what () const noexcept override {
    return message.c_str();
  }
};

class NoConvExcept: public std::exception {
private:
  std::string message;  
public:
  NoConvExcept(const std::string& s1, const std::string& s2) : message("Conversion '"+s1+" -> "+s2+"' is not available!") {}
  const char * what () const noexcept override {
    return message.c_str();
  }
};

class Converter {
private:
  BaseUnits baseunits1;
  BaseUnits baseunits2;
  MAGNITUDE_TYPE _convert_linear(const MAGNITUDE_TYPE& m1, const MAGNITUDE_TYPE& m2);
#ifdef UNITS_LOGARITHMIC
  MAGNITUDE_TYPE _convert_logarithmic(MAGNITUDE_TYPE m);
#endif
#ifdef UNITS_TEMPERATURES
  MAGNITUDE_TYPE _convert_temperature(MAGNITUDE_TYPE m);
#endif
public:
  Utype utype;
  Dimensions dimensions1;
  Dimensions dimensions2;
  Converter(): utype(Utype::NUL) {};
  Converter(const BaseUnits& bu1, const BaseUnits& bu2);
  Converter(const std::string& s1, const std::string& s2): Converter(BaseUnits(s1), BaseUnits(s2)) {};
  MAGNITUDE_TYPE convert(const MAGNITUDE_TYPE& m1, const MAGNITUDE_TYPE& m2=1);
};

}
  
#endif // PUQ_CONVERTER_H
