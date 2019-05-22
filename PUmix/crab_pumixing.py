from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from multiprocessing import Process
config = config()

config.General.requestName     = 'PUMIX'
config.General.workArea        = 'PUMIX'
config.General.transferOutputs = True
config.General.transferLogs    = True
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 15000

config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName   = 'run_pumix.py'

config.Data.inputDBS             = 'phys03'
config.Data.splitting            = 'EventAwareLumiBased'
config.Data.unitsPerJob          = 1600
config.Data.totalUnits           = -1
config.Data.outLFNDirBase        = '/store/user/{}/MG5MC_2016/'.format(getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.ignoreLocality      = True

config.Site.whitelist   = ['T2_*','T1_*','T3_*']
config.Site.storageSite = 'T2_UK_London_IC'

#config.Data.outputDatasetTag = 'GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-PUMIX'
#config.General.requestName = 'GluGluToHToTauTau_M125_MG5'
#config.Data.inputDataset = '/GluGluToPseudoscalarHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-GEN/dwinterb-GluGluToPseudoscalarHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-GEN_RAWSIMoutput-3fa654e8a8bdbd48dc7b69a77be7238d/USER'


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

    tasks.append(('GluGluToHToTauTau_M125_MG5', '/GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-GEN/dwinterb-GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-GEN_RAWSIMoutput-49464db14bc113525fbdfe2a7aee8889/USER', 'GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-PUMIX'))

    tasks.append(('GluGluToMaxmixHToTauTau_M125_MG5', '/GluGluToMaxmixHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-GEN/dwinterb-GluGluToMaxmixHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-GEN_RAWSIMoutput-c288e5b87904e9278cf7f18297debdb0/USER', 'GluGluToMaxmixHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-PUMIX'))

    for task in tasks:
        print task[0]
        config.Data.outputDatasetTag = task[2]
        config.General.requestName = task[2]
        config.Data.inputDataset = task[1]
        #submit(config)

        p = Process(target=submit, args=(config,))
        p.start()
        p.join()



