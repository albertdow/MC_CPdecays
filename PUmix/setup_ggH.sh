#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc630
if [ -r CMSSW_9_4_7/src ] ; then 
 echo release CMSSW_9_4_7 already exists
else
scram p CMSSW CMSSW_9_4_7
fi
cd CMSSW_9_4_7/src
eval `scram runtime -sh`


scram b
cd ../../
cmsDriver.py step1 --filein "file:test_gen.root" --fileout file:test_pumix.root  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-MCv2_correctPU_94X_mc2017_realistic_v9-v1/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 94X_mc2017_realistic_v11 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:2e34v40 --nThreads 8 --datamix PreMix --era Run2_2017 --python_filename run_pumix.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 100 || exit $? ; 

cp run_pumix.py CMSSW_9_4_7/src/Submit/

cmsDriver.py step2 --filein file:test_pumix.root --fileout file:test_aod.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v11 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 8 --era Run2_2017 --python_filename run_aod.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 100 || exit $? ; 

cp run_aod.py CMSSW_9_4_7/src/Submit/

cp crab_pumix.py CMSSW_9_4_7/src/Submit/
cp test_gen.root CMSSW_9_4_7/src/Submit/
