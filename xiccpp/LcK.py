
the_year = '2016'
polarity = 'MD'

if ((the_year == '2015') | (the_year == '2016')):
    rootInTES = '/Event/Turbo'
#    rootInTES = '/Event/AllStreams'
#     rootInTES = '/Event'

## (1) read data from Turbo:
from PhysConf.Selections import Selection
from PhysConf.Selections import AutomaticData
from PhysConf.Selections import PrescaleSelection, PrescaleEventSelection, MergedSelection

## I.3.1   IMPOTANT: need to rebuild it!!
from StandardParticles import StdAllNoPIDsKaons as kaons
from PhysConf.Selections import RebuildSelection

the_line  = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'

Lc = AutomaticData(the_line)

#kaons.algorithm().RootInTES = '/Event'

kaons = RebuildSelection ( kaons )
################################################### 
## (6) build the final selection sequence
from PhysConf.Selections import SelectionSequence
seq0 = SelectionSequence('SEQ0', Lc )
seq1 = SelectionSequence('SEQ1', kaons )

## (7) configure DaVinci
from Configurables import DaVinci ,  TurboConf
#TurboConf().RunPersistRecoUnpacking = True
dv = DaVinci(
    PrintFreq  = 25000          ,
    DataType   = the_year       ,
    InputType  = 'MDST'         , ## ATTENTION! 
    RootInTES  = rootInTES      , ## ATTENTION! 
    ##
    #EventPreFilters = fltrs.filters('FILTER') , 
    #Lumi       = True           , 
    Simulation = True          ,
    ## 
    TupleFile  = 'LcK_Turbo_240118_MC.root'   , 
    Turbo      = True      
 )

#TurboConf().RunPersistRecoUnpacking = True

## (8) insert our sequence into DaVinci 
dv.UserAlgorithms = [ seq0.sequence(), seq1.sequence()]

## (9) number of event and input data

dv.EvtMax = 10000

# 2016
if the_year == "2016":
    if polarity == "MD":
        dv.CondDBtag = "sim-20161124-2-vc-md100"
        dv.DDDBtag   = "dddb-20150724"
    if polarity == "MU":
        dv.CondDBtag = "sim-20161124-2-vc-mu100"
        dv.DDDBtag   = "dddb-20150724"

from GaudiConf import IOHelper
# Use the local input data
IOHelper().inputFiles([
    '/tmp/mpappaga/00061410_00000194_7.AllStreams.dst',
    '/tmp/mpappaga/00061410_00000241_7.AllStreams.dst',
    '/tmp/mpappaga/00061410_00000248_7.AllStreams.dst',
    '/tmp/mpappaga/00061410_00000294_7.AllStreams.dst'
#    'PFN:root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2016/ALLSTREAMS.DST/00061410/0000/00061410_00000194_7.AllStreams.dst'
    ], clear=True)


#from Configurables import DataOnDemandSvc
#
#dod = DataOnDemandSvc()
#from Configurables import Gaudi__DataLink as Link
#for  name , target , what  in [
##    ( 'LinkHlt2Tracks' , '/Event/Turbo/Hlt2/TrackFitted/Long' , '/Event/Hlt2/TrackFitted/Long'     ) ,
##    ( 'LinkDAQ'        , '/Event/Turbo/DAQ'                   , '/Event/DAQ'                       ) ,
##    ( 'LinkPPs'        , '/Event/Turbo/Rec/ProtoP/Charged'    , '/Event/Turbo/Hlt2/Protos/Charged' ) ,
#    ( 'LinkPPs'        , '/Event/Turbo/Rec/Track/Best'         , '/Event/Rec/Track/Best' ) ,    
#    ] :
#    dod.AlgMap [ target ] = Link ( name , Target = target , What = what , RootInTES = '' )
