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
cmsDriver.py step1 --fileout file:HIG-RunIIFall17DRPremix-03204_step1.root  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-MCv2_correctPU_94X_mc2017_realistic_v9-v1/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 94X_mc2017_realistic_v11 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:2e34v40 --nThreads 8 --datamix PreMix --era Run2_2017 --python_filename HIG-RunIIFall17DRPremix-03204_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1751 || exit $? ; 
cmsRun -e -j HIG-RunIIFall17DRPremix-03204_rt.xml HIG-RunIIFall17DRPremix-03204_1_cfg.py || exit $? ; 
echo 1751 events were ran 
grep "TotalEvents" HIG-RunIIFall17DRPremix-03204_rt.xml 
if [ $? -eq 0 ]; then
    grep "Timing-tstoragefile-write-totalMegabytes" HIG-RunIIFall17DRPremix-03204_rt.xml 
    if [ $? -eq 0 ]; then
        events=$(grep "TotalEvents" HIG-RunIIFall17DRPremix-03204_rt.xml | tail -1 | sed "s/.*>\(.*\)<.*/\1/")
        size=$(grep "Timing-tstoragefile-write-totalMegabytes" HIG-RunIIFall17DRPremix-03204_rt.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
        if [ $events -gt 0 ]; then
            echo "McM Size/event: $(bc -l <<< "scale=4; $size*1024 / $events")"
        fi
    fi
fi
grep "EventThroughput" HIG-RunIIFall17DRPremix-03204_rt.xml 
if [ $? -eq 0 ]; then
  var1=$(grep "EventThroughput" HIG-RunIIFall17DRPremix-03204_rt.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
  echo "McM time_event value: $(bc -l <<< "scale=4; 1/$var1")"
fi
echo CPU efficiency info:
grep "TotalJobCPU" HIG-RunIIFall17DRPremix-03204_rt.xml 
grep "TotalJobTime" HIG-RunIIFall17DRPremix-03204_rt.xml 

cmsDriver.py step2 --filein file:HIG-RunIIFall17DRPremix-03204_step1.root --fileout file:HIG-RunIIFall17DRPremix-03204.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v11 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 8 --era Run2_2017 --python_filename HIG-RunIIFall17DRPremix-03204_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1751 || exit $? ; 
cmsRun -e -j HIG-RunIIFall17DRPremix-03204_2_rt.xml HIG-RunIIFall17DRPremix-03204_2_cfg.py || exit $? ; 
echo 1751 events were ran 
grep "TotalEvents" HIG-RunIIFall17DRPremix-03204_2_rt.xml 
if [ $? -eq 0 ]; then
    grep "Timing-tstoragefile-write-totalMegabytes" HIG-RunIIFall17DRPremix-03204_2_rt.xml 
    if [ $? -eq 0 ]; then
        events=$(grep "TotalEvents" HIG-RunIIFall17DRPremix-03204_2_rt.xml | tail -1 | sed "s/.*>\(.*\)<.*/\1/")
        size=$(grep "Timing-tstoragefile-write-totalMegabytes" HIG-RunIIFall17DRPremix-03204_2_rt.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
        if [ $events -gt 0 ]; then
            echo "McM Size/event: $(bc -l <<< "scale=4; $size*1024 / $events")"
        fi
    fi
fi
grep "EventThroughput" HIG-RunIIFall17DRPremix-03204_2_rt.xml 
if [ $? -eq 0 ]; then
  var1=$(grep "EventThroughput" HIG-RunIIFall17DRPremix-03204_2_rt.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
  echo "McM time_event value: $(bc -l <<< "scale=4; 1/$var1")"
fi
echo CPU efficiency info:
grep "TotalJobCPU" HIG-RunIIFall17DRPremix-03204_2_rt.xml 
grep "TotalJobTime" HIG-RunIIFall17DRPremix-03204_2_rt.xml 
