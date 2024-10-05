/*-----------------------------------------------------------------*/
/*!
  \file calcephspicefileversion.c
  \brief get file version of the SPICE KERNEL ephemeris data file

  \author  M. Gastineau
           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de
  Paris.

   Copyright, 2018-2023, CNRS
   email of the author : Mickael.Gastineau@obspm.fr

  History:
*/
/*-----------------------------------------------------------------*/

/*-----------------------------------------------------------------*/
/* License  of this file :
 This file is "triple-licensed", you have to choose one  of the three licenses
 below to apply on this file.

    CeCILL-C
        The CeCILL-C license is close to the GNU LGPL.
        ( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )

 or CeCILL-B
        The CeCILL-B license is close to the BSD.
        (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)

 or CeCILL v2.1
      The CeCILL license is compatible with the GNU GPL.
      ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )

This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under
French law and abiding by the rules of distribution of free software.
You can  use, modify and/ or redistribute the software under the terms
of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA
at the following URL "http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its
terms.
*/
/*-----------------------------------------------------------------*/

#include "calcephconfig.h"
#if HAVE_STDIO_H
#include <stdio.h>
#endif
#if HAVE_STDLIB_H
#include <stdlib.h>
#endif
#if HAVE_STRING_H
#include <string.h>
#endif
#if HAVE_ERRNO_H
#include <errno.h>
#endif
#if HAVE_MATH_H
#include <math.h>
#endif
#if HAVE_SYS_TYPES_H
#include <sys/types.h>
#endif

#include "calcephdebug.h"
#include "real.h"
#define __CALCEPH_WITHIN_CALCEPH 1
#include "calceph.h"
#include "calcephinternal.h"
#include "util.h"

/*--------------------------------------------------------------------------*/
/*! store, in szversion, the file version of the ephemeris file.
   return 0 if the file version was not found.
   return 1 on sucess.

  @param eph (inout) ephemeris descriptor
  @param szversion (out) null-terminated string of the version of the ephemeris
  file

*/
/*--------------------------------------------------------------------------*/
int calceph_spice_getfileversion(struct calcephbin_spice *eph, char szversion[CALCEPH_MAX_CONSTANTVALUE])
{
    int res = 1;
    double versio = 1.E0;
    t_calcephcharvalue szversio;
    int iversio;
    char subrelease;

    if (calceph_spice_getconstant_vs(eph, "INPOP_PCK_VERSION", &szversio, 1) == 1)
    {
        strcpy(szversion, szversio);
    }
    else if (calceph_spice_getconstant_vd(eph, "INPOP_PCK_VERSION", &versio, 1) == 1)
    {                           /* old INPOP release : deduce from versio */
        if (versio <= 0.2012011600000000E+04)
            versio = 10.2;      /*INPOP10B */

        else if (versio <= 0.2012120500000000E+04)
            versio = 10.5;      /*INPOP10E */

        else if (versio <= 0.2014040400000000E+04)
            versio = 13.2;      /*INPOP13B */

        else if (versio <= 0.2014061800000000E+04)
            versio = 13.3;      /*INPOP13C */

        else if (versio <= 0.2017082100000000E+04)
            versio = 17.1;      /* INPOP17A */
        iversio = (int) versio;
        subrelease = (char) rint((versio - iversio) * 10);
        sprintf(szversion, "INPOP%02d%c", iversio, 'A' + subrelease - 1);
    }
    else if (calceph_spice_getconstant_vs(eph, "EPM_PCK_VERSION", &szversio, 1) == 1)
    {
        strcpy(szversion, szversio);
    }
    else if (calceph_spice_getconstant_vs(eph, "PCK_VERSION", &szversio, 1) == 1)
    {
        strcpy(szversion, szversio);
    }
    else
    {
        res = 0;
    }
    return res;
}
