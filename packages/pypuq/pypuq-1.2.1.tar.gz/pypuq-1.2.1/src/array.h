#ifndef PUQ_ARRAY_H
#define PUQ_ARRAY_H

#include <vector>
#include <array>
#include <iostream>

#include "settings.h"
#include "exponent.h"

#ifdef MAGNITUDE_ARRAYS

namespace puq {

typedef std::vector<MAGNITUDE_PRECISION> ArrayValue;
class Array {
public:
  ArrayValue value;
  Array(): value() {};
  Array(const MAGNITUDE_PRECISION& v): value({v}) {value.shrink_to_fit();};
  Array(const ArrayValue& v): value(v) {value.shrink_to_fit();};
  static Array const_operation(const Array& a1, const Array& a2,
			       MAGNITUDE_PRECISION (*func)(const MAGNITUDE_PRECISION& v1,
							   const MAGNITUDE_PRECISION& v2));
  static Array filled(const MAGNITUDE_PRECISION& v, const size_t &s);
  std::string to_string(int precision=std::cout.precision()) const;
  size_t size() const;
  void append(const MAGNITUDE_PRECISION& v);
  void append(const ArrayValue& v);
  friend Array operator+(const Array& a1, const Array& a2);
  friend Array operator-(const Array& a1, const Array& a2);
  friend Array operator*(const Array& a1, const Array& a2);
  friend Array operator/(const Array& a1, const Array& a2);
  friend Array operator-(const Array& a);
  friend std::ostream& operator<<(std::ostream& os, const Array& a);
  void operator+=(const Array& a);
  void operator-=(const Array& a);
  void operator*=(const Array& a);
  void operator/=(const Array& a);
  bool operator==(const Array& a) const;
  bool operator!=(const Array& a) const;
  MAGNITUDE_PRECISION operator[](const size_t i) const;
  void pow(const EXPONENT_TYPE& e);
#ifdef EXPONENT_FRACTIONS
  void pow(const EXPONENT_INT_PRECISION& e);
#endif
  ArrayValue::const_iterator begin() const;
  ArrayValue::const_iterator end() const;
};

class ArraySizeException: public std::exception {
private:
  std::string message;  
public:
  ArraySizeException(std::string m) : message(m) {}
  ArraySizeException(const Array& a1, const Array& a2) : message("Arrays have different sizes: "+std::to_string(a1.size())+" != "+std::to_string(a2.size())) {}
  ArraySizeException(const ArrayValue& v1, const ArrayValue& v2) : message("Arrays have different sizes: "+std::to_string(v1.size())+" != "+std::to_string(v2.size())) {}
  const char * what () const noexcept override {
    return message.c_str();
  }
};

}
  
#endif

#endif // PUQ_ARRAY_H
