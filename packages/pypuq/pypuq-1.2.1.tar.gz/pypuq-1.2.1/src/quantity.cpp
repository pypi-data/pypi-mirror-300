#include <iostream>

#include "quantity.h"

namespace puq {

  void Quantity::preprocess(std::string& expression, SystemType& system) const {
#ifdef PREPROCESS_SYSTEM
    for (auto sys: SystemMap) {
      std::string symbol = sys.second->SystemAbbrev+SYMBOL_SYSTEM;
      if (expression.rfind(symbol, 0) == 0) {
	expression = expression.substr(symbol.size(), expression.size()-symbol.size());
	if (system==SystemType::NONE)
	  system = sys.first;
	else if (system!=sys.first) {
	  auto it = SystemMap.find(system);
	  throw UnitSystemExcept("Selected unit systems are ambiguous: "+it->second->SystemAbbrev+" "+sys.second->SystemAbbrev);
	}
	break;
      }
    }
    if (system==SystemType::NONE)
      system = UnitSystem::System;
#endif
#ifdef PREPROCESS_SYMBOLS
    // replace non standard symbols
    std::unordered_map<std::string, std::string> dict {
      {"\u00D710", SYMBOL_EXPONENT},  // ×10 -> e
      {"\u2212",   SYMBOL_MINUS},     // −   -> -
      {"\u22C5",   SYMBOL_MULTIPLY},  // ⋅   -> *
    };
    for (auto item: dict) {
      size_t pos = expression.find(item.first);
      while (pos != std::string::npos) {
	expression.replace(pos, item.first.size(), item.second);
	pos = expression.find(item.first, pos + item.first.size());
      }
    }
#endif
  }
  
  Quantity::Quantity(std::string s, const SystemType system): stype(system) {
    preprocess(s, stype);
    UnitSystem us(stype);
    value = UnitValue(s);
  }
  
  Quantity::Quantity(const UnitValue& v, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = v;
  }

  Quantity::Quantity(const MAGNITUDE_TYPE& m, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m);
  }
  
  Quantity::Quantity(const MAGNITUDE_TYPE& m, const BaseUnitsList& bu, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m, bu);
  }
  
  Quantity::Quantity(const MAGNITUDE_TYPE &m, std::string s, const SystemType system): stype(system) {
    preprocess(s, stype);
    UnitSystem us(stype); 
    value = UnitValue(m, s);
  }
  
#ifdef MAGNITUDE_ERRORS

  Quantity::Quantity(const MAGNITUDE_PRECISION& m, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m);
  }
  
  Quantity::Quantity(const MAGNITUDE_PRECISION& m, const BaseUnitsList& bu, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m, bu);
  }
  
  Quantity::Quantity(const MAGNITUDE_PRECISION& m, std::string s, const SystemType system): stype(system) {
    preprocess(s, stype);
    UnitSystem us(stype);
    Magnitude mag(m);
    value = UnitValue(mag, s);
  }

  Quantity::Quantity(const MAGNITUDE_PRECISION& m, const MAGNITUDE_PRECISION& e, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m, e);
  }
  
  Quantity::Quantity(const MAGNITUDE_PRECISION& m, const MAGNITUDE_PRECISION& e, const BaseUnitsList& bu, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m, e, bu);
  }
 
  Quantity::Quantity(const MAGNITUDE_PRECISION& m, const MAGNITUDE_PRECISION& e, std::string s, const SystemType system): stype(system) {
    preprocess(s, stype);
    UnitSystem us(stype);
    Magnitude mag(m,e);
    value = UnitValue(mag, s);
  }
  
#ifdef MAGNITUDE_ARRAYS

  Quantity::Quantity(const Array& m, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m);
  }
  
  Quantity::Quantity(const Array& m, const BaseUnitsList& bu, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m, bu);
  }
  
  Quantity::Quantity(const Array& m, std::string s, const SystemType system): stype(system) {
    preprocess(s, stype);
    UnitSystem us(stype);
    Magnitude mag(m);
    value = UnitValue(mag, s);
  }

  Quantity::Quantity(const Array& m, const Array& e, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m, e);
  }
  
  Quantity::Quantity(const Array& m, const Array& e, const BaseUnitsList& bu, const SystemType system): stype(system) {
    UnitSystem us(stype);
    value = UnitValue(m, e, bu);
  }
 
  Quantity::Quantity(const Array& m, const Array& e, std::string s, const SystemType system): stype(system) {
    preprocess(s, stype);
    UnitSystem us(stype);
    Magnitude mag(m,e);
    value = UnitValue(mag, s);
  }
  
#endif
  
#endif

  std::string Quantity::unit_system() const {
    auto it = SystemMap.find(stype);
    if (it == SystemMap.end()) {
      it = SystemMap.find(UnitSystem::System);
    }
    return it->second->SystemAbbrev;
  }

  std::size_t Quantity::size() const {
    return value.size();
  }
  
  // strings and streams
  std::string Quantity::to_string(int precision) const {
    UnitSystem us(stype);
    return value.to_string(precision);
  }
  std::ostream& operator<<(std::ostream& os, const Quantity& q) {
    os << q.to_string();
    return os;
  }

  // overloading quantity/quantity binary operations
  Quantity operator+(const Quantity& q1, const Quantity& q2) {
    UnitSystem us(q1.stype);
    if (q1.stype==q2.stype) {
      return Quantity(q1.value+q2.value);
    } else {
      Quantity q3 = q2.convert(q1.value.baseunits, q1.stype);
      return Quantity(q1.value+q3.value);
    }
  }
  Quantity operator-(const Quantity& q1, const Quantity& q2) {
    UnitSystem us(q1.stype);
    if (q1.stype==q2.stype) {
      return Quantity(q1.value-q2.value);
    } else {
      Quantity q3 = q2.convert(q1.value.baseunits, q1.stype);
      return Quantity(q1.value-q3.value);
    }
  }
  Quantity operator*(const Quantity& q1, const Quantity& q2) {
    if (q1.stype!=q2.stype)
      throw UnitSystemExcept(q1.stype, q2.stype);
    UnitSystem us(q1.stype);
    return Quantity(q1.value*q2.value);
  }
  Quantity operator/(const Quantity& q1, const Quantity& q2) {
    if (q1.stype!=q2.stype)
      throw UnitSystemExcept(q1.stype, q2.stype);
    UnitSystem us(q1.stype);
    return Quantity(q1.value/q2.value);
  }

  // overloading scalar/quantity
  Quantity operator+(const MAGNITUDE_PRECISION& m, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(m)+q.value);
  }  
  Quantity operator-(const MAGNITUDE_PRECISION& m, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(m)-q.value);
  }
  Quantity operator*(const MAGNITUDE_PRECISION& m, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(m)*q.value);
  }
  Quantity operator/(const MAGNITUDE_PRECISION& m, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(m)/q.value);
  }

  // overloading quantity/scalar
  Quantity operator+(const Quantity& q, const MAGNITUDE_PRECISION& m) {
    UnitSystem us(q.stype);
    return Quantity(q.value+UnitValue(m));
  }  
  Quantity operator-(const Quantity& q, const MAGNITUDE_PRECISION& m) {
    UnitSystem us(q.stype);
    return Quantity(q.value-UnitValue(m));
  }
  Quantity operator*(const Quantity& q, const MAGNITUDE_PRECISION& m) {
    UnitSystem us(q.stype);
    return Quantity(q.value*UnitValue(m));
  }
  Quantity operator/(const Quantity& q, const MAGNITUDE_PRECISION& m) {
    UnitSystem us(q.stype);
    return Quantity(q.value/UnitValue(m));
  }

  // overloading array/quantity
  Quantity operator+(const Array& a, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(a)+q.value);
  }  
  Quantity operator-(const Array& a, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(a)-q.value);
  }
  Quantity operator*(const Array& a, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(a)*q.value);
  }
  Quantity operator/(const Array& a, const Quantity& q) {
    UnitSystem us(q.stype);
    return Quantity(UnitValue(a)/q.value);
  }

  // overloading quantity/array
  Quantity operator+(const Quantity& q, const Array& a) {
    UnitSystem us(q.stype);
    q.value+UnitValue(a);
    return Quantity(q.value+UnitValue(a));
  }  
  Quantity operator-(const Quantity& q, const Array& a) {
    UnitSystem us(q.stype);
    return Quantity(q.value-UnitValue(a));
  }
  Quantity operator*(const Quantity& q, const Array& a) {
    UnitSystem us(q.stype);
    return Quantity(q.value*UnitValue(a));
  }
  Quantity operator/(const Quantity& q, const Array& a) {
    UnitSystem us(q.stype);
    return Quantity(q.value/UnitValue(a));
  }
  
  // overloading unary operations
  Quantity operator+(const Quantity& q) {
    return Quantity(+q.value);
  }
  Quantity operator-(const Quantity& q) {
    return Quantity(-q.value);
  }

  // overloading self assignment operations
  void Quantity::operator+=(Quantity& q) {
    UnitSystem us(stype);
    if (stype==q.stype) {
      value += q.value;
    } else {
      Quantity qc = q.convert(value.baseunits, stype);
      value += qc.value;
    }
  }
  void Quantity::operator-=(Quantity& q) {
    UnitSystem us(stype);
    if (stype==q.stype) {
      value -= q.value;
    } else {
      Quantity qc = q.convert(value.baseunits, stype);
      value -= qc.value;
    }
  }
  void Quantity::operator*=(Quantity& q) {
    if (stype!=q.stype)
      throw UnitSystemExcept(stype, q.stype);
    UnitSystem us(stype);
    value *= q.value;
  }
  void Quantity::operator/=(Quantity& q) {
    if (stype!=q.stype)
      throw UnitSystemExcept(stype, q.stype);
    UnitSystem us(stype);
    value /= q.value;
  }

  // conversion of units
  UnitValue Quantity::_convert_without_context(UnitSystem& us, const SystemType stt) const {
    Dimensions dim = value.baseunits.dimensions();
    us.change(stt);         // change the unit system
    return UnitValue(value.magnitude, dim);
  }

  UnitValue Quantity::_convert_with_context(UnitSystem& us, const SystemType stt,
					    QuantityListType::iterator& qs1, QuantityListType::iterator& qs2,
					    const std::string& q) const {
    UnitValue uv = value;
    if (qs1->second.sifactor != "") {
      uv *= UnitValue(SYMBOL_SIFACTOR_START+q+SYMBOL_SIFACTOR_END);
    }
    uv = uv.convert(SYMBOL_QUANTITY_START+q+SYMBOL_QUANTITY_END);
    us.change(stt);
    uv = UnitValue(uv.magnitude, SYMBOL_QUANTITY_START+q+SYMBOL_QUANTITY_END);
    if (qs2->second.sifactor != "") {
      uv /= UnitValue(SYMBOL_SIFACTOR_START+q+SYMBOL_SIFACTOR_END);
    }
    return uv;
  }  

  // convert using Dformat
  Quantity Quantity::convert(const Dformat& format) const {
    UnitSystem us(stype);
    return Quantity(value.convert(format));
  }
  
  // convert using quantity
  Quantity Quantity::convert(const Quantity& q) const {
    return convert(q.value, q.stype);
  }

  // convert using unit value
  Quantity Quantity::convert(const UnitValue& uv1) const {
    UnitSystem us(stype);
    UnitValue uv2 = value.convert(uv1);
    return Quantity(uv2);
  }

  Quantity Quantity::convert(const UnitValue& uv1, const SystemType system, const std::string& q) const {
    UnitSystem us(stype);
    if (stype == system) {
      return convert(uv1);
    } else if (q == "") {
      UnitValue uv2 = _convert_without_context(us, system);
      return Quantity(uv2.convert(uv1), system);
    } else {
      QuantityListType::iterator qs1 = puq::UnitSystem::Data->QuantityList.find(q);
      if (qs1==puq::UnitSystem::Data->QuantityList.end())
	throw UnitSystemExcept("Quantity symbol not found: "+q);
      us.change(system);       
      QuantityListType::iterator qs2 = puq::UnitSystem::Data->QuantityList.find(q);
      if (qs2==puq::UnitSystem::Data->QuantityList.end())
	throw UnitSystemExcept("Quantity symbol not found: "+q);
      us.change(stype);
      if (qs1->second.sifactor == "" && qs2->second.sifactor == "") {
	UnitValue uv2 = _convert_without_context(us, system);
	return Quantity(uv2.convert(uv1), system);
      } else {
	UnitValue uv2 = _convert_with_context(us, system, qs1, qs2, q);
	return Quantity(uv2.convert(uv1), system);
      }
    }
  }

  // convert using base units
  Quantity Quantity::convert(const BaseUnits& bu) const {
    UnitSystem us(stype);
    UnitValue uv = value.convert(bu);
    return Quantity(uv);
  }

  Quantity Quantity::convert(const BaseUnits& bu, const SystemType system, const std::string& q) const {
    UnitSystem us(stype);
    if (stype == system) {
      return convert(bu);
    } else if (q == "") {
      UnitValue uv = _convert_without_context(us, system);
      return Quantity(uv.convert(bu), system);
    } else {
      QuantityListType::iterator qs1 = puq::UnitSystem::Data->QuantityList.find(q);
      if (qs1==puq::UnitSystem::Data->QuantityList.end())
	throw UnitSystemExcept("Quantity symbol not found: "+q);
      us.change(system);       
      QuantityListType::iterator qs2 = puq::UnitSystem::Data->QuantityList.find(q);
      if (qs2==puq::UnitSystem::Data->QuantityList.end())
	throw UnitSystemExcept("Quantity symbol not found: "+q);
      us.change(stype);
      if (qs1->second.sifactor == "" && qs2->second.sifactor == "") {
	UnitValue uv = _convert_without_context(us, system);
	return Quantity(uv.convert(bu), system);
      } else {
	UnitValue uv = _convert_with_context(us, system, qs1, qs2, q);
	return Quantity(uv.convert(bu), system);
      }
    }
  }
  
  // convert using string expression
  Quantity Quantity::convert(std::string s, SystemType system, const std::string& q) const {
    preprocess(s, system);
    UnitSystem us(stype);
    if (stype == system) {
      UnitValue uv = value.convert(s);
      return Quantity(uv);
    } else if (q == "") {
      UnitValue uv = _convert_without_context(us, system);
      return Quantity(uv.convert(s), system);
    } else {      
      QuantityListType::iterator qs1 = puq::UnitSystem::Data->QuantityList.find(q);
      if (qs1==puq::UnitSystem::Data->QuantityList.end())
	throw UnitSystemExcept("Quantity symbol not found: "+q);
      us.change(system);  
      QuantityListType::iterator qs2 = puq::UnitSystem::Data->QuantityList.find(q);
      if (qs2==puq::UnitSystem::Data->QuantityList.end())
	throw UnitSystemExcept("Quantity symbol not found: "+q);
      us.change(stype);
      if (qs1->second.sifactor == "" && qs2->second.sifactor == "") {
	UnitValue uv = _convert_without_context(us, system);
	return Quantity(uv.convert(s), system);
      } else {
	UnitValue uv = _convert_with_context(us, system, qs1, qs2, q);
	return Quantity(uv.convert(s), system);
      }
    }
  }
  
  Quantity Quantity::rebase_prefixes() {
    UnitSystem us(stype);
    UnitValue uv = value.rebase_prefixes();
    return Quantity(uv);
  }
    
}
