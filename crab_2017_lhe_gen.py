from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from multiprocessing import Process
config = config()

config.General.workArea        = 'MC_PH_GEN_20Nov18'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000

config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 500
config.Data.totalUnits           = 5000000
config.Data.outLFNDirBase        = '/store/user/{}/PHMC_20Nov18/'.format(getUsernameFromSiteDB())
config.Data.publication          = True

config.Site.storageSite = 'T2_UK_London_IC'
config.Site.blacklist = ['T2_RU_*']

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

    # tasks.append(('VBFHToPseudoscalarTauTau_GEN','VBFHToPseudoscalarTauTau_M125_13TeV_powheg_pythia8_2017-GEN_TEST4','VBFPS_GEN'))
    # tasks.append(('VBFHToMaxmixTauTau_GEN','VBFHToMaxmixTauTau_M125_13TeV_powheg_pythia8_2017-GEN_TEST4','VBFMM_GEN'))

    tasks.append(('GluGluHToPseudoScalarTauTau_GEN','GluGluHToPseudoscalarTauTau_M125_13TeV_powheg_pythia8_2017-GEN_TEST','ggHPS_GEN'))
    tasks.append(('GluGluHToMaxmixTauTau_GEN','GluGluHToMaxmixTauTau_M125_13TeV_powheg_pythia8_2017-GEN_TEST','ggHMM_GEN'))

    for task in tasks:
        print task[0]
        config.General.requestName = task[0]
        config.Data.outputPrimaryDataset = task[1]
        config.Data.outputDatasetTag = task[1]
        config.JobType.psetName = '{}.py'.format(task[2])

        p = Process(target=submit, args=(config,))
        p.start()
        p.join()

