#include <sstream>
#include <iostream>
#include <iomanip>
#include <string>

#include "array.h"

#ifdef MAGNITUDE_ARRAYS

namespace puq {

inline void mutating_operation(ArrayValue& v1, const ArrayValue& v2,
			       void (*func)(MAGNITUDE_PRECISION& v1,
					    const MAGNITUDE_PRECISION& v2)) {
  if (v1.size()==v2.size())    // arrays have same sizes
    for (int i=0; i<v1.size(); i++)
      func(v1[i],v2[i]);       
  else if (v1.size()==1)       // first value is a scalar
    for (int i=0; i<v2.size(); i++)
      func(v1[0],v2[i]);
  else if (v2.size()==1)       // second value is a scalar
    for (int i=0; i<v1.size(); i++)
      func(v1[i],v2[0]);       
  else                         // arrays have different sizes
    throw ArraySizeException(v1, v2);
}

Array Array::const_operation(const Array& a1, const Array& a2,
			     MAGNITUDE_PRECISION (*func)(const MAGNITUDE_PRECISION& v1,
							 const MAGNITUDE_PRECISION& v2)) {
  Array a;
  if (a1.size()==a2.size()) {  // arrays have same sizes
    for (int i=0; i<a1.size(); i++)
      a.append(func(a1[i],a2[i]));
  } else if (a1.size()==1) {   // first value is a scalar
    for (int i=0; i<a2.size(); i++)
      a.append(func(a1[0],a2[i]));
  } else if (a2.size()==1) {   // second value is a scalar
    for (int i=0; i<a1.size(); i++)
      a.append(func(a1[i],a2[0]));
  } else {                     // arrays have different sizes
    throw ArraySizeException(a1, a2);
  }
  return a;
}

Array Array::filled(const MAGNITUDE_PRECISION& v, const size_t &s) {
  Array a;
  for (size_t i = 0; i<s; i++)
    a.append(v);
  return a;
};

std::string Array::to_string(int precision) const {
  std::stringstream ss;
  if (value.size()==1) {
    ss << std::setprecision(precision);
    ss << value[0] << std::scientific;
  } else if (value.size()==2) {
    ss << std::setprecision(precision);
    ss << SYMBOL_ARRAY_START << value[0];
    ss << SYMBOL_ARRAY_SEPARATOR << " " << value[1];
    ss << std::scientific << SYMBOL_ARRAY_END;
  } else if (value.size()>2) {
    ss << std::setprecision(precision);
    ss << SYMBOL_ARRAY_START << value[0];
    ss << SYMBOL_ARRAY_SEPARATOR << " " << value[1];
    ss << SYMBOL_ARRAY_SEPARATOR << " " << SYMBOL_ARRAY_MORE;
    ss << std::scientific << SYMBOL_ARRAY_END;
  }
  return ss.str();
}

size_t Array::size() const {
  return value.size();
};

void Array::append(const MAGNITUDE_PRECISION& v) {
  value.push_back(v);
}

void Array::append(const ArrayValue& v) {
  value.insert(value.end(), v.begin(), v.end());
}

MAGNITUDE_PRECISION Array::operator[](const size_t i) const {
  return value[i];
}

Array operator+(const Array& a1, const Array& a2) {
  auto fn = [](const MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    return v1 + v2;
  };
  return Array::const_operation(a1.value, a2.value, fn);
}

Array operator-(const Array& a1, const Array& a2) {
  auto fn = [](const MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    return v1 - v2;
  };
  return Array::const_operation(a1.value, a2.value, fn);
}

Array operator*(const Array& a1, const Array& a2) {
  auto fn = [](const MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    return v1 * v2;
  };
  return Array::const_operation(a1.value, a2.value, fn);
}

Array operator/(const Array& a1, const Array& a2) {
  auto fn = [](const MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    return v1 / v2;
  };
  return Array::const_operation(a1.value, a2.value, fn);
}

Array operator-(const Array& a) {
  ArrayValue av;
  for (int i=0; i<a.value.size(); i++)
    av.push_back(-a.value[i]);
  return Array(av);
}

void Array::operator+=(const Array& a) {
  auto fn = [](MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    v1 += v2;
  };
  mutating_operation(value, a.value, fn);
}

void Array::operator-=(const Array& a) {
  auto fn = [](MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    v1 -= v2;
  };
  mutating_operation(value, a.value, fn);
}

void Array::operator*=(const Array& a) {
  auto fn = [](MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    v1 *= v2;
  };
  mutating_operation(value, a.value, fn);
}

void Array::operator/=(const Array& a) {
  auto fn = [](MAGNITUDE_PRECISION& v1, const MAGNITUDE_PRECISION& v2) {
    v1 /= v2;
  };
  mutating_operation(value, a.value, fn);
}

bool Array::operator==(const Array& a) const {
  if (value.size()==a.value.size()) {    // arrays have same sizes
    for (int i=0; i<value.size(); i++)
      if (value[i] != a.value[i]) return false;       
  } else if (value.size()==1) {          // first value is a scalar
    for (int i=0; i<a.value.size(); i++)
      if (value[0] != a.value[i]) return false;
  } else if (a.value.size()==1) {        // second value is a scalar
    for (int i=0; i<value.size(); i++)
      if (value[i] != a.value[0]) return false;       
  } else {                               // arrays have different sizes
    throw ArraySizeException(value, a.value);
  }
  return true;
}

bool Array::operator!=(const Array& a) const {
  if (value.size()==a.value.size()) {    // arrays have same sizes
    for (int i=0; i<value.size(); i++)
      if (value[i] != a.value[i]) return true;       
  } else if (value.size()==1) {          // first value is a scalar
    for (int i=0; i<a.value.size(); i++)
      if (value[0] != a.value[i]) return true;
  } else if (a.value.size()==1) {        // second value is a scalar
    for (int i=0; i<value.size(); i++)
      if (value[i] != a.value[0]) return true;       
  } else {                               // arrays have different sizes
    throw ArraySizeException(value, a.value);
  }
  return false;
}

std::ostream& operator<<(std::ostream& os, const Array& a) {
  os << a.to_string();
  return os;
}
  
void Array::pow(const EXPONENT_TYPE& e) {
  for (int i=0; i<value.size(); i++)
    value[i] = std::pow(value[i], (EXPONENT_REAL_PRECISION)e);
}

#ifdef EXPONENT_FRACTIONS
void Array::pow(const EXPONENT_INT_PRECISION& e) {
  for (int i=0; i<value.size(); i++)
    value[i] = std::pow(value[i], e);
}
#endif

ArrayValue::const_iterator Array::begin() const {
  return value.begin();
}

ArrayValue::const_iterator Array::end() const {
  return value.end();
}

}
  
#endif
