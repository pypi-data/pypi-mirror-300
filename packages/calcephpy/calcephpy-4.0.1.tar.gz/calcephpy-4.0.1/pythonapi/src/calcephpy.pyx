# /*-----------------------------------------------------------------*/
# /*!
#  \file calcephpy.pyx
#  \brief public Python API for calceph library
#        access and interpolate INPOP and JPL Ephemeris data.
#
#  \author  M. Gastineau
#           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris.
#
#   Copyright, 2016-2024, CNRS
#   email of the author : Mickael.Gastineau@obspm.fr
# */
# /*-----------------------------------------------------------------*/
#
# /*-----------------------------------------------------------------*/
# /* License  of this file :
# This file is "triple-licensed", you have to choose one  of the three licenses
# below to apply on this file.
#
#    CeCILL-C
#    	The CeCILL-C license is close to the GNU LGPL.
#    	( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
#
# or CeCILL-B
#        The CeCILL-B license is close to the BSD.
#        (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
#
# or CeCILL v2.1
#      The CeCILL license is compatible with the GNU GPL.
#      ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
#
#
# This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/ or redistribute the software under the terms
# of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA
# at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its terms.
# */
# /*-----------------------------------------------------------------*/

# see http://docs.cython.org/en/latest/src/tutorial/clibraries.html
# compile with : python setyup.py build_ext -i
cimport calcephpy
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
cimport cpython.version
cimport cpython.string
import numpy


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/


class Constants:
    """Constants values of the CALCEPH library.

    >>> from calcephpy import Constants
    """
# /*----------------------------------------------------------------------------------------------*/
# /* definition of the CALCEPH library version */
# /*----------------------------------------------------------------------------------------------*/
# version : major number of CALCEPH library
    VERSION_MAJOR = 4
# version : minor number of CALCEPH library
    VERSION_MINOR = 0
#  version : patch number of CALCEPH library
    VERSION_PATCH = 1
#  version : string of characters
    VERSION_STRING = '4.0.1'

# /*----------------------------------------------------------------------------------------------*/
# /* definition of some constants */
# /*----------------------------------------------------------------------------------------------*/
# /*! define the maximum number of characters (including the trailing '\0')
# that the name of a constant could contain. */
    MAX_CONSTANTNAME = 33

# /*! define the offset value for asteroid for calceph_?compute */
    ASTEROID = 2000000

# /* unit for the output */
# /*! outputs are in Astronomical Unit */
    UNIT_AU = 1
# /*! outputs are in kilometers */
    UNIT_KM = 2
# /*! outputs are in day */
    UNIT_DAY = 4
# /*! outputs are in seconds */
    UNIT_SEC = 8
# /*! outputs are in radians */
    UNIT_RAD = 16

# /*! use the NAIF body identification numbers for target and center integers */
    USE_NAIFID = 32

# /* kind of output */
# /*! outputs are the euler angles */
    OUTPUT_EULERANGLES = 64
# /*! outputs are the nutation angles */
    OUTPUT_NUTATIONANGLES = 128

# /* Segment type for spice kernels and inpop/jpl original file format */
# /* segment of the original DE/INPOP file format */
    SEGTYPE_ORIG_0 = 0   
# /* segment of the spice kernels */
    SEGTYPE_SPK_1 = 1
    SEGTYPE_SPK_2 = 2
    SEGTYPE_SPK_3 = 3
    SEGTYPE_SPK_5 = 5
    SEGTYPE_SPK_8 = 8
    SEGTYPE_SPK_9 = 9
    SEGTYPE_SPK_12 = 12
    SEGTYPE_SPK_13 = 13
    SEGTYPE_SPK_14 = 14
    SEGTYPE_SPK_17 = 17
    SEGTYPE_SPK_18 = 18
    SEGTYPE_SPK_19 = 19
    SEGTYPE_SPK_20 = 20
    SEGTYPE_SPK_21 = 21
    SEGTYPE_SPK_102 = 102
    SEGTYPE_SPK_103 = 103
    SEGTYPE_SPK_120 = 120 

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
class NaifId:
    """NAIF identification numbers of the CALCEPH library.

    >>> from calcephpy import NaifId
    """
# /*! NAIF identification numbers for the Sun and planetary barycenters (table 2 of reference 1) */
    SOLAR_SYSTEM_BARYCENTER = 0
    MERCURY_BARYCENTER = 1
    VENUS_BARYCENTER = 2
    EARTH_MOON_BARYCENTER = 3
    MARS_BARYCENTER = 4
    JUPITER_BARYCENTER = 5
    SATURN_BARYCENTER = 6
    URANUS_BARYCENTER = 7
    NEPTUNE_BARYCENTER = 8
    PLUTO_BARYCENTER = 9
    SUN = 10

# /*! NAIF identification numbers for the Coordinate Time ephemerides */
# /*! value to set as the center to get any Coordinate Time */
    TIME_CENTER = 1000000000
# /*! value to set as the target to get the Coordinate Time TT-TDB */
    TIME_TTMTDB = 1000000001
# /*! value to set as the target to get the Coordinate Time TCG-TCB */
    TIME_TCGMTCB = 1000000002

# /*! NAIF identification numbers for the planet centers and satellites (table= 3 of reference= 1)  */
    MERCURY = 199
    VENUS = 299
    EARTH = 399
    MOON = 301

    MARS = 499
    PHOBOS = 401
    DEIMOS = 402

    JUPITER = 599
    IO = 501
    EUROPA = 502
    GANYMEDE = 503
    CALLISTO = 504
    AMALTHEA = 505
    HIMALIA = 506
    ELARA = 507
    PASIPHAE = 508
    SINOPE = 509
    LYSITHEA = 510
    CARME = 511
    ANANKE = 512
    LEDA = 513
    THEBE = 514
    ADRASTEA = 515
    METIS = 516
    CALLIRRHOE = 517
    THEMISTO = 518
    MEGACLITE = 519
    TAYGETE = 520
    CHALDENE = 521
    HARPALYKE = 522
    KALYKE = 523
    IOCASTE = 524
    ERINOME = 525
    ISONOE = 526
    PRAXIDIKE = 527
    AUTONOE = 528
    THYONE = 529
    HERMIPPE = 530
    AITNE = 531
    EURYDOME = 532
    EUANTHE = 533
    EUPORIE = 534
    ORTHOSIE = 535
    SPONDE = 536
    KALE = 537
    PASITHEE = 538
    HEGEMONE = 539
    MNEME = 540
    AOEDE = 541
    THELXINOE = 542
    ARCHE = 543
    KALLICHORE = 544
    HELIKE = 545
    CARPO = 546
    EUKELADE = 547
    CYLLENE = 548
    KORE = 549
    HERSE = 550
    DIA = 553

    SATURN = 699
    MIMAS = 601
    ENCELADUS = 602
    TETHYS = 603
    DIONE = 604
    RHEA = 605
    TITAN = 606
    HYPERION = 607
    IAPETUS = 608
    PHOEBE = 609
    JANUS = 610
    EPIMETHEUS = 611
    HELENE = 612
    TELESTO = 613
    CALYPSO = 614
    ATLAS = 615
    PROMETHEUS = 616
    PANDORA = 617
    PAN = 618
    YMIR = 619
    PAALIAQ = 620
    TARVOS = 621
    IJIRAQ = 622
    SUTTUNGR = 623
    KIVIUQ = 624
    MUNDILFARI = 625
    ALBIORIX = 626
    SKATHI = 627
    ERRIAPUS = 628
    SIARNAQ = 629
    THRYMR = 630
    NARVI = 631
    METHONE = 632
    PALLENE = 633
    POLYDEUCES = 634
    DAPHNIS = 635
    AEGIR = 636
    BEBHIONN = 637
    BERGELMIR = 638
    BESTLA = 639
    FARBAUTI = 640
    FENRIR = 641
    FORNJOT = 642
    HATI = 643
    HYROKKIN = 644
    KARI = 645
    LOGE = 646
    SKOLL = 647
    SURTUR = 648
    ANTHE = 649
    JARNSAXA = 650
    GREIP = 651
    TARQEQ = 652
    AEGAEON = 653

    URANUS = 799
    ARIEL = 701
    UMBRIEL = 702
    TITANIA = 703
    OBERON = 704
    MIRANDA = 705
    CORDELIA = 706
    OPHELIA = 707
    BIANCA = 708
    CRESSIDA = 709
    DESDEMONA = 710
    JULIET = 711
    PORTIA = 712
    ROSALIND = 713
    BELINDA = 714
    PUCK = 715
    CALIBAN = 716
    SYCORAX = 717
    PROSPERO = 718
    SETEBOS = 719
    STEPHANO = 720
    TRINCULO = 721
    FRANCISCO = 722
    MARGARET = 723
    FERDINAND = 724
    PERDITA = 725
    MAB = 726
    CUPID = 727

    NEPTUNE = 899
    TRITON = 801
    NEREID = 802
    NAIAD = 803
    THALASSA = 804
    DESPINA = 805
    GALATEA = 806
    LARISSA = 807
    PROTEUS = 808
    HALIMEDE = 809
    PSAMATHE = 810
    SAO = 811
    LAOMEDEIA = 812
    NESO = 813

    PLUTO = 999
    CHARON = 901
    NIX = 902
    HYDRA = 903
    KERBEROS = 904
    STYX = 905

# /*! NAIF identification numbers for the comets (table= 4 of reference= 1)  */
    AREND = 1000001
    AREND_RIGAUX = 1000002
    ASHBROOK_JACKSON = 1000003
    BOETHIN = 1000004
    BORRELLY = 1000005
    BOWELL_SKIFF = 1000006
    BRADFIELD = 1000007
    BROOKS_2 = 1000008
    BRORSEN_METCALF = 1000009
    BUS = 1000010
    CHERNYKH = 1000011
    CHURYUMOV_GERASIMENKO = 1000012
    CIFFREO = 1000013
    CLARK = 1000014
    COMAS_SOLA = 1000015
    CROMMELIN = 1000016
    D__ARREST = 1000017
    DANIEL = 1000018
    DE_VICO_SWIFT = 1000019
    DENNING_FUJIKAWA = 1000020
    DU_TOIT_1 = 1000021
    DU_TOIT_HARTLEY = 1000022
    DUTOIT_NEUJMIN_DELPORTE = 1000023
    DUBIAGO = 1000024
    ENCKE = 1000025
    FAYE = 1000026
    FINLAY = 1000027
    FORBES = 1000028
    GEHRELS_1 = 1000029
    GEHRELS_2 = 1000030
    GEHRELS_3 = 1000031
    GIACOBINI_ZINNER = 1000032
    GICLAS = 1000033
    GRIGG_SKJELLERUP = 1000034
    GUNN = 1000035
    HALLEY = 1000036
    HANEDA_CAMPOS = 1000037
    HARRINGTON = 1000038
    HARRINGTON_ABELL = 1000039
    HARTLEY_1 = 1000040
    HARTLEY_2 = 1000041
    HARTLEY_IRAS = 1000042
    HERSCHEL_RIGOLLET = 1000043
    HOLMES = 1000044
    HONDA_MRKOS_PAJDUSAKOVA = 1000045
    HOWELL = 1000046
    IRAS = 1000047
    JACKSON_NEUJMIN = 1000048
    JOHNSON = 1000049
    KEARNS_KWEE = 1000050
    KLEMOLA = 1000051
    KOHOUTEK = 1000052
    KOJIMA = 1000053
    KOPFF = 1000054
    KOWAL_1 = 1000055
    KOWAL_2 = 1000056
    KOWAL_MRKOS = 1000057
    KOWAL_VAVROVA = 1000058
    LONGMORE = 1000059
    LOVAS_1 = 1000060
    MACHHOLZ = 1000061
    MAURY = 1000062
    NEUJMIN_1 = 1000063
    NEUJMIN_2 = 1000064
    NEUJMIN_3 = 1000065
    OLBERS = 1000066
    PETERS_HARTLEY = 1000067
    PONS_BROOKS = 1000068
    PONS_WINNECKE = 1000069
    REINMUTH_1 = 1000070
    REINMUTH_2 = 1000071
    RUSSELL_1 = 1000072
    RUSSELL_2 = 1000073
    RUSSELL_3 = 1000074
    RUSSELL_4 = 1000075
    SANGUIN = 1000076
    SCHAUMASSE = 1000077
    SCHUSTER = 1000078
    SCHWASSMANN_WACHMANN_1 = 1000079
    SCHWASSMANN_WACHMANN_2 = 1000080
    SCHWASSMANN_WACHMANN_3 = 1000081
    SHAJN_SCHALDACH = 1000082
    SHOEMAKER_1 = 1000083
    SHOEMAKER_2 = 1000084
    SHOEMAKER_3 = 1000085
    SINGER_BREWSTER = 1000086
    SLAUGHTER_BURNHAM = 1000087
    SMIRNOVA_CHERNYKH = 1000088
    STEPHAN_OTERMA = 1000089
    SWIFT_GEHRELS = 1000090
    TAKAMIZAWA = 1000091
    TAYLOR = 1000092
    TEMPEL_1 = 1000093
    TEMPEL_2 = 1000094
    TEMPEL_TUTTLE = 1000095
    TRITTON = 1000096
    TSUCHINSHAN_1 = 1000097
    TSUCHINSHAN_2 = 1000098
    TUTTLE = 1000099
    TUTTLE_GIACOBINI_KRESAK = 1000100
    VAISALA_1 = 1000101
    VAN_BIESBROECK = 1000102
    VAN_HOUTEN = 1000103
    WEST_KOHOUTEK_IKEMURA = 1000104
    WHIPPLE = 1000105
    WILD_1 = 1000106
    WILD_2 = 1000107
    WILD_3 = 1000108
    WIRTANEN = 1000109
    WOLF = 1000110
    WOLF_HARRINGTON = 1000111
    LOVAS_2 = 1000112
    URATA_NIIJIMA = 1000113
    WISEMAN_SKIFF = 1000114
    HELIN = 1000115
    MUELLER = 1000116
    SHOEMAKER_HOLT_1 = 1000117
    HELIN_ROMAN_CROCKETT = 1000118
    HARTLEY_3 = 1000119
    PARKER_HARTLEY = 1000120
    HELIN_ROMAN_ALU_1 = 1000121
    WILD_4 = 1000122
    MUELLER_2 = 1000123
    MUELLER_3 = 1000124
    SHOEMAKER_LEVY_1 = 1000125
    SHOEMAKER_LEVY_2 = 1000126
    HOLT_OLMSTEAD = 1000127
    METCALF_BREWINGTON = 1000128
    LEVY = 1000129
    SHOEMAKER_LEVY_9 = 1000130
    HYAKUTAKE = 1000131
    HALE_BOPP = 1000132
    SIDING_SPRING = 1003228


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
cdef class CalcephBin:
    """A CalcephBin class to access the ephemeris file.

    >>> from calcephpy import *
    >>> f = CalcephBin.open("ephemerisfile.dat")
    >>> PV = f.compute(jd, dt, target, center)
    >>> PV = peph.compute_unit(jd0, dt, NaifId.EARTH, NaifId.SUN,
                               Constants.UNIT_AU+Constants.UNIT_DAY+Constants.USE_NAIFID)
    >>> f.close()
    """
    cdef calcephpy.t_calcephbin * _c_handle

    def __cinit__(self):
        self._c_handle = NULL

    def __dealloc__(self):
        if self._c_handle is not NULL:
            calcephpy.calceph_close(self._c_handle)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/

    @staticmethod
    def __check_returnerror_0(res):
        """internal : check the error of the library  and raise an exception"""
        global __usertypehandler_python
        if (res == 0) and (__usertypehandler_python != 3):
            raise RuntimeError("Calceph library has encountered a problem")


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/

    def __check_returnerror_null(self):
        """check if the ephemeris file is opened on exit and raise an exception"""
        if (self._c_handle is NULL) and (__usertypehandler_python != 3):
            raise RuntimeError("No ephemeris files are opened")

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    def __check_chandle_null(self):
        """check if the ephemeris file is opened on input and raise an exception"""
        if (self._c_handle is NULL):
            raise RuntimeError("No ephemeris files are opened")

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    @staticmethod
    def __isarray_and_samesize(v1, v2):
        """internal : return non-zero value if v1 and v2 are two arrays of same size """
        try:
            n = len(v1)
            supportlen = True
        except:
            supportlen = False

        if supportlen :
            if len(v1) != len(v2):
                raise RuntimeError("The two vectors of time should have the same length")
            return 1
        
        return 0


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    @staticmethod
    def __exportresult(v,n, typeres):
        """internal : return the numpy-array v as n vectors. These n vectors have the same type as typeres
         the vector[1] is extracted as v[1::n],  the vector[2] is extracted as v[2::n], ... """
                                 
        vlist = []
        if isinstance(typeres, numpy.ndarray):
            for k in range(n):
                vlist.append(v[k::n])
        else:
            for k in range(n):
                vlist.append(v[k::n].tolist())
        return vlist


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    @staticmethod
    def open(pyarfilename):
        """Open the file(s) pyarfilename
    
              pyarfilename (in) a single string or an array of strings
        """
        cdef bytes bs
        cdef char **arfilename
        cdef char *filename1
        cdef char* c_string
        cdef char* c_arfilename
        # self.close()
        v = CalcephBin()
        if  isinstance(pyarfilename,str):
            py_byte_pyarfilename = pyarfilename.encode('ascii')
            c_arfilename = py_byte_pyarfilename
            v._c_handle = calcephpy.calceph_open(c_arfilename) 
        else:
            # copy the array of string
            slen = len(pyarfilename)
            arfilename = <char**>PyMem_Malloc(slen * sizeof(char*))
            if not arfilename:
                raise MemoryError()
                    
            py_byte_pyarfilename = [s.encode('ascii') for s in pyarfilename] 
            for i in range(slen):
                arfilename[i] = py_byte_pyarfilename[i]
                
            # open files 
            v._c_handle = calcephpy.calceph_open_array(slen, <const char * const*>arfilename)
            
            PyMem_Free(arfilename)
        v.__check_returnerror_null()
        return v


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef close(self):
        """Close the ephemeris file"""
        if self._c_handle is not  NULL:
            calcephpy.calceph_close(self._c_handle)
        self._c_handle = NULL


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef prefetch(self):
        """Prefetch all data to memory"""
        self.__check_returnerror_null()
        res = calcephpy.calceph_prefetch(self._c_handle)
        self.__check_returnerror_0(res)

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __vector_compute(self, JD0, time, target, center):
        """internal : compute the position <x,y,z> and velocity <xdot,ydot,zdot>
           for a given target and center for a vector of times. The output is in UA, UA/day, radians
           The vector JD0 and time must have the same length
           
           return a list of 6 vectors : position and the velocity of the "target" object.
           Each vector has the same length as JD0 and contains a single component of the position or velocity.

    
           @param JD0 (in) vector of reference time (could be 0)
           @param time (in) vector of time elapsed from JD0
           @param target (in) "target" object 
           @param center (in) "center" object """
                                 
        n = len(JD0)
        cdef double lPV[6]
        vPV = numpy.zeros(6*n, dtype=numpy.float64)
        for j in range(n):
            res = calcephpy.calceph_compute(self._c_handle, JD0[j], time[j], target, center, lPV)
            self.__check_returnerror_0(res)
            vPV[6*j:6*j+6] = lPV 
        return self.__exportresult(vPV, 6, JD0)
 
# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __scalar_compute(self, JD0, time, target, center):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
           for a given target and center at a single time. The output is in UA, UA/day, radians
           
           return a list of 6 elements : position and the velocity of the "target" object.
    
           @param JD0 (in) reference time (could be 0)
           @param time (in) time elapsed from JD0
           @param target (in) "target" object 
           @param center (in) "center" object """
                                 
        cdef double PV[6]
        res = calcephpy.calceph_compute(self._c_handle, JD0, time, target, center, PV)
        self.__check_returnerror_0(res)
        return PV
            

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef compute(self, JD0, time, target, center):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
           for a given target and center at the given time. The output is in UA, UA/day, radians.

           
            If JD0 is a scalar, it returns a list of 6 elements : position and the velocity of the "target" object.
            If JD0 is a list or numpy's array, it returns a list of 6 vectors : position and the velocity of the "target" object. Each vector has the same length as JD0 and contains a single component of the position or velocity. 
            
            JD0 and time should have the same length.
            

           @param JD0 (in) reference time (could be 0). It could be a scalar, list or 1D numpy's array.
           @param time (in) time elapsed from JD0. It could be a scalar, list or 1D numpy's array.
           @param target (in) "target" object 
           @param center (in) "center" object """
                                 
        self.__check_chandle_null()
        if self.__isarray_and_samesize(JD0, time) :
            return self.__vector_compute(JD0, time, target, center)
        else:
            return self.__scalar_compute(JD0, time, target, center)
            


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __vector_compute_unit(self, JD0, time, target, center, unit):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
        for a given target and center  at the specified time 
        (time elapsed from JD0).
        The output is expressed according to unit.
 
        return a list of 6 vectors : position and the velocity of the "target" object.
        Each vector has the same length as JD0 and contains a single component of the position or velocity. 

        @param JD0 (in) vector of reference time (could be 0)
        @param time (in) vector of time elapsed from JD0
        @param target (in) "target" object 
        @param center (in) "center" object 
        @param unit (in) sum of CALCEPH_UNIT_???"""
                                 
        n = len(JD0)
        cdef double lPV[6]
        vPV = numpy.zeros(6*n, dtype=numpy.float64)
        for j in range(n):
            res = calcephpy.calceph_compute_unit(self._c_handle, JD0[j], time[j], target, center, unit, lPV)
            self.__check_returnerror_0(res)
            vPV[6*j:6*j+6] = lPV 
        return self.__exportresult(vPV, 6, JD0)

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __scalar_compute_unit(self, JD0, time, target, center, unit):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
        for a given target and center  at the specified time 
        (time elapsed from JD0).
        The output is expressed according to unit.
 
        return a list of 6 elements : position and the velocity of the "target" object.

        @param JD0 (in) reference time (could be 0)
        @param time (in) time elapsed from JD0
        @param target (in) "target" object 
        @param center (in) "center" object 
        @param unit (in) sum of CALCEPH_UNIT_???"""
                                 
        cdef double PV[6]
        res = calcephpy.calceph_compute_unit(self._c_handle, JD0, time, target, center, unit, PV)
        self.__check_returnerror_0(res)
        return PV    

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef compute_unit(self, JD0, time, target, center, unit):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
        for a given target and center  at the given time 
        (time elapsed from JD0).
        The output is expressed according to unit.
 
        If JD0 is a scalar, it returns a list of 6 elements : position and the velocity of the "target" object.
        If JD0 is a list or numpy's array, it returns a list of 6 vectors : position and the velocity of the "target" object. Each vector has the same length as JD0 and contains a single component of the position or velocity. 

        @param JD0 (in) reference time (could be 0). It could be a scalar, list or 1D numpy's array.
        @param time (in) time elapsed from JD0. It could be a scalar, list or 1D numpy's array.
        @param target (in) "target" object 
        @param center (in) "center" object 
        @param unit (in) sum of CALCEPH_UNIT_???"""
                                
        self.__check_chandle_null()
        if self.__isarray_and_samesize(JD0, time) :
            return self.__vector_compute_unit(JD0, time, target, center, unit)
        else:
            return self.__scalar_compute_unit(JD0, time, target, center, unit)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __vector_orient_unit(self, JD0, time, target, unit):
        """Return the orientations of the object "target" for a vector of times 
        (time elapsed from JD0).
        The output is expressed according to unit.
 
        return a list of 6 elements : orientation (euler angles and their derivatives) of the "target" object.
        return a list of 6 vectors : orientation (euler angles and their derivatives) of the "target" object.
        Each vector has the same length as JD0 and contains a single component of the orientation.

        @param JD0 (in) vector of reference time (could be 0)
        @param time (in) vector of time elapsed from JD0
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_??? and OUTPUT_???"""
                                 
        n = len(JD0)
        cdef double lPV[6]
        vPV = numpy.zeros(6*n, dtype=numpy.float64)
        for j in range(n):
            res = calcephpy.calceph_orient_unit(self._c_handle, JD0[j], time[j], target, unit, lPV)
            self.__check_returnerror_0(res)
            vPV[6*j:6*j+6] = lPV 
        return self.__exportresult(vPV, 6, JD0)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __scalar_orient_unit(self, JD0, time, target, unit):
        """Return the orientation of the object "target"  at the specified time 
        (time elapsed from JD0).
        The output is expressed according to unit.
 
        return a list of 6 elements : orientation (euler angles and their derivatives) of the "target" object.

        @param JD0 (in) reference time (could be 0)
        @param time (in) time elapsed from JD0
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_??? and OUTPUT_???"""
                                 
        cdef double PV[6]
        res = calcephpy.calceph_orient_unit(self._c_handle, JD0, time, target, unit, PV)
        self.__check_returnerror_0(res)
        return PV    


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef orient_unit(self, JD0, time, target, unit):
        """Return the orientation of the object "target"  at the specified time 
        (time elapsed from JD0).
        The output is expressed according to unit.
 
        If JD0 is a scalar, it returns a list of 6 elements : orientation (euler angles and their derivatives) of the "target" object.
        If JD0 is a list or numpy's array, it returns a list of 6 vectors : orientation (euler angles and their derivatives) of the "target" object. Each vector has the same length as JD0 and contains a single component of the position or velocity. 
        
        JD0 and time should have the same length.
        

        @param JD0 (in) reference time (could be 0). It could be a scalar, list or 1D numpy's array.
        @param time (in) time elapsed from JD0. It could be a scalar, list or 1D numpy's array.

        @param JD0 (in) reference time (could be 0)
        @param time (in) time elapsed from JD0
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_??? and OUTPUT_???"""
                                 
                                    
        self.__check_chandle_null()
        if self.__isarray_and_samesize(JD0, time) :
            return self.__vector_orient_unit(JD0, time, target, unit)
        else:
            return self.__scalar_orient_unit(JD0, time, target, unit)

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef rotangmom_unit(self, JD0, time, target, unit):
        """Return the rotional angular momentum (G/(mR^2)) of the object "target"  at the specified time 
        (time elapsed from JD0).
        The output is expressed according to unit.
 
        return a list of 6 elements : rotional angular momentum  and their first derivatives of the "target" object.

        @param JD0 (in) reference time (could be 0)
        @param time (in) time elapsed from JD0
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_???"""
                                 
        self.__check_chandle_null()
        cdef double PV[6]
        res = calcephpy.calceph_rotangmom_unit(self._c_handle, JD0, time, target, unit, PV)
        self.__check_returnerror_0(res)
        return PV    

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __vector_compute_order(self, JD0, time, target, center, unit, order):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
        for a given target and center for  a vector of time
        (time elapsed from JD0).
        The output is expressed according to unit.
        The vector JD0 and time must have the same length.
        
        return a list of 3*(order+1) vectors of floating-point numbers.
        This list contains the positions and their derivatives of the "target" object
        Each vector has the same length as JD0 and contains a single component of the position or its derivatives.
 
        @param JD0 (in) vector of reference time (could be 0)
        @param time (in) vector of time elapsed from JD0
        @param target (in) "target" object 
        @param center (in) "center" object 
        @param unit (in) sum of CALCEPH_UNIT_???
        @param order (in) order of the computation
        =0 : Positions are computed
        =1 : Position+Velocity are computed
        =2 : Position+Velocity+Acceleration are computed
        =3 : Position+Velocity+Acceleration+Jerk are computed."""
                                 
        n = len(JD0)
        ncomp = 3*(order+1)
        cdef double lPV[12]
        vPV = numpy.zeros(ncomp*n, dtype=numpy.float64)
        lPV12 = numpy.zeros(12, dtype=numpy.float64)
        for j in range(n):
            res = calcephpy.calceph_compute_order(self._c_handle, JD0[j], time[j], target, center, unit, order, lPV)
            self.__check_returnerror_0(res)
            lPV12 = lPV
            vPV[ncomp*j:ncomp*j+ncomp] = lPV12[:ncomp]
        return self.__exportresult(vPV, ncomp, JD0)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __scalar_compute_order(self, JD0, time, target, center, unit, order):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
        for a given target and center  at the specified time
        (time elapsed from JD0).
        The output is expressed according to unit.
        
        return a list of 3*(order+1) floating-point numbers.
        This list contains the positions and their derivatives of the "target" object
 
        @param JD0 (in) reference time (could be 0)
        @param time (in) time elapsed from JD0
        @param target (in) "target" object 
        @param center (in) "center" object 
        @param unit (in) sum of CALCEPH_UNIT_???
        @param order (in) order of the computation
        =0 : Positions are computed
        =1 : Position+Velocity are computed
        =2 : Position+Velocity+Acceleration are computed
        =3 : Position+Velocity+Acceleration+Jerk are computed."""
                                 
        cdef double PV[12]
        res = calcephpy.calceph_compute_order(self._c_handle, JD0, time, target, center, unit, order, PV)
        self.__check_returnerror_0(res)
        return [PV[i] for i in range(0,3*(order+1)) ]   


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef compute_order(self, JD0, time, target, center, unit, order):
        """compute the position <x,y,z> and velocity <xdot,ydot,zdot>
        for a given target and center  at the specified time
        (time elapsed from JD0).
        The output is expressed according to unit.
         
        If JD0 is a scalar, it returns a list of 3*(order+1) floating-point numbers.
        This list contains the positions and their derivatives of the "target" object.

        If JD0 is a list or numpy's array, it returns a list of 3*(order+1) vectors.
        Each vector has the same length as JD0 and contains a single component of the positions and their derivatives. 
            
        JD0 and time should have the same length.
            

        @param JD0 (in) reference time (could be 0). It could be a scalar, list or 1D numpy's array.
        @param time (in) time elapsed from JD0. It could be a scalar, list or 1D numpy's array.
        @param target (in) "target" object 
        @param center (in) "center" object 
        @param unit (in) sum of CALCEPH_UNIT_???
        @param order (in) order of the computation
        =0 : Positions are computed
        =1 : Position+Velocity are computed
        =2 : Position+Velocity+Acceleration are computed
        =3 : Position+Velocity+Acceleration+Jerk are computed."""
                                 
        self.__check_chandle_null()
        if self.__isarray_and_samesize(JD0, time) :
            return self.__vector_compute_order(JD0, time, target, center, unit, order)
        else:
            return self.__scalar_compute_order(JD0, time, target, center, unit, order)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __vector_orient_order(self, JD0, time, target, unit, order):
        """Return the orientation of the object "target" for a vector of time
        (time elapsed from JD0).
        The output is expressed according to unit.
        
        return a list of 3*(order+1) vectors of floating-point numbers.
        This list contains the orientation (euler angles and their derivatives) of the "target" object.
        Each vector has the same length as JD0 and contains a single component of the orientation.
 
        @param JD0 (in) vector of reference time (could be 0)
        @param time (in) vector of time elapsed from JD0
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_??? and OUTPUT_???
        @param order (in) order of the computation
         =0 : orientations are computed
         =1 : orientations and their first derivatives are computed
         =2 : orientations and their first,second derivatives are computed
         =3 : orientations and their first, second, third derivatives are computed."""
                                 
        n = len(JD0)
        ncomp = 3*(order+1)
        cdef double lPV[12]
        vPV = numpy.zeros(ncomp*n, dtype=numpy.float64)
        lPV12 = numpy.zeros(12, dtype=numpy.float64)
        for j in range(n):
            res = calcephpy.calceph_orient_order(self._c_handle, JD0[j], time[j], target, unit, order, lPV)
            self.__check_returnerror_0(res)
            lPV12 = lPV
            vPV[ncomp*j:ncomp*j+ncomp] = lPV12[:ncomp]
        return self.__exportresult(vPV, ncomp, JD0)

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef __scalar_orient_order(self, JD0, time, target, unit, order):
        """Return the orientation of the object "target" at the specified time
        (time elapsed from JD0).
        The output is expressed according to unit.
        
        return a list of 3*(order+1) floating-point numbers.
        This list contains the orientation (euler angles and their derivatives) of the "target" object
 
        @param JD0 (in) reference time (could be 0)
        @param time (in) time elapsed from JD0
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_??? and OUTPUT_???
        @param order (in) order of the computation
         =0 : orientations are computed
         =1 : orientations and their first derivatives are computed
         =2 : orientations and their first,second derivatives are computed
         =3 : orientations and their first, second, third derivatives are computed."""
                                 
        self.__check_chandle_null()
        cdef double PV[12]
        res = calcephpy.calceph_orient_order(self._c_handle, JD0, time, target, unit, order, PV)
        self.__check_returnerror_0(res)
        return [PV[i] for i in range(0,3*(order+1)) ]   

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef orient_order(self, JD0, time, target, unit, order):
        """Return the orientation of the object "target" at the specified time
        (time elapsed from JD0).
        The output is expressed according to unit.
         
        If JD0 is a scalar, it returns a list of 3*(order+1) floating-point numbers.
        This list contains the orientation (euler angles or nutation angles and their derivatives) of the "target" object

        If JD0 is a list or numpy's array, it returns a list of 3*(order+1) vectors.
        Each vector has the same length as JD0 and contains a single component of the orientation (euler angles or nutation angles and their derivatives) . 
            
        JD0 and time should have the same length.
            

        @param JD0 (in) reference time (could be 0). It could be a scalar, list or 1D numpy's array.
        @param time (in) time elapsed from JD0. It could be a scalar, list or 1D numpy's array.
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_??? and OUTPUT_???
        @param order (in) order of the computation
         =0 : orientations are computed
         =1 : orientations and their first derivatives are computed
         =2 : orientations and their first,second derivatives are computed
         =3 : orientations and their first, second, third derivatives are computed."""
                                 
        self.__check_chandle_null()
        if self.__isarray_and_samesize(JD0, time) :
            return self.__vector_orient_order(JD0, time, target, unit, order)
        else:
            return self.__scalar_orient_order(JD0, time, target, unit, order)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef rotangmom_order(self, JD0, time, target, unit, order):
        """Return the rotional angular momentum (G/(mR^2)) of the object "target" at the specified time
        (time elapsed from JD0).
        The output is expressed according to unit.
        
        return a list of 3*(order+1) floating-point numbers.
        This list contains the rotional angular momentum (G/(mR^2)) and their derivatives of the "target" object
 
        @param JD0 (in) reference time (could be 0)
        @param time (in) time elapsed from JD0
        @param target (in) "target" object 
        @param unit (in) sum of CALCEPH_UNIT_???
        @param order (in) order of the computation
          =0 : (G/mR^2) are computed
          =1 : (G/mR^2) and their first derivatives are computed
          =2 : (G/mR^2) and their first,second derivatives  are computed
          =3 : (G/mR^2) and their first, second, third derivatives are computed."""
                                 
        self.__check_chandle_null()
        cdef double PV[12]
        res = calcephpy.calceph_rotangmom_order(self._c_handle, JD0, time, target, unit, order, PV)
        self.__check_returnerror_0(res)
        return [PV[i] for i in range(0,3*(order+1)) ]   


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getconstant(self, name):
        """get constant value from the specified name in the ephemeris file
    
              name (in) name of the constant
        """
        return self.getconstantsd(name)

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getconstantsd(self, name):
        """get first value from the specified name in the ephemeris file
    
              name (in) name of the constant
        """
        self.__check_chandle_null()
        cdef double val[1]
        py_byte_name = name.encode('ascii')
        cdef char* c_name = py_byte_name
        res = calcephpy.calceph_getconstantsd(self._c_handle, c_name, val)
        self.__check_returnerror_0(res)
        return val[0]    

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getconstantvd(self, name):
        """get all values associated from the specified name in the ephemeris file
    
              name (in) name of the constant
        """
        self.__check_chandle_null()
        cdef double val[1]
        py_byte_name = name.encode('ascii')
        cdef char* c_name = py_byte_name
        res = calcephpy.calceph_getconstantsd(self._c_handle, c_name, val)
        if (res>1):
            arval = <double*>PyMem_Malloc(res * sizeof(double))
            if not arval:
                raise MemoryError()
            res = calcephpy.calceph_getconstantvd(self._c_handle, c_name, arval, res)
            self.__check_returnerror_0(res)
            vlist = [arval[i] for i in range(0, res)]
            PyMem_Free(arval)
            return vlist
        else:
            self.__check_returnerror_0(res)
            return [val[0]]    

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getconstantss(self, name):
        """get first value from the specified name in the ephemeris file
    
              name (in) name of the constant
        """
        self.__check_chandle_null()
        cdef char c_val[1024]
        py_byte_name = name.encode('ascii')
        cdef char* c_name = py_byte_name
        res = calcephpy.calceph_getconstantss(self._c_handle, c_name, c_val)
        self.__check_returnerror_0(res)
        val = c_val.decode('ascii')
        return val    

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getconstantvs(self, name):
        """get all values associated from the specified name in the ephemeris file
    
              name (in) name of the constant
        """
        self.__check_chandle_null()
        cdef char c_val[1024]
        py_byte_name = name.encode('ascii')
        cdef char* c_name = py_byte_name
        res = calcephpy.calceph_getconstantss(self._c_handle, c_name, c_val)
        if (res>1):
            arval = <char[1024]*>PyMem_Malloc(res * sizeof(char)*1024)
            if not arval:
                raise MemoryError()
            res = calcephpy.calceph_getconstantvs(self._c_handle, c_name, arval, res)
            self.__check_returnerror_0(res)
            vlist = [arval[i].decode('ascii') for i in range(0, res)]
            PyMem_Free(arval)
            return vlist
        else:
            self.__check_returnerror_0(res)
            val = c_val.decode('ascii')
            return [val]    


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getconstantcount(self):
        """Return the number of constants available in the ephemeris file"""
        self.__check_chandle_null()
        return calcephpy.calceph_getconstantcount(self._c_handle)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getconstantindex(self, index):
        """return the name and the associated value of the constant available at some index in the ephemeris file
           The value of index must be between 1 and getconstantcount().
    
              index (in) index of the constant. 
        """
        self.__check_chandle_null()
        cdef double cval[1]
        cdef char cname[33]
        res = calcephpy.calceph_getconstantindex(self._c_handle, index, cname, cval)
        self.__check_returnerror_0(res)
        name = cname.decode('ascii')    
        val = cval[0]
        return (name, val) 

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getidbyname(self, name, unit):
        """get the id of the body from the specified name in the ephemeris file
    
              name (in) name of the body
              unit (in) unit of the id
        """
        self.__check_chandle_null()
        cdef int cid[1]
        py_byte_name = name.encode('ascii')
        cdef char* c_name = py_byte_name
        res = calcephpy.calceph_getidbyname(self._c_handle, c_name, unit, cid)
        if (res == 0):
            id = None
        else:    
            id = cid[0]
        return id 


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getnamebyidss(self, id, unit):
        """get the first name of the body from the specified identification number in the ephemeris file
    
              id (in) identification number of the body
              unit (in) unit of the id
        """
        self.__check_chandle_null()
        cdef char c_val[1024]
        cdef int c_id
        c_id = id
        cdef int c_unit
        c_unit = unit
        res = calcephpy.calceph_getnamebyidss(self._c_handle, c_id, c_unit, c_val)
        if (res == 0):
            val = None
        else:    
            val = c_val.decode('ascii')
        return val 



# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getpositionrecordcount(self):
        """return the number of position’s records available in the ephemeris file"""
        self.__check_chandle_null()
        return calcephpy.calceph_getpositionrecordcount(self._c_handle)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getpositionrecordindex(self, index):
        """return the target and origin bodies, the first and last time, and the reference frame available at the
specified index for the position's records of the ephemeris file.
           The value of index must be between 1 and getpositionrecordcount().
    
              index (in) index of the constant. 
        """
        self.__check_chandle_null()
        cdef int ctarget[1]
        cdef int ccenter[1]
        cdef double cfirsttime[1]
        cdef double clasttime[1]
        cdef int cframe[1]
        res = calcephpy.calceph_getpositionrecordindex(self._c_handle, index, ctarget, ccenter, cfirsttime, clasttime, cframe)
        self.__check_returnerror_0(res)
        target = ctarget[0]
        center = ccenter[0]
        firsttime = cfirsttime[0]
        lasttime = clasttime[0]
        frame = cframe[0]
        return (target, center, firsttime, lasttime, frame) 

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getpositionrecordindex2(self, index):
        """return the target and origin bodies, the first and last time, the reference frame and the segment type available at the
specified index for the position's records of the ephemeris file.
           The value of index must be between 1 and getpositionrecordcount().
    
              index (in) index of the constant. 
        """
        self.__check_chandle_null()
        cdef int ctarget[1]
        cdef int ccenter[1]
        cdef double cfirsttime[1]
        cdef double clasttime[1]
        cdef int cframe[1]
        cdef int csegtype[1]
        res = calcephpy.calceph_getpositionrecordindex2(self._c_handle, index, ctarget, ccenter, cfirsttime, clasttime, cframe, csegtype)
        self.__check_returnerror_0(res)
        target = ctarget[0]
        center = ccenter[0]
        firsttime = cfirsttime[0]
        lasttime = clasttime[0]
        frame = cframe[0]
        segid = csegtype[0]
        return (target, center, firsttime, lasttime, frame, segid) 

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getorientrecordcount(self):
        """return the number of orientation’s records available in the ephemeris file"""
        self.__check_chandle_null()
        return calcephpy.calceph_getorientrecordcount(self._c_handle)


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getorientrecordindex(self, index):
        """return the target and origin bodies, the first and last time, and the reference frame available at the
specified index for the orientation's records of the ephemeris file.
           The value of index must be between 1 and getorientrecordcount().
    
              index (in) index of the constant. 
        """
        self.__check_chandle_null()
        cdef int ctarget[1]
        cdef double cfirsttime[1]
        cdef double clasttime[1]
        cdef int cframe[1]
        res = calcephpy.calceph_getorientrecordindex(self._c_handle, index, ctarget, cfirsttime, clasttime, cframe)
        self.__check_returnerror_0(res)
        target = ctarget[0]
        firsttime = cfirsttime[0]
        lasttime = clasttime[0]
        frame = cframe[0]
        return (target, firsttime, lasttime, frame) 

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getorientrecordindex2(self, index):
        """return the target and origin bodies, the first and last time, the reference frame, and the segment type available at the
specified index for the orientation's records of the ephemeris file.
           The value of index must be between 1 and getorientrecordcount().
    
              index (in) index of the constant. 
        """
        self.__check_chandle_null()
        cdef int ctarget[1]
        cdef double cfirsttime[1]
        cdef double clasttime[1]
        cdef int cframe[1]
        cdef int csegtype[1]
        res = calcephpy.calceph_getorientrecordindex2(self._c_handle, index, ctarget, cfirsttime, clasttime, cframe, csegtype)
        self.__check_returnerror_0(res)
        target = ctarget[0]
        firsttime = cfirsttime[0]
        lasttime = clasttime[0]
        frame = cframe[0]
        segid = csegtype[0]
        return (target, firsttime, lasttime, frame, segid) 


# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef gettimescale(self):
        """Return the time scale of the ephemeris file"""
        self.__check_chandle_null()
        return calcephpy.calceph_gettimescale(self._c_handle)

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef gettimespan(self):
        """Return the time span of the ephemeris file"""
        self.__check_chandle_null()
        cdef double firsttime[1]
        cdef double lasttime[1]
        cdef int continuous[1]
        res = calcephpy.calceph_gettimespan(self._c_handle, firsttime, lasttime, continuous)
        self.__check_returnerror_0(res)
        pfirsttime = firsttime[0]
        plasttime = lasttime[0]
        pcontinuous = continuous[0]
        return (pfirsttime, plasttime, pcontinuous)

# /*-----------------------------------------------------------------*/
# /*-----------------------------------------------------------------*/
    cpdef getfileversion(self):
        """return the file version of the ephemeris file"""
        self.__check_chandle_null()
        cdef char cname[1024]
        calcephpy.calceph_getfileversion(self._c_handle, cname)
        name = cname.decode('ascii')
        return name


# /*-----------------------------------------------------------------*/
# /* maxsupportedderivativeorder */
# /*-----------------------------------------------------------------*/
def getmaxsupportedorder(idseg):
    """return the maximal supported derivate order for the segment"""
    cdef int iseg
    iseg = idseg
    order = calcephpy.calceph_getmaxsupportedorder(iseg)
    return order


# /*-----------------------------------------------------------------*/
# /* error handler */
# /*-----------------------------------------------------------------*/
def seterrorhandler(typehandler, userfunc):
    """set the error handler """
    global __userfuncerrorhandler_python, __usertypehandler_python
    __userfuncerrorhandler_python = userfunc
    __usertypehandler_python = typehandler
    calcephpy.calceph_seterrorhandler(typehandler, __callbackerrorhandler)
        
# /*-----------------------------------------------------------------*/
# /* version */
# /*-----------------------------------------------------------------*/
def getversion_str():
    """return the version of the library as a string"""
    cdef char cname[33]
    calcephpy.calceph_getversion_str(cname)
    name = cname.decode('ascii')
    return name


# /*-----------------------------------------------------------------*/
#  python error callback for calceph_seterrorhandler(3,...)
# /*-----------------------------------------------------------------*/
cdef void __callbackerrorhandler(const char *msg):
    __userfuncerrorhandler_python(msg.decode('utf-8'))
    
# default initialization of the kind of error handler
__usertypehandler_python = 1

