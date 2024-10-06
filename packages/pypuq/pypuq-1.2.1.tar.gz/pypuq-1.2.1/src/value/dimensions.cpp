#include <sstream>
#include <iostream>
#include <iomanip>
#include <algorithm>

#include "../settings.h"
#include "value.h"

namespace puq {

  Dimensions::Dimensions(): utype(Utype::NUL), numerical(1) {
    for (int i=0; i<NUM_BASEDIM; i++) {
      physical[i] = 0; 
    }
  }

  Dimensions::Dimensions(const MAGNITUDE_TYPE& n): utype(Utype::NUL), numerical(n) {
    for (int i=0; i<NUM_BASEDIM; i++) {
      physical[i] = 0; 
    }
  }

#ifdef MAGNITUDE_ERRORS

  Dimensions::Dimensions(const MAGNITUDE_PRECISION& m, const MAGNITUDE_PRECISION& e): utype(Utype::NUL), numerical(m,e) {
    for (int i=0; i<NUM_BASEDIM; i++) {
      physical[i] = 0; 
    }  
  }

#endif

  inline std::string _numerical_to_string(MAGNITUDE_TYPE numerical, const BaseDimensions& physical,
					  Dformat& format, int precision) {
    std::stringstream ss;
    if ((format&Dformat::MKS)==Dformat::MKS) {
      numerical = numerical * (MAGNITUDE_TYPE)(std::pow(1e-3,(EXPONENT_REAL_PRECISION)physical[1]));
    } else if ((format&Dformat::CGS)==Dformat::CGS) {
      numerical = numerical * (MAGNITUDE_TYPE)(std::pow(1e2,(EXPONENT_REAL_PRECISION)physical[0]));
    }
#if defined(MAGNITUDE_ERRORS)
    if (numerical.value!=1 && (format&Dformat::NUM)==Dformat::NUM) {
      ss << numerical.to_string(precision) << SYMBOL_MULTIPLY;
    }
#elif defined(MAGNITUDE_ARRAYS)
    if (numerical!=1 && (format&Dformat::NUM)==Dformat::NUM) {
      ss << numerical.to_string(precision) << SYMBOL_MULTIPLY;
    }
#else
    if (numerical!=1 && (format&Dformat::NUM)==Dformat::NUM) {
      ss << std::setprecision(precision);
      ss << numerical << std::scientific << SYMBOL_MULTIPLY;
    }
#endif
    return ss.str();
  }


  inline std::string _physical_to_string(const BaseDimensions& physical, Dformat& format) {
    std::stringstream ss;
    for (int i=0; i<NUM_BASEDIM; i++) {
      std::string symbol = SystemData::BaseUnitOrder[i];
      if (i==1 && (format&Dformat::MKS)==Dformat::MKS) {
	symbol = "kg";
      } else if (i==0 && (format&Dformat::CGS)==Dformat::CGS) {
	symbol = "cm";
      }
#ifdef EXPONENT_FRACTIONS
      if (physical[i]!=0)
	ss << symbol << physical[i].to_string() << SYMBOL_MULTIPLY;
#else
      if (physical[i]==1)
	ss << symbol << SYMBOL_MULTIPLY;
      else if (physical[i]!=0)
	ss << symbol << physical[i] << SYMBOL_MULTIPLY;
#endif
    }
    return ss.str();
  }

  std::string Dimensions::to_string(Dformat format, int precision) const {
    std::stringstream ss;
    if ((format & Dformat::NUM)==Dformat::NUM) {
      ss << _numerical_to_string(numerical, physical, format, precision);
    }
    if ((format & Dformat::PHYS)==Dformat::PHYS) {
      ss << _physical_to_string(physical, format);
    }
    std::string s = ss.str();
    return (s=="") ? "1" : s.substr(0,s.size()-1);
  }

  std::ostream& operator<<(std::ostream& os, const Dimensions& d) {
    os << d.to_string();
    return os;
  }
  
  bool Dimensions::operator==(const Dimensions& d) const {
    for (int i=0; i<NUM_BASEDIM; i++) {
      if (physical[i]!=d.physical[i])
	return false;
    }
    return true;
  }

  bool Dimensions::operator!=(const Dimensions& d) const {
    bool equal = false;
    for (int i=0; i<NUM_BASEDIM; i++) {
      if (physical[i]!=d.physical[i])
	return true;
    }
    return false;
  }

}
