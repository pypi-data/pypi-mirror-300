#include <benchmark/benchmark.h>

#include "../src/quantity.h"

static void BM_ConvertArray(benchmark::State& state) {
  puq::Array a;
  for (int i=0; i<state.range(0); i++)
    a.append(i);
  for (auto _ : state) {
    puq::Quantity q(a, "kg*m2/s2");
    q.convert("erg");
  }
}

BENCHMARK(BM_ConvertArray)->Arg(1)->Arg(10)->Arg(100)->Arg(1000)->Arg(10000)->Arg(100000);

static void BM_ConvertValue(benchmark::State& state) {
  puq::Quantity q(3, "kg*m2/s2");
  bool way = true;
  for (auto _ : state) {
    if (way) {
      q = q.convert("g*dm2/h2");
      way = false;
    } else {
      q = q.convert("kg*m2/s2");
      way = true;
    }
  }
}

BENCHMARK(BM_ConvertValue)->Arg(1)->Arg(10)->Arg(100)->Arg(1000)->Arg(10000);

static void BM_ConvertSystem(benchmark::State& state) {
  puq::Quantity q(3, "kg*m2/s2");
  bool way = true;
  for (auto _ : state) {
    if (way) {
      q = q.convert("g*dm2/h2", puq::SystemType::SI);
      way = false;
    } else {
      q = q.convert("kg*m2/s2", puq::SystemType::AU);
      way = true;
    }
  }
}

BENCHMARK(BM_ConvertSystem)->Arg(1)->Arg(10)->Arg(100)->Arg(1000)->Arg(10000);

BENCHMARK_MAIN();
