from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from multiprocessing import Process
config = config()

config.General.workArea        = 'MC_PH_GEN'
config.General.transferOutputs = True
config.General.transferLogs    = True
config.JobType.numCores = 4
config.JobType.pluginName = 'PrivateMC'

config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 500
config.Data.totalUnits           = 100000
config.Data.outLFNDirBase        = '/store/user/{}/PHMC/'.format(getUsernameFromSiteDB())
config.Data.publication          = True

config.Site.storageSite = 'T2_UK_London_IC'

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print hte.headers

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    tasks=list()

    tasks.append(('VBFHToPseudoscalarTauTau_GEN','VBFHToPseudoscalarTauTau_M125_13TeV_powheg_pythia8_2017-GEN','VBFPS_GEN'))
    tasks.append(('VBFHToMaxMixTauTau_GEN','VBFHToMaxmixTauTau_M125_13TeV_powheg_pythia8_2017-GEN','VBFMM_GEN'))

    for task in tasks:
        print task[0]
        config.General.requestName = task[0]
        config.Data.outputPrimaryDataset = task[1]
        config.Data.outputDatasetTag = task[1]
        config.JobType.psetName = task[2]

        p = Process(target=submit, args=(config,))
        p.start()
        p.join()

