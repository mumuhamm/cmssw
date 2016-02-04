#ifndef TrapezoidalCylindricalMFGrid_H
#define TrapezoidalCylindricalMFGrid_H

#include "MagneticField/Interpolation/interface/MFGrid3D.h"
#include "MagneticField/Interpolation/src/Trapezoid2RectangleMappingX.h"

class binary_ifstream;

class TrapezoidalCylindricalMFGrid : public MFGrid3D {
public:

  TrapezoidalCylindricalMFGrid( binary_ifstream& istr, 
				const GloballyPositioned<float>& vol);

  virtual LocalVector uncheckedValueInTesla( const LocalPoint& p) const;

  void dump() const;

  virtual void toGridFrame( const LocalPoint& p, double& a, double& b, double& c) const;

  virtual LocalPoint fromGridFrame( double a, double b, double c) const;

private:

  Trapezoid2RectangleMappingX mapping_;

};

#endif
