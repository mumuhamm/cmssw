#ifndef L1Trigger_Phase2L1GMT_HybridStubTypes_h
#define L1Trigger_Phase2L1GMT_HybridStubTypes_h

#include "ap_int.h"

namespace Phase2L1GMT {

  struct HybridStub {
    ap_int<BITSSTUBCOORD> coord1;
    ap_uint<BITSSIGMACOORD> sigma_coord1;
    ap_int<BITSSTUBCOORD> coord2;
    ap_uint<BITSSIGMACOORD> sigma_coord2;
    ap_int<BITSSTUBETA> eta;
    ap_uint<BITSSIGMAETA> sigma_eta1;
    ap_uint<BITSSIGMAETA> sigma_eta2;
    ap_uint<1> valid;
    ap_uint<1> is_barrel;
  };
  using propagation_t = HybridStub;

}  // namespace Phase2L1GMT

#endif
