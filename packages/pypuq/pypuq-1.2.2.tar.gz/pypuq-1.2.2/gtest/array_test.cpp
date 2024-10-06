#include <gtest/gtest.h>

#include "../src/array.h"

#ifdef MAGNITUDE_ARRAYS

TEST(Array, Initialization) {

  puq::Array a;
  EXPECT_EQ(a.to_string(), "");
  a.append(3);              // appending a single value
  a.append({3.14, 3.14e5}); // appending a vector
  EXPECT_EQ(a.to_string(), "{3, 3.14, ...}");

  a = puq::Array(3);
  EXPECT_EQ(a.to_string(), "3");
  
  a = puq::Array({3,4});
  EXPECT_EQ(a.to_string(), "{3, 4}");

  a = puq::Array({3,4,5});
  EXPECT_EQ(a.to_string(), "{3, 4, ...}");

  a = puq::Array({3e12,4.34,5.23e2});
  EXPECT_EQ(a.to_string(), "{3e+12, 4.34, ...}");

  a = puq::Array({3,4,5});    
  std::stringstream ss;
  ss << a;                      // cast array as a string into a stream
  EXPECT_EQ(ss.str(), "{3, 4, ...}");
  
}

TEST(Array, Arithmetics) {

  puq::Array a, b, c;
  
  a = puq::Array({3.1,4.2,5.3});
  b = puq::Array({0.1,1.2,2.3});
  c = a + b;
  EXPECT_EQ(c.to_string(), "{3.2, 5.4, ...}");
  a += b;
  EXPECT_EQ(a.to_string(), "{3.2, 5.4, ...}");  

  a = puq::Array({3.1,4.2,5.3});
  b = puq::Array({0.1,1.2,2.3});
  c = a - b;
  EXPECT_EQ(c.to_string(), "{3, 3, ...}");
  a -= b;
  EXPECT_EQ(a.to_string(), "{3, 3, ...}");  

  a = puq::Array({3.1,4.2,5.3});
  b = puq::Array({0.1,1.2,2.3});
  c = a * b;
  EXPECT_EQ(c.to_string(), "{0.31, 5.04, ...}");
  a *= b;
  EXPECT_EQ(a.to_string(), "{0.31, 5.04, ...}");  

  a = puq::Array({3.1,4.2,5.3});
  b = puq::Array({0.1,1.2,2.3});
  c = a / b;
  EXPECT_EQ(c.to_string(), "{31, 3.5, ...}");
  a /= b;
  EXPECT_EQ(a.to_string(), "{31, 3.5, ...}");  
  
}

TEST(Array, Comparison) {

  puq::Array a, b;

  a = puq::Array({3.1,4.2,5.3});
  b = puq::Array({0.1,1.2,2.3});

  EXPECT_EQ(a==a, true);
  EXPECT_EQ(a!=a, false);
  EXPECT_EQ(a==b, false);
  EXPECT_EQ(a!=b, true);

}

#endif // MAGNITUDE_ARRAYS
