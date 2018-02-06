import os, re
from math import ceil
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--era', metavar='F', type='string', action='store',
                  dest='era',
                  help='Input era')
parser.add_option('-o','--output', metavar='F', type='string', action='store',
                  dest='output',
                  help='Output path')

(options, args) = parser.parse_args()

ERA = options.era
OPATH = options.output
if not OPATH.endswith('/'):
    OPATH+='/'

if ERA is None:
    raise Exception("You must specify an era with --era")
if OPATH is None:
    raise Exception("You must specify an output pat with --output")
    
if not os.path.exists(OPATH):
    raise Exception("No path named %r found." % (OPATH))

doSynchtest = True
doSynchfit  = True
doSynchplot = True
doApplyJEC  = False
doJRA       = False
doJRF       = False
doJRAR      = False
doJCA       = False
doJDCTR     = False

print "Configuration:"
print "\tjet_synchtest_x ... " + ("on" if doSynchtest else "off")
print "\tjet_synchfit_x ... " + ("on" if doSynchfit else "off")
print "\tjet_synchplot_x ... " + ("on" if doSynchplot else "off")
print "\tjet_apply_jec_x ... " + ("on" if doApplyJEC else "off")
print "\tjet_response_analyzer_x ... " + ("on" if doJRA else "off")
print "\tjet_response_fitter_x ... " + ("on" if doJRF else "off")
print "\tjet_response_and_resolution_x ... " + ("on" if doJRAR else "off")
print "\tjet_correction_analyzer_x ... " + ("on" if doJCA else "off")
print "\tjet_draw_corrections_TDR_ratio_x ... " + ("on" if doJDCTR else "off")

algorithms = []
upperAlgorithms = []
all_alg = ""
all_alg_size = ""

algsizetype = {'ak':[4,8]}
jettype = ['pf','pfchs','puppi']
corrs = ['']

for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            for c in corrs:
                algorithms.append(str(k+str(s)+j+c))
                upperAlgorithms.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs")))
                all_alg += algorithms[-1]+" "
                all_alg_size += algorithms[-1]+":"+("%.3f" % float(s/20.0))+" "

template1='templates/batchInputJetSynchtestALGO_CORRECTIONLEVEL.txt'
template2='templates/batchInputJetSynchfitALGO_CORRECTIONLEVEL.txt'
template3='templates/batchInputJetSynchplotALGO_CORRECTIONLEVEL.txt'
template4='templates/batchInputJetApplyJECALGO_CORRECTIONLEVEL.txt'
template5='templates/batchInputJetCorrectionAnalyzerALGO_CORRECTIONLEVEL.txt'
template6='templates/batchInputJetDrawCorrectionsTDRRatioALGO_CORRECTIONLEVEL.txt'
template7='templates/batchInputJetResponseAnalyzerJOB_CORRECTIONLEVEL.txt'
template8='templates/batchInputJetResponseFitterJOB_CORRECTIONLEVEL.txt'
template8='templates/batchInputJetResponseAndResolutionJOB_CORRECTIONLEVEL.txt'

print "Doing files for all algorithms ..."
if doJRA:
    #To derive L2L3 corrections
    config7=OPATH+'batchInputJetResponseAnalyzer0_0.txt'
    os.system('cp '+template7+' '+config7)
    os.system('sed s%ALGORITHMS%\"'+all_alg_size+'\"%g '+config7+' --in-place')
    os.system('sed s%NBINSETARSP%0%g '+config7+' --in-place')
    os.system('sed s%NBINSPHIRSP%0%g '+config7+' --in-place')
    os.system('sed s%DOFLAVOR%false%g '+config7+' --in-place')
    os.system('sed s%NREFMAX%0%g '+config7+' --in-place')
    os.system('sed s%USEWEIGHT%false%g '+config7+' --in-place')
    os.system('sed s%OUTPUTPATH%'+OPATH+'correctionL2L3/jra.root'+'%g '+config7+' --in-place')

    #To plot the final resolution
    config7=OPATH+'batchInputJetResponseAnalyzer0_1.txt'
    os.system('cp '+template7+' '+config7)
    os.system('sed s%ALGORITHMS%\"'+all_alg_size+'\"%g '+config7+' --in-place')
    os.system('sed s%NBINSETARSP%100%g '+config7+' --in-place')
    os.system('sed s%NBINSPHIRSP%100%g '+config7+' --in-place')
    os.system('sed s%DOFLAVOR%false%g '+config7+' --in-place')
    os.system('sed s%NREFMAX%2%g '+config7+' --in-place')
    os.system('sed s%USEWEIGHT%true%g '+config7+' --in-place')
    os.system('sed s%OUTPUTPATH%'+OPATH+'resolutionL1L2L3/jra.root'+'%g '+config7+' --in-place')

if doJRF:
    #To derive L2L3 corrections
    config8=OPATH+'batchInputJetResponseFitter0_0.txt'
    os.system('cp '+template8+' '+config8)
    os.system('sed s%INPUT%'+OPATH+'correctionL2L3/jra.root%g '+config8+' --in-place')
    os.system('sed s%OUTPUT%'+OPATH+'correctionL2L3/jra_f.root%g '+config8+' --in-place')
    os.system('sed s%FITTYPE%0%g '+config8+' --in-place')
    os.system('sed s%DOETARSP%false%g '+config8+' --in-place')
    os.system('sed s%DOPHIRSP%false%g '+config8+' --in-place')

    #To plot the final resolution
    config8=OPATH+'batchInputJetResponseFitter0_1.txt'
    os.system('cp '+template8+' '+config8)
    os.system('sed s%INPUT%'+OPATH+'resolutionL1L2L3/jra.root%g '+config8+' --in-place')
    os.system('sed s%OUTPUT%'+OPATH+'resolutionL1L2L3/jra_f.root%g '+config8+' --in-place')
    os.system('sed s%FITTYPE%1%g '+config8+' --in-place')
    os.system('sed s%DOETARSP%true%g '+config8+' --in-place')
    os.system('sed s%DOPHIRSP%true%g '+config8+' --in-place')

if doJRAR:
    #To plot the final resolution
    config9=OPATH+'batchInputJetResponseAndResolution0_0.txt'
    os.system('cp '+template9+' '+config9)
    os.system('sed s%INPUT%'+OPATH+'resolutionL1L2L3/jra_f.root%g '+config9+' --in-place')
    os.system('sed s%OUTPUT%'+OPATH+'resolutionL1L2L3/jra_f_g.root%g '+config9+' --in-place')
    os.system('sed s%ALGORITHMS%'+all_alg+'%g '+config9+' --in-place')

print "Doing files on per algorithm basis ..."
for ialg, alg in enumerate(algorithms):
    print "\tDoing Algorithm " + alg + " ... "

    if doSynchtest:
        #Synchtest without L1 corrections applied
        config=OPATH+'batchInputJetSynchtest'+str(ialg)+'_0.txt'
        os.system('cp '+template1+' '+config)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config+' --in-place')
        os.system('sed s%APPLYJEC%false%g '+config+' --in-place')
        os.system('sed s%JECTEXTFILE%'+OPATH+ERA+'/'+ERA+'_L1FastJet_'+upperAlgorithms[ialg]+'.txt%g '+config+' --in-place')
        os.system('sed s%OUTPUTPATH%'+OPATH+'correction/'+'%g '+config+' --in-place')
            
        #Synchtest with L1 corrections applied
        config=OPATH+'batchInputJetSynchtest'+str(ialg)+'_1.txt'
        os.system('cp '+template1+' '+config)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config+' --in-place')
        os.system('sed s%APPLYJEC%true%g '+config+' --in-place')
        os.system('sed s%JECTEXTFILE%'+OPATH+ERA+'/'+ERA+'_L1FastJet_'+upperAlgorithms[ialg]+'.txt%g '+config+' --in-place')
        os.system('sed s%OUTPUTPATH%'+OPATH+'correctionL1/'+'%g '+config+' --in-place')

    if doSynchfit:
        config2=OPATH+'batchInputJetSynchfit'+str(ialg)+'_0.txt'
        os.system('cp '+template2+' '+config2)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config2+' --in-place')
        if 'puppi' in alg:
            os.system('sed s%USEPUPPIFUNCTION%true%g '+config2+' --in-place')
        else:
            os.system('sed s%USEPUPPIFUNCTION%false%g '+config2+' --in-place')

    if doSynchplot:
        #Synchplot without L1 corrections applied
        config3=OPATH+'batchInputJetSynchplot'+str(ialg)+'_0.txt'
        os.system('cp '+template3+' '+config3)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config3+' --in-place')
        os.system('sed s%DIR%./%g '+config3+' --in-place')
        os.system('sed s%FIXEDRANGE%false%g '+config3+' --in-place')
            
        #Synchplot with L1 corrections applied
        config3=OPATH+'batchInputJetSynchplot'+str(ialg)+'_1.txt'
        os.system('cp '+template3+' '+config3)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config3+' --in-place')
        os.system('sed s%DIR%./%g '+config3+' --in-place')
        os.system('sed s%FIXEDRANGE%true%g '+config3+' --in-place')

    if doApplyJEC:
        #Applying the L1 corrections
        config4=OPATH+'batchInputJetApplyJEC'+str(ialg)+'_0.txt'
        os.system('cp '+template4+' '+config4)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config4+' --in-place')
        os.system('sed s%LEVELS%1%g '+config4+' --in-place')

        #Appplying the L2L3 corrections
        config4=OPATH+'batchInputJetApplyJEC'+str(ialg)+'_1.txt'
        os.system('cp '+template4+' '+config4)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config4+' --in-place')
        os.system('sed \"s%LEVELS%2 3%g\" '+config4+' --in-place')

        #Apply the L1+L2L3 corrections
        config4=OPATH+'batchInputJetApplyJEC'+str(ialg)+'_2.txt'
        os.system('cp '+template4+' '+config4)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config4+' --in-place')
        os.system('sed \"s%LEVELS%1 2 3%g\" '+config4+' --in-place')

    if doJCA:
        config5=OPATH+'batchInputJetCorrectionAnalyzer'+str(ialg)+'_0.txt'
        os.system('cp '+template5+' '+config5)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config5+' --in-place')
        os.system('sed s%DRMAX%'+str(float(re.findall(r'\d+', alg)[0])/20.0)+'%g '+config5+' --in-place')

    if doJDCTR:
        config6=OPATH+'batchInputJetDrawCorrectionsTDRRatio'+str(ialg)+'_0.txt'
        os.system('cp '+template6+' '+config6)
        os.system('sed s%ALGORITHM%'+alg+'%g '+config6+' --in-place')
