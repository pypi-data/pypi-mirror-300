#include <sstream>
#include <iostream>
#include <memory>

#include "value.h"
#include "../solver/solver.h"
#include "../converter.h"

namespace puq {
  
  UnitValue::UnitValue(const std::string& s) {
    UnitSolver solver;  
    UnitAtom atom = solver.solve(s);
    magnitude = atom.value.magnitude;
    baseunits = atom.value.baseunits;
  }

  UnitValue::UnitValue(const MAGNITUDE_TYPE& m, const std::string& s) {
    UnitSolver solver;  
    UnitAtom atom = solver.solve(s);
    magnitude = m * atom.value.magnitude;
    baseunits = atom.value.baseunits;
  }

  UnitValue::UnitValue(const MAGNITUDE_TYPE& m, const Dimensions& dim) {
    magnitude = m * dim.numerical;
    for (int i=0; i<NUM_BASEDIM; i++) {
      std::string symbol = SystemData::BaseUnitOrder[i];
      baseunits.append("", symbol, dim.physical[i]);
    }
  }

#ifdef MAGNITUDE_ERRORS
  UnitValue::UnitValue(const MAGNITUDE_PRECISION& m, const std::string& s) {
    UnitSolver solver;  
    UnitAtom atom = solver.solve(s);
    magnitude = Magnitude(m) * atom.value.magnitude;
    baseunits = atom.value.baseunits;
  }
  UnitValue::UnitValue(const MAGNITUDE_PRECISION& m, const MAGNITUDE_PRECISION& e, const std::string& s) {
    UnitSolver solver;  
    UnitAtom atom = solver.solve(s);
    magnitude = Magnitude(m,e) * atom.value.magnitude;
    baseunits = atom.value.baseunits;
  }
#ifdef MAGNITUDE_ARRAYS
  UnitValue::UnitValue(const Array& m, const std::string& s) {
    UnitSolver solver;  
    UnitAtom atom = solver.solve(s);
    magnitude = Magnitude(m) * atom.value.magnitude;
    baseunits = atom.value.baseunits;
  }
  UnitValue::UnitValue(const Array& m, const Array& e, const std::string& s) {
    UnitSolver solver;  
    UnitAtom atom = solver.solve(s);
    magnitude = Magnitude(m,e) * atom.value.magnitude;
    baseunits = atom.value.baseunits;
  }
#endif
#endif
  
  std::size_t UnitValue::size() const {
    return magnitude.size();
  }
  
  std::string UnitValue::to_string(int precision) const {
    std::stringstream ss;
  #if defined(MAGNITUDE_ERRORS)
    if (magnitude.value!=1 || baseunits.size()==0)
      ss << magnitude.to_string(precision) << SYMBOL_MULTIPLY;
  #elif defined(MAGNITUDE_ARRAYS)
    if (magnitude!=1 || baseunits.size()==0)
      ss << magnitude.to_string(precision) << SYMBOL_MULTIPLY;
  #else
    if (magnitude!=1 || baseunits.size()==0) {
      ss << std::setprecision(precision);
      ss << magnitude << std::scientific << SYMBOL_MULTIPLY;
    }
  #endif
    if (baseunits.size()>0)
      ss << baseunits.to_string() << SYMBOL_MULTIPLY;
    std::string s = ss.str();
    return s.substr(0,s.size()-1);
  }

  UnitValue operator+(const UnitValue& v1, const UnitValue& v2) {
    Converter conv(v2.baseunits, v1.baseunits);
  #ifdef UNITS_LOGARITHMIC
    if (conv.utype==Utype::LOG) {
      MAGNITUDE_TYPE m1 = v1.magnitude * conv.dimensions1.numerical;
      MAGNITUDE_TYPE m2 = conv.convert(v2.magnitude) * conv.dimensions2.numerical;
      if ((conv.dimensions1.utype & Utype::LOG) == Utype::LOG)
	m1 = nostd::pow(10, m1);
      if ((conv.dimensions2.utype & Utype::LOG) == Utype::LOG)
	m2 = nostd::pow(10, m2);
      return UnitValue(nostd::log10(m1 + m2) / conv.dimensions1.numerical, v1.baseunits);
    }
  #endif
    return UnitValue(v1.magnitude + conv.convert(v2.magnitude), v1.baseunits);
  }

  UnitValue operator+(const UnitValue& v) {
    return v;
  }
  
  void UnitValue::operator+=(const UnitValue& v) {
    Converter conv(v.baseunits, baseunits);
  #ifdef UNITS_LOGARITHMIC
    if (conv.utype==Utype::LOG) {
      MAGNITUDE_TYPE m1 = magnitude * conv.dimensions1.numerical;
      MAGNITUDE_TYPE m2 = conv.convert(v.magnitude) * conv.dimensions2.numerical;
      if ((conv.dimensions1.utype & Utype::LOG) == Utype::LOG)
	m1 = nostd::pow(10, m1);
      if ((conv.dimensions2.utype & Utype::LOG) == Utype::LOG)
	m2 = nostd::pow(10, m2);
      magnitude = nostd::log10(m1 + m2) / conv.dimensions1.numerical;
      return;
    }
  #endif
    magnitude += conv.convert(v.magnitude);
  }

  UnitValue operator-(const UnitValue& v1, const UnitValue& v2) {
    Converter conv(v2.baseunits, v1.baseunits);
  #ifdef UNITS_LOGARITHMIC
    if (conv.utype==Utype::LOG) {
      MAGNITUDE_TYPE m1 = v1.magnitude * conv.dimensions1.numerical;
      MAGNITUDE_TYPE m2 = conv.convert(v2.magnitude) * conv.dimensions2.numerical;
      if ((conv.dimensions1.utype & Utype::LOG) == Utype::LOG)
	m1 = nostd::pow(10, m1);
      if ((conv.dimensions2.utype & Utype::LOG) == Utype::LOG)
	m2 = nostd::pow(10, m2);
      return UnitValue(nostd::log10(m1 - m2) / conv.dimensions1.numerical, v1.baseunits);
    }
  #endif
    return UnitValue(v1.magnitude - conv.convert(v2.magnitude), v1.baseunits);
  }

  UnitValue operator-(const UnitValue& v) {
    return UnitValue(-v.magnitude, v.baseunits);
  }
  
  void UnitValue::operator-=(const UnitValue& v) {
    Converter conv(v.baseunits, baseunits);
  #ifdef UNITS_LOGARITHMIC
    if (conv.utype==Utype::LOG) {
      MAGNITUDE_TYPE m1 = magnitude * conv.dimensions1.numerical;
      MAGNITUDE_TYPE m2 = conv.convert(v.magnitude) * conv.dimensions2.numerical;
      if ((conv.dimensions1.utype & Utype::LOG) == Utype::LOG)
	m1 = nostd::pow(10, m1);
      if ((conv.dimensions2.utype & Utype::LOG) == Utype::LOG)
	m2 = nostd::pow(10, m2);
      magnitude = nostd::log10(m1 - m2) / conv.dimensions1.numerical;
      return;
    }
  #endif
    magnitude -= conv.convert(v.magnitude);
  }

  UnitValue operator*(const UnitValue& v1, const UnitValue& v2) {
    return UnitValue(v1.magnitude * v2.magnitude, v1.baseunits + v2.baseunits);
  }

  void UnitValue::operator*=(const UnitValue& v) {
    magnitude *= v.magnitude;
    baseunits += v.baseunits;
  }

  UnitValue operator/(const UnitValue& v1, const UnitValue& v2) {
    return UnitValue(v1.magnitude / v2.magnitude, v1.baseunits - v2.baseunits);
  }

  void UnitValue::operator/=(const UnitValue& v) {
    magnitude /= v.magnitude;
    baseunits -= v.baseunits;
  } 

  std::ostream& operator<<(std::ostream& os, const UnitValue& v) {
    os << v.to_string();
    return os;
  }
  
  void UnitValue::pow(const EXPONENT_TYPE& e) {
  #if defined(MAGNITUDE_ERRORS) || defined(MAGNITUDE_ARRAYS)
    magnitude.pow(e);
  #else
    magnitude = std::pow(magnitude, (EXPONENT_REAL_PRECISION)e);
  #endif
    baseunits *= e;
  }

  UnitValue UnitValue::convert(const std::string& s) const {
    UnitValue uv = UnitValue(s);
    return convert(uv);
  }

  UnitValue UnitValue::convert(const UnitValue& v) const {
    Converter conv(baseunits, v.baseunits);
    MAGNITUDE_TYPE m = conv.convert(magnitude, v.magnitude);
    return UnitValue(m, v.baseunits);
  }

  UnitValue UnitValue::convert(const BaseUnits& bu) const {
    Converter conv(baseunits, bu);
    return UnitValue(conv.convert(magnitude, 1), bu);
  }

  UnitValue UnitValue::convert(const Dformat& format) const {
    BaseUnits bu;
    Dimensions dim = baseunits.dimensions();
    for (int i=0; i<NUM_BASEDIM; i++) {
      if (dim.physical[i]==0)
	continue;
      if (i==1 && (format&Dformat::MKS)==Dformat::MKS) {
	bu.append({"k","g",dim.physical[i]});
      }
      else if (i==0 && (format&Dformat::CGS)==Dformat::CGS) {
	bu.append({"c","m",dim.physical[i]});	
      }
#ifdef UNIT_SYSTEM_EUS
      else if (i==0 && (format&Dformat::FPS)==Dformat::FPS) {
	bu.append({"","ft",dim.physical[i]});	
      }
      else if (i==1 && (format&Dformat::FPS)==Dformat::FPS) {
	bu.append({"","lb",dim.physical[i]});	
      }
#endif
      else {
	bu.append({"",SystemData::BaseUnitOrder[i],dim.physical[i]});
      }
    }
    return convert(bu);
  }
  
  UnitValue UnitValue::rebase_prefixes() {
    MAGNITUDE_TYPE mag = magnitude;
    std::map<std::string, BaseUnit> bumap;
    for (auto bu: baseunits) {
      if (bumap.find(bu.unit) == bumap.end()) {
	bumap.insert({bu.unit, {bu.prefix, bu.unit, bu.exponent}});
      } else {
	auto prefix1 = UnitPrefixList.find(bu.prefix);
	auto prefix2 = UnitPrefixList.find(bumap[bu.unit].prefix);
	if (prefix1!=UnitPrefixList.end())
	  mag *= nostd::pow(prefix1->second.magnitude, bu.exponent);
	if (prefix2!=UnitPrefixList.end())
	  mag /= nostd::pow(prefix2->second.magnitude, bu.exponent);
	bumap[bu.unit].exponent += bu.exponent;
      }
    }
    BaseUnits bus;
    for (auto bum: bumap) {
      bus.append(bum.second);
    }
    return UnitValue(mag, bus);
  }

  UnitValue UnitValue::rebase_dimensions() {
    MAGNITUDE_TYPE mag = magnitude;
    std::map<std::string, BaseUnit> bumap;
    for (auto bu: baseunits) {
      Dimensions dim = BaseUnits(bu.prefix+bu.unit).dimensions();
      std::string key = dim.to_string(Dformat::PHYS);
      if (bumap.find(key) == bumap.end()) {
	bumap.insert({key, {bu.prefix, bu.unit, bu.exponent}});
      } else {
	Dimensions dim0 = BaseUnits(bumap[key].prefix+bumap[key].unit).dimensions();
	mag *= nostd::pow(dim.numerical/dim0.numerical, bu.exponent);
	bumap[key].exponent += bu.exponent;
      }
    }
    BaseUnits bus;
    for (auto bum: bumap) {
      bus.append(bum.second);
    }
  return UnitValue(mag, bus);
  }
  
}
