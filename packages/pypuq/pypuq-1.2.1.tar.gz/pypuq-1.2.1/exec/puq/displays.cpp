#include "main.h"

void display_unit_systems() {
  std::cout << std::endl << "Unit systems:" << std::endl << std::endl;
  for (auto sys: puq::SystemMap) {
    std::cout << std::setfill(' ') << std::setw(8)  << std::left << sys.second->SystemAbbrev;
    std::cout << std::setfill(' ') << std::setw(22)  << std::left << sys.second->SystemName;
    std::cout << std::endl;
  }
  std::cout << std::endl;
}

void table_header(std::string title, std::vector<std::string> header, std::vector<int> width) {
  std::cout << std::endl;
  std::cout << title << std::endl << std::endl;
  for (size_t i=0; i<header.size(); i++) {
    std::cout << std::setfill(' ') << std::setw(width[i])  << std::left << header[i];
  }
  std::cout << std::endl;
  for (size_t i=0; i<header.size(); i++) {
    std::cout << std::setfill('-') << std::setw(width[i])  << std::right << "  ";
  }
  std::cout << std::endl;  
}

void display_prefixes() {
  table_header("Prefixes:", {"Symbol","Name","Magnitude"}, {8,8,11});
  for (auto symbol: puq::UnitPrefixOrder) {
    auto prefix = puq::UnitPrefixList.at(symbol);
    std::cout << std::setfill(' ') << std::setw(8)  << std::left << symbol;
    std::cout << std::setfill(' ') << std::setw(8)  << std::left << prefix.name;
    std::cout << std::setfill(' ') << std::setw(11) << std::left << puq::nostd::to_string(prefix.magnitude);
    std::cout << std::scientific << std::endl;
  }
  std::cout << std::endl;
}

void display_base_units() {
  table_header("Base units:", {"Symbol","Name","Allowed prefixes"}, {8,19,22});
  for (auto symbol: puq::SystemData::BaseUnitOrder) {
    auto unit = puq::UnitSystem::Data->UnitList.at(symbol);
    if ((unit.utype & puq::Utype::BAS)!=puq::Utype::BAS) continue;
    std::cout << std::setfill(' ') << std::setw(8)  << std::left << symbol;
    std::cout << std::setfill(' ') << std::setw(19) << std::left << unit.name;
    std::cout << std::setfill(' ') << std::setw(22) << std::left << puq::nostd::to_string(unit.use_prefixes, unit.allowed_prefixes);
    std::cout << std::scientific << std::endl;
  }
  std::cout << std::endl;
}

void display_derived_units() {
  table_header("Derived units:", {"Symbol","Name","Magnitude","Dimension","Definition","Allowed prefixes"}, {9,22,13,30,25,22});
  std::map<std::string, puq::UnitStruct> ordered(puq::UnitSystem::Data->UnitList.begin(), puq::UnitSystem::Data->UnitList.end());
  for (auto unit: ordered) {
    if ((unit.second.utype & puq::Utype::LIN)!=puq::Utype::LIN) continue;
    if ((unit.second.utype & puq::Utype::BAS)==puq::Utype::BAS) continue;
    if ((unit.second.utype & puq::Utype::CST)==puq::Utype::CST) continue;
    if ((unit.second.utype & puq::Utype::CSC)==puq::Utype::CSC) continue;
    puq::UnitValue uv(unit.first);
    puq::Dimensions dim = uv.baseunits.dimensions();
    std::cout << std::setfill(' ') << std::setw(9)  << std::left << unit.first;
    std::cout << std::setfill(' ') << std::setw(22) << std::left << unit.second.name;
    std::cout << std::setfill(' ') << std::setw(13) << std::left << dim.to_string(puq::Dformat::NUM);
    std::cout << std::setfill(' ') << std::setw(30) << std::left << dim.to_string(puq::Dformat::PHYS);
    std::cout << std::setfill(' ') << std::setw(25) << std::left << unit.second.definition;
    std::cout << std::setfill(' ') << std::setw(22) << std::left << puq::nostd::to_string(unit.second.use_prefixes, unit.second.allowed_prefixes);
    std::cout << std::scientific << std::endl;
  }
  std::cout << std::endl;
}

void display_constants() {
  table_header("Constants:", {"Symbol","Name","Magnitude","Dimension","Definition"}, {9,19,30,20,30});
  std::map<std::string, puq::UnitStruct> ordered(puq::UnitSystem::Data->UnitList.begin(), puq::UnitSystem::Data->UnitList.end());
  for (auto unit: ordered) {
    if ((unit.second.utype & puq::Utype::CST)!=puq::Utype::CST) continue;
    puq::UnitValue uv(unit.first);
    puq::Dimensions dim = uv.baseunits.dimensions();
    std::cout << std::setfill(' ') << std::setw(9)  << std::left << unit.first;
    std::cout << std::setfill(' ') << std::setw(19) << std::left << unit.second.name;
    std::cout << std::setfill(' ') << std::setw(30) << std::left << dim.to_string(puq::Dformat::NUM);
    std::cout << std::setfill(' ') << std::setw(20) << std::left << dim.to_string(puq::Dformat::PHYS);
    std::cout << std::setfill(' ') << std::setw(30) << std::left << unit.second.definition;
    std::cout << std::scientific << std::endl;
  }
  std::cout << std::endl;
}

void display_quantities() {
  table_header("Constants:", {"Symbol","Name","Magnitude","Dimension","Definition","SI factor"}, {10,30,30,22,25,11});
  std::map<std::string, puq::QuantityStruct> ordered(puq::UnitSystem::Data->QuantityList.begin(), puq::UnitSystem::Data->QuantityList.end());
  for (auto quantity: ordered) {
    std::string symbol = SYMBOL_QUANTITY_START+quantity.first+SYMBOL_QUANTITY_END;
    puq::UnitValue uv(symbol);
    puq::Dimensions dim = uv.baseunits.dimensions();
    std::cout << std::setfill(' ') << std::setw(10)  << std::left << symbol;
    std::cout << std::setfill(' ') << std::setw(30) << std::left << puq::QuantityNames.at(quantity.first);
    std::cout << std::setfill(' ') << std::setw(30) << std::left << dim.to_string(puq::Dformat::NUM);
    std::cout << std::setfill(' ') << std::setw(22) << std::left << dim.to_string(puq::Dformat::PHYS);
    std::cout << std::setfill(' ') << std::setw(25) << std::left << quantity.second.definition;
    std::cout << std::setfill(' ') << std::setw(11) << std::left << ((quantity.second.sifactor=="") ? "no" : "yes");
    std::cout << std::scientific << std::endl;
  }
  std::cout << std::endl;
}

#ifdef UNITS_TEMPERATURES
void display_temperature_units() {
  table_header("Temperatures:", {"Symbol","Name","Allowed prefixes"}, {9,19,22});
  std::map<std::string, puq::UnitStruct> ordered(puq::UnitSystem::Data->UnitList.begin(), puq::UnitSystem::Data->UnitList.end());
  for (auto unit: ordered) {
    if ((unit.second.utype & puq::Utype::TMP)!=puq::Utype::TMP) continue;
    std::cout << std::setfill(' ') << std::setw(9)  << std::left << unit.first;
    std::cout << std::setfill(' ') << std::setw(19) << std::left << unit.second.name;
    std::cout << std::setfill(' ') << std::setw(22) << std::left << puq::nostd::to_string(unit.second.use_prefixes, unit.second.allowed_prefixes);
    std::cout << std::scientific << std::endl;
  }
  std::cout << std::endl;
}
#endif

#ifdef UNITS_LOGARITHMIC
void display_logarithmic_units() {
  table_header("Logarithmic units:", {"Symbol","Name","Allowed prefixes"}, {9,19,22});
  std::map<std::string, puq::UnitStruct> ordered(puq::UnitSystem::Data->UnitList.begin(), puq::UnitSystem::Data->UnitList.end());
  for (auto unit: ordered) {
    if ((unit.second.utype & puq::Utype::LOG)!=puq::Utype::LOG) continue;
    std::cout << std::setfill(' ') << std::setw(9)  << std::left << unit.first;
    std::cout << std::setfill(' ') << std::setw(19) << std::left << unit.second.name;
    std::cout << std::setfill(' ') << std::setw(22) << std::left << puq::nostd::to_string(unit.second.use_prefixes, unit.second.allowed_prefixes);
    std::cout << std::scientific << std::endl;
  }
  std::cout << std::endl;
}
#endif

void display_info(std::string expr) {
  puq::UnitValue uv = puq::Quantity(expr).value;
  puq::BaseUnits bus = uv.baseunits;
  puq::Dimensions dim = bus.dimensions();
  puq::Dimensions dim_m = bus.dimensions();
  dim_m.numerical *= uv.magnitude;
  std::cout << std::endl << "Expression:  " << expr << std::endl << std::endl;
  std::cout << "Unit system: " << puq::UnitSystem::Data->SystemAbbrev << " (" << puq::UnitSystem::Data->SystemName << ")" << std::endl;
  std::cout << "Magnitude:   " << puq::nostd::to_string(uv.magnitude) << std::endl;
  std::cout << "Base units:  " << puq::nostd::to_string(uv.baseunits) << std::endl;
  std::stringstream ss; bool display = false;
  for (auto unit: puq::UnitSystem::Data->DimensionMap) {
    if (puq::Dimensions(1,unit.second.dimensions) != dim) continue;
    ss << (display?", ":"") << unit.first;
    display = true;
  }
  if (display) {
    std::cout << std::endl;
    std::cout << "Conversions: " << ss.str() << std::endl;
  }
  ss.str(std::string()); display = false;
  for (auto quant: puq::UnitSystem::Data->QuantityList) {
    if (puq::BaseUnits(quant.second.definition).dimensions() != dim) continue;
    ss << (display?", ":"") << quant.first;
    display = true;
  }
  if (display) {
    std::cout << std::endl;
    std::cout << "Quantities:  " << ss.str() << std::endl;
  }
  std::cout << std::endl;
  std::cout << "Dimensions:" << std::endl << std::endl;
  std::cout << "Base   Num*Mag                  Numerical                Physical" << std::endl;
  std::cout << "MGS    ";
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim_m.to_string(puq::Dformat::NUM);
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim.to_string(puq::Dformat::NUM);
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim.to_string(puq::Dformat::PHYS);
  std::cout << std::endl;
  std::cout << "MKS    ";
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim_m.to_string(puq::Dformat::NUM|puq::Dformat::MKS);
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim.to_string(puq::Dformat::NUM|puq::Dformat::MKS);
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim.to_string(puq::Dformat::PHYS|puq::Dformat::MKS);
  std::cout << std::endl;
  std::cout << "CGS    ";
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim_m.to_string(puq::Dformat::NUM|puq::Dformat::CGS);
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim.to_string(puq::Dformat::NUM|puq::Dformat::CGS);
  std::cout << std::setfill(' ') << std::setw(25) << std::left << dim.to_string(puq::Dformat::PHYS|puq::Dformat::CGS);
  std::cout << std::endl;
  if (bus.size() > 0) {
    table_header("Components:",
		 {"Prefix","Symbol","Exponent","Name","Definition","Dimensions MGS","Allowed prefixes"},
		 {8,8,10,30,30,22,22});
    for (auto unit: puq::UnitSystem::Data->UnitList) {
      for (auto bu: bus) {
	if (bu.unit!=unit.first)
	  continue;
	puq::BaseUnits bu_unit({bu});
	std::cout << std::setfill(' ') << std::setw(8) << std::left << bu.prefix;
	std::cout << std::setfill(' ') << std::setw(8) << std::left << bu.unit;
	std::cout << std::setfill(' ') << std::setw(10) << std::left << ((puq::nostd::to_string(bu.exponent)=="") ? "1" : puq::nostd::to_string(bu.exponent));
	std::cout << std::setfill(' ') << std::setw(30) << std::left << unit.second.name;
	std::cout << std::setfill(' ') << std::setw(30) << std::left << unit.second.definition;
	std::cout << std::setfill(' ') << std::setw(22) << std::left << bu_unit.dimensions().to_string();
	std::cout << std::setfill(' ') << std::setw(22) << std::left << puq::nostd::to_string(unit.second.use_prefixes, unit.second.allowed_prefixes);
	std::cout << std::scientific << std::endl;
      }
    }
    for (auto quant: puq::UnitSystem::Data->QuantityList) {
      for (auto bu: bus) {
	if (bu.unit!=SYMBOL_QUANTITY_START+quant.first+SYMBOL_QUANTITY_END)
	  continue;
	puq::BaseUnits bu_unit({bu});
	std::cout << std::setfill(' ') << std::setw(8) << std::left << bu.prefix;
	std::cout << std::setfill(' ') << std::setw(8) << std::left << bu.unit;
	std::cout << std::setfill(' ') << std::setw(10) << std::left << ((puq::nostd::to_string(bu.exponent)=="") ? "1" : puq::nostd::to_string(bu.exponent));
	std::cout << std::setfill(' ') << std::setw(30) << std::left << puq::QuantityNames.at(quant.first);
	std::cout << std::setfill(' ') << std::setw(30) << std::left << quant.second.definition;
	std::cout << std::setfill(' ') << std::setw(22) << std::left << bu_unit.dimensions().to_string();
	std::cout << std::setfill(' ') << std::setw(22) << std::left << "";
	std::cout << std::scientific << std::endl;
      }
    }
  }
  std::cout << std::endl;
}

void display_lists(std::deque<std::string>& convert) {
  std::stringstream ss;
  ss << std::endl;
  if (convert.size()>0) 
    ss << "List '" << convert[0] << "' does not exist." << std::endl << std::endl;
  ss << "Available lists:" << std::endl << std::endl;
  ss << "prefix  unit prefixes"         << std::endl;
  ss << "base    base units"            << std::endl;
  ss << "deriv   derived units"         << std::endl;
  ss << "log     logarithmic units"     << std::endl;
  ss << "temp    temperature units"     << std::endl;
  ss << "const   constants"             << std::endl;
  ss << "quant   quantities"            << std::endl;
  ss << "sys     unit systems"          << std::endl;
  throw std::runtime_error(ss.str());
}
