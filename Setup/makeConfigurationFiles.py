import os, sys, re, argparse
from math import ceil
from textwrap import dedent
from collections import namedtuple

'''
From http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text
and https://bitbucket.org/ruamel/std.argparse
'''
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

def checks(args):
    if not args.output.endswith('/'):
        args.output+='/'
    if args.era is None:
        raise Exception("You must specify an era with --era")
    if args.output is None:
        raise Exception("You must specify an output pat with --output")
    if not os.path.exists(args.output):
        raise Exception("No path named %r found." % (args.output))    

def printOnOff(args):
    print "Configuration:"
    print "\tjet_synchtest_x ... " + ("on" if args.doSynchtest else "off")
    print "\tjet_synchfit_x ... " + ("on" if args.doSynchfit else "off")
    print "\tjet_synchplot_x ... " + ("on" if args.doSynchplot else "off")
    print "\tjet_apply_jec_x ... " + ("on" if args.doApplyJEC else "off")
    print "\tjet_response_analyzer_x ... " + ("on" if args.doJRA else "off")
    print "\tjet_response_fitter_x ... " + ("on" if args.doJRF else "off")
    print "\tjet_response_and_resolution_x ... " + ("on" if args.doJRAR else "off")
    print "\tjet_correction_analyzer_x ... " + ("on" if args.doJCA else "off")
    print "\tjet_draw_corrections_TDR_ratio_x ... " + ("on" if args.doJDCTR else "off")

def algorithm_information():
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
    alg_info = namedtuple('alg_info', 'all_alg all_alg_size algorithms upperAlgorithms')
    return alg_info(all_alg, all_alg_size, algorithms, upperAlgorithms)

def main(args):
    checks(args)
    printOnOff(args)
    alg_info = algorithm_information()

    templateBasePath = '/fdata/hepx/store/user/aperloff/JEC/'
    template1=templateBasePath+'templates/batchInputJetSynchtestALGO_CORRECTIONLEVEL.txt'
    template2=templateBasePath+'templates/batchInputJetSynchfitALGO_CORRECTIONLEVEL.txt'
    template3=templateBasePath+'templates/batchInputJetSynchplotALGO_CORRECTIONLEVEL.txt'
    template4=templateBasePath+'templates/batchInputJetApplyJECALGO_CORRECTIONLEVEL.txt'
    template5=templateBasePath+'templates/batchInputJetCorrectionAnalyzerALGO_CORRECTIONLEVEL.txt'
    template6=templateBasePath+'templates/batchInputJetDrawCorrectionsTDRRatioALGO_CORRECTIONLEVEL.txt'
    template7=templateBasePath+'templates/batchInputJetResponseAnalyzerJOB_CORRECTIONLEVEL.txt'
    template8=templateBasePath+'templates/batchInputJetResponseFitterJOB_CORRECTIONLEVEL.txt'
    template8=templateBasePath+'templates/batchInputJetResponseAndResolutionJOB_CORRECTIONLEVEL.txt'
    
    print "Doing files for all algorithms ..."
    if args.doJRA:
        #To derive L2L3 corrections
        config7=args.output+'batchInputJetResponseAnalyzer0_0.txt'
        os.system('cp '+template7+' '+config7)
        os.system('sed s%ALGORITHMS%\"'+alg_info.all_alg_size+'\"%g '+config7+' --in-place')
        os.system('sed s%NBINSETARSP%0%g '+config7+' --in-place')
        os.system('sed s%NBINSPHIRSP%0%g '+config7+' --in-place')
        os.system('sed s%DOFLAVOR%false%g '+config7+' --in-place')
        os.system('sed s%NREFMAX%0%g '+config7+' --in-place')
        os.system('sed s%USEWEIGHT%false%g '+config7+' --in-place')
        os.system('sed s%OUTPUTPATH%'+args.output+'correctionL2L3/jra.root'+'%g '+config7+' --in-place')
        
        #To plot the final resolution
        config7=args.output+'batchInputJetResponseAnalyzer0_1.txt'
        os.system('cp '+template7+' '+config7)
        os.system('sed s%ALGORITHMS%\"'+alg_info.all_alg_size+'\"%g '+config7+' --in-place')
        os.system('sed s%NBINSETARSP%100%g '+config7+' --in-place')
        os.system('sed s%NBINSPHIRSP%100%g '+config7+' --in-place')
        os.system('sed s%DOFLAVOR%false%g '+config7+' --in-place')
        os.system('sed s%NREFMAX%2%g '+config7+' --in-place')
        os.system('sed s%USEWEIGHT%true%g '+config7+' --in-place')
        os.system('sed s%OUTPUTPATH%'+args.output+'resolutionL1L2L3/jra.root'+'%g '+config7+' --in-place')
        
    if args.doJRF:
        #To derive L2L3 corrections
        config8=args.output+'batchInputJetResponseFitter0_0.txt'
        os.system('cp '+template8+' '+config8)
        os.system('sed s%INPUT%'+args.output+'correctionL2L3/jra.root%g '+config8+' --in-place')
        os.system('sed s%OUTPUT%'+args.output+'correctionL2L3/jra_f.root%g '+config8+' --in-place')
        os.system('sed s%FITTYPE%0%g '+config8+' --in-place')
        os.system('sed s%DOETARSP%false%g '+config8+' --in-place')
        os.system('sed s%DOPHIRSP%false%g '+config8+' --in-place')
        
        #To plot the final resolution
        config8=args.output+'batchInputJetResponseFitter0_1.txt'
        os.system('cp '+template8+' '+config8)
        os.system('sed s%INPUT%'+args.output+'resolutionL1L2L3/jra.root%g '+config8+' --in-place')
        os.system('sed s%OUTPUT%'+args.output+'resolutionL1L2L3/jra_f.root%g '+config8+' --in-place')
        os.system('sed s%FITTYPE%1%g '+config8+' --in-place')
        os.system('sed s%DOETARSP%true%g '+config8+' --in-place')
        os.system('sed s%DOPHIRSP%true%g '+config8+' --in-place')

    if args.doJRAR:
    #To plot the final resolution
        config9=args.output+'batchInputJetResponseAndResolution0_0.txt'
        os.system('cp '+template9+' '+config9)
        os.system('sed s%INPUT%'+args.output+'resolutionL1L2L3/jra_f.root%g '+config9+' --in-place')
        os.system('sed s%OUTPUT%'+args.output+'resolutionL1L2L3/jra_f_g.root%g '+config9+' --in-place')
        os.system('sed s%ALGORITHMS%'+alg_info.all_alg+'%g '+config9+' --in-place')

    print "Doing files on per algorithm basis ..."
    for ialg, alg in enumerate(alg_info.algorithms):
        print "\tDoing Algorithm " + alg + " ... "

        if args.doSynchtest:
            #Synchtest without L1 corrections applied
            config=args.output+'batchInputJetSynchtest'+str(ialg)+'_0.txt'
            os.system('cp '+template1+' '+config)
            os.system('sed s%ALGORITHM%'+alg+'%g '+config+' --in-place')
            os.system('sed s%APPLYJEC%false%g '+config+' --in-place')
            os.system('sed s%JECTEXTFILE%'+args.output+args.era+'/'+args.era+'_L1FastJet_'+alg_info.upperAlgorithms[ialg]+'.txt%g '+config+' --in-place')
            os.system('sed s%OUTPUTPATH%'+args.output+'correction/'+'%g '+config+' --in-place')
            os.system('sed \'/MATCHEDEVENTMAPS/d\' '+config+' --in-place') 
            
            #Synchtest with L1 corrections applied
            config=args.output+'batchInputJetSynchtest'+str(ialg)+'_1.txt'
            os.system('cp '+template1+' '+config)
            os.system('sed s%ALGORITHM%'+alg+'%g '+config+' --in-place')
            os.system('sed s%APPLYJEC%true%g '+config+' --in-place')
            os.system('sed s%JECTEXTFILE%'+args.output+args.era+'/'+args.era+'_L1FastJet_'+alg_info.upperAlgorithms[ialg]+'.txt%g '+config+' --in-place')
            os.system('sed s%OUTPUTPATH%'+args.output+'correctionL1/%g '+config+' --in-place')
            os.system('sed s%MATCHEDEVENTMAPS%'+args.output+'correction/matchedEventsMaps_'+alg+'.root%g '+config+' --in-place')

        if args.doSynchfit:
            config2=args.output+'batchInputJetSynchfit'+str(ialg)+'_0.txt'
            os.system('cp '+template2+' '+config2)
            os.system('sed s%INPUTDIRECTORY%'+args.output+'correction/%g '+config2+' --in-place')
            os.system('sed s%OUTPUTDIRECTORY%'+args.output+'correction/%g '+config2+' --in-place')
            os.system('sed s%ALGORITHM%'+alg+'%g '+config2+' --in-place')
            if 'puppi' in alg:
                os.system('sed s%FUNCTIONTYPE%puppi%g '+config2+' --in-place')
            else:
                os.system('sed s%FUNCTIONTYPE%standard%g '+config2+' --in-place')
            os.system('sed s%ERA%'+args.era+'%g '+config2+' --in-place')

        if args.doSynchplot:
            #Synchplot without L1 corrections applied
            config3=args.output+'batchInputJetSynchplot'+str(ialg)+'_0.txt'
            os.system('cp '+template3+' '+config3)
            os.system('sed s%INPUTDIRECTORY%'+args.output+'correction/%g '+config3+' --in-place')
            os.system('sed s%ALGORITHM%'+alg+'%g '+config3+' --in-place')
            os.system('sed s%OUTPUTDIRECTORY%'+args.output+'correction/%g '+config3+' --in-place')
            os.system('sed s%FIXEDRANGE%false%g '+config3+' --in-place')
            
            #Synchplot with L1 corrections applied
            config3=args.output+'batchInputJetSynchplot'+str(ialg)+'_1.txt'
            os.system('cp '+template3+' '+config3)
            os.system('sed s%INPUTDIRECTORY%'+args.output+'correctionL1/%g '+config3+' --in-place')
            os.system('sed s%ALGORITHM%'+alg+'%g '+config3+' --in-place')
            os.system('sed s%OUTPUTDIRECTORY%'+args.output+'correctionL1/%g '+config3+' --in-place')
            os.system('sed s%FIXEDRANGE%true%g '+config3+' --in-place')

        if args.doApplyJEC:
            #Applying the L1 corrections
            config4=args.output+'batchInputJetApplyJEC'+str(ialg)+'_0.txt'
            os.system('cp '+template4+' '+config4)
            os.system('sed s%ALGORITHM%'+alg+'%g '+config4+' --in-place')
            os.system('sed s%LEVELS%1%g '+config4+' --in-place')

            #Applying the L2L3 corrections
            config4=args.output+'batchInputJetApplyJEC'+str(ialg)+'_1.txt'
            os.system('cp '+template4+' '+config4)
            os.system('sed s%ALGORITHM%'+alg+'%g '+config4+' --in-place')
            os.system('sed \"s%LEVELS%2 3%g\" '+config4+' --in-place')

            #Apply the L1+L2L3 corrections
            config4=args.output+'batchInputJetApplyJEC'+str(ialg)+'_2.txt'
            os.system('cp '+template4+' '+config4)
            os.system('sed s%ALGORITHM%'+alg+'%g '+config4+' --in-place')
            os.system('sed \"s%LEVELS%1 2 3%g\" '+config4+' --in-place')

        if args.doJCA:
            config5=args.output+'batchInputJetCorrectionAnalyzer'+str(ialg)+'_0.txt'
            os.system('cp '+template5+' '+config5)
            os.system('sed s%ALGORITHM%'+alg+'%g '+config5+' --in-place')
            os.system('sed s%DRMAX%'+str(float(re.findall(r'\d+', alg)[0])/20.0)+'%g '+config5+' --in-place')

        if args.doJDCTR:
            config6=args.output+'batchInputJetDrawCorrectionsTDRRatio'+str(ialg)+'_0.txt'
            os.system('cp '+template6+' '+config6)
            os.system('sed s%ALGORITHM%'+alg+'%g '+config6+' --in-place')

if __name__ == '__main__':
    #program name available through the %(prog)s command
    #can use prog="" in the ArgumentParser constructor
    #can use the type=int option to make the parameters integers
    #can use the action='append' option to make a list of options
    parser = argparse.ArgumentParser(description="Setup the directory structure of the folder used to create a given JEC era.",
                                     epilog="And those are the options available. Deal with it.",
                                     formatter_class=SmartFormatter)
    parser.add_argument("--debug", help="Shows some extra information in order to debug this program",
                        action="store_true")
    parser.add_argument('--doSynchtest' , help="Makes configuration files for jet_synchtest_x.",
                        action="store_true")
    parser.add_argument('--doSynchfit'  , help="Makes configuration files for jet_synchfit_x.",
                        action="store_true")
    parser.add_argument('--doSynchplot' , help="Makes configuration files for jet_synchplot_x.",
                        action="store_true")
    parser.add_argument('--doApplyJEC'  , help="Makes configuration files for jet_apply_jec_x.",
                        action="store_true")
    parser.add_argument('--doJRA'       , help="Makes configuration files for jet_response_analyzer_x.",
                        action="store_true")
    parser.add_argument('--doJRF'       , help="Makes configuration files for jet_response_fitter_x.",
                        action="store_true")
    parser.add_argument('--doJRAR'      , help="Makes configuration files for jet_response_and_resolution_x.",
                        action="store_true")
    parser.add_argument('--doJCA'       , help="Makes configuration files for jet_correction_analyzer_x.",
                        action="store_true")
    parser.add_argument('--doJDCTR'     , help="Makes configuration files for jet_draw_corrections_TDR_ratio_x.",
                        action="store_true")
    parser.add_argument("-e", "--era", help="Input era",
                        type=str, action='store')
    parser.add_argument('-o','--output', help='Output path',
                        type=str, action='store')    
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.",
                        action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s 1.1', help=dedent("""\
                         R|Prints the current version of the code.
                         V1.0 Used OptionParser instead of argparse. Also no implementation of functions.
                         V1.1 Implemented the argparser. Changes to code structure only.
                         """))
    args = parser.parse_args()

    if(args.debug):
        print 'Number of arguments:', len(sys.argv), 'arguments.'
        print 'Argument List:', str(sys.argv)
        print "Argument ", args

    main(args)        
