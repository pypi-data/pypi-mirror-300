# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:37:16 2022

@author: svc_ccg
"""

import argparse
import itertools
import os
import pathlib
import random
import numpy as np
import pandas as pd
import scipy.optimize
import scipy.stats
import sklearn.metrics
import psytrack
import ssm
from  DynamicRoutingAnalysisUtils import getFirstExperimentSession, getSessionsToPass, getSessionData


baseDir = pathlib.Path('//allen/programs/mindscope/workgroups/dynamicrouting')


def getSessionsToFit(mouseId,trainingPhase,sessionIndex):
    if trainingPhase == 'opto':
        optoLabel = 'lFC'
        df = pd.read_excel(os.path.join(baseDir,'Sam','OptoExperiments.xlsx'),sheet_name=str(mouseId))
        sessions = np.where(df[optoLabel] & ~(df['unilateral'] & df['bilateral']))[0]
        testSession = sessions[sessionIndex]
        trainSessions = [s for s in sessions if s != testSession]
    else:
        drSheets,nsbSheets = [pd.read_excel(os.path.join(baseDir,'DynamicRoutingTask',fileName),sheet_name=None) for fileName in ('DynamicRoutingTraining.xlsx','DynamicRoutingTrainingNSB.xlsx')]
        df = drSheets[str(mouseId)] if str(mouseId) in drSheets else nsbSheets[str(mouseId)]
        preExperimentSessions = np.array(['stage 5' in task for task in df['task version']]) & ~np.array(df['ignore'].astype(bool))
        firstExperimentSession = getFirstExperimentSession(df)
        if firstExperimentSession is not None:
            preExperimentSessions[firstExperimentSession:] = False
        preExperimentSessions = np.where(preExperimentSessions)[0]
        if trainingPhase in ('initial training','after learning','clusters'):
            if trainingPhase == 'initial training':
                sessions = preExperimentSessions[:5]
            elif trainingPhase == 'after learning':
                sessionsToPass = getSessionsToPass(mouseId,df,preExperimentSessions,stage=5)
                sessions = preExperimentSessions[sessionsToPass:sessionsToPass+5]
            elif trainingPhase == 'clusters':
                sessions = preExperimentSessions
            testSession = sessions[sessionIndex]
            trainSessions = [s for s in sessions if s != testSession]
        else:
            sessions = np.array([trainingPhase in task for task in df['task version']]) & ~np.array(df['ignore'].astype(bool))
            sessions = np.where(sessions)[0]
            testSession = sessions[sessionIndex]
            # trainSessions = preExperimentSessions[-4:]
            trainSessions = [s for s in sessions if s != testSession]
    testData = getSessionData(mouseId,df.loc[testSession,'start time'])
    trainData = [getSessionData(mouseId,startTime) for startTime in df.loc[trainSessions,'start time']]
    if trainingPhase == 'clusters':
        clustData = np.load(os.path.join(baseDir,'Sam','clustData.npy'),allow_pickle=True).item()
        trainDataTrialCluster = [clustData['trialCluster'][str(mouseId)][startTime.strftime('%Y%m%d_%H%M%S')] for startTime in df.loc[trainSessions,'start time']]
    else:
        trainDataTrialCluster = None
    return testData,trainData,trainDataTrialCluster


def calcLogisticProb(q,beta,bias,lapse):
    return (1 - lapse) / (1 + np.exp(-beta * (q - 0.5 + bias)))


def runModel(obj,betaAction,biasAction,lapseRate,biasAttention,visConfidence,audConfidence,wContext,alphaContext,decayContext,
             alphaReinforcement,rewardBias,rewardBiasDecay,noRewardBias,noRewardBiasTau,alphaPerseveration,decayPerseveration,
             betaActionOpto,biasActionOpto,wContextOpto,
             optoLabel=None,useHistory=True,nReps=1):

    stimNames = ('vis1','vis2','sound1','sound2')
    stimConfidence = [visConfidence,audConfidence]
    modality = 0

    pContext = 0.5 + np.zeros((nReps,obj.nTrials,2))
    qContext = np.array([visConfidence,1-visConfidence,audConfidence,1-audConfidence])

    qReinforcement = np.zeros((nReps,obj.nTrials,len(stimNames)))
    qReinforcement[:,0] = [visConfidence,1-visConfidence,audConfidence,1-audConfidence]

    qPerseveration = np.zeros((nReps,obj.nTrials,len(stimNames)))

    qReward = np.zeros((nReps,obj.nTrials))

    qNoReward = np.zeros((nReps,obj.nTrials))

    qTotal = np.zeros((nReps,obj.nTrials))

    pAction = np.zeros((nReps,obj.nTrials))
    
    action = np.zeros((nReps,obj.nTrials),dtype=int)
    
    for i in range(nReps):
        lastRewardTime = 0
        for trial,stim in enumerate(obj.trialStim):
            if optoLabel is not None and obj.trialOptoLabel[trial] in optoLabel:
                betaAct = betaActionOpto if betaActionOpto > 0 else betaAction
                biasAct = biasActionOpto if biasActionOpto > 0 else biasAction
                wCntx = wContextOpto if wContextOpto > 0 else wContext
            else:
                betaAct = betaAction
                biasAct = biasAction
                wCntx = wContext

            if stim != 'catch':
                modality = 0 if 'vis' in stim else 1
                pStim = np.zeros(len(stimNames))
                pStim[[stim[:-1] in s for s in stimNames]] = [stimConfidence[modality],1-stimConfidence[modality]] if '1' in stim else [1-stimConfidence[modality],stimConfidence[modality]]
                if biasAttention > 0:
                    pStim[-2:] *= 1 - biasAttention
                else:
                    pStim[:2] *= 1 + biasAttention

                if wCntx > 0:
                    expectedValue = ((wCntx * np.sum(qContext * pStim * np.repeat(pContext[i,trial],2))) + 
                                     ((1-wCntx) * np.sum(qReinforcement[i,trial] * pStim)))
                elif alphaContext > 0:
                    expectedValue = np.sum(qReinforcement[i,trial] * pStim * np.repeat(pContext[i,trial],2))
                else:
                    expectedValue = np.sum(qReinforcement[i,trial] * pStim)

                qTotal[i,trial] = expectedValue
                qTotal[i,trial] += np.sum(qPerseveration[i,trial] * pStim) + qReward[i,trial] + qNoReward[i,trial]

                pAction[i,trial] = calcLogisticProb(qTotal[i,trial],betaAct,biasAct,lapseRate)
                
                if useHistory:
                    action[i,trial] = obj.trialResponse[trial]
                elif random.random() < pAction[i,trial]:
                    action[i,trial] = 1 
            
            if trial+1 < obj.nTrials:
                pContext[i,trial+1] = pContext[i,trial]
                qReinforcement[i,trial+1] = qReinforcement[i,trial]
                qPerseveration[i,trial+1] = qPerseveration[i,trial]
                qReward[i,trial+1] = qReward[i,trial]
                qNoReward[i,trial+1] = qNoReward[i,trial]
                
                outcome = (action[i,trial] and stim == obj.rewardedStim[trial]) or obj.autoRewardScheduled[trial]
                resp = action[i,trial] or obj.autoRewardScheduled[trial]
                if outcome:
                    lastRewardTime = obj.trialStartTimes[trial]
                
                if stim != 'catch':
                    if resp:
                        if alphaContext > 0:
                            if outcome:
                                contextError = 1 - pContext[i,trial,modality]
                            else:
                                contextError = -pContext[i,trial,modality] * pStim[(0 if modality==0 else 2)]
                            pContext[i,trial+1,modality] += alphaContext * contextError
                            pContext[i,trial+1,modality] = np.clip(pContext[i,trial+1,modality],0,1)
                    
                        if alphaReinforcement > 0:
                            predictionError = pStim * (outcome - qReinforcement[i,trial])
                            if wContext == 0 and alphaContext > 0:
                                predictionError *= np.repeat(pContext[i,trial],2)
                            qReinforcement[i,trial+1] += alphaReinforcement * predictionError
                            qReinforcement[i,trial+1] = np.clip(qReinforcement[i,trial+1],0,1)
                
                    if alphaPerseveration > 0:
                        qPerseveration[i,trial+1] += alphaPerseveration * pStim * (resp - qPerseveration[i,trial])
                
                iti = obj.trialStartTimes[trial+1] - obj.trialStartTimes[trial]

                if decayPerseveration > 0:
                    qPerseveration[i,trial+1] *= np.exp(-iti/perseverationDecay)

                if rewardBiasDecay > 0:
                    if outcome > 0:
                        qReward[i,trial+1] += rewardBias
                    qReward[i,trial+1] *= np.exp(-iti/rewardBiasDecay)

                if noRewardBiasTau > 0:
                    if outcome > 0:
                        qNoReward[i,trial+1] = 0
                    else:
                        qNoReward[i,trial+1] = noRewardBias * np.exp((obj.trialStartTimes[trial+1] - lastRewardTime)/noRewardBiasTau)

                if decayContext > 0:
                    pContext[i,trial+1,modality] += (1 - np.exp(-iti/decayContext)) * (0.5 - pContext[i,trial+1,modality])
                pContext[i,trial+1,(1 if modality==0 else 0)] = 1 - pContext[i,trial+1,modality]
    
    return pContext, qReinforcement, qReward, qTotal, pAction, action


def insertFixedParamVals(fitParams,fixedInd,fixedVal):
    nParams = len(fitParams) + (len(fixedVal) if isinstance(fixedVal,list) else 1)
    params = np.full(nParams,np.nan)
    params[fixedInd] = fixedVal
    params[np.isnan(params)] = fitParams
    return params


def calcPrior(params):
    delta = 0.025
    p = 1
    for i,val in enumerate(params):
        if i in (5,8,10,12,14):
            f = scipy.stats.norm(0,0.5).cdf
            p *= f(val+delta) - f(val-delta)
        elif i in (6,9,11,13):
            f = scipy.stats.beta(2,2).cdf
            p *= f(val+delta) - f(val-delta)
    return p


def getModelRegressors(modelType,modelTypeDict,params,sessions):
    regressors = ['context','reinforcement','reward','bias']
    x = {r: [] for r in regressors}
    y = []
    sessionTrials = []
    for obj in sessions:
        for reg in regressors[:-1]:
            betaAction,biasAction,biasAttention,visConfidence,audConfidence,wContext,alphaContext,decayContext,alphaReinforcement,wReward,alphaReward,wPerseveration,alphaPerseveration = params
            if reg == 'context':
                wContext = 1
                wReward = 0
            elif reg == 'reinforcement':
                wContext = 0
                alphaContext = 0
                wReward = 0
            elif reg == 'reward':
                wContext = 0
                alphaContext = 0
                wReward = 1
            params = (betaAction,biasAction,biasAttention,visConfidence,audConfidence,wContext,alphaContext,decayContext,alphaReinforcement,wReward,alphaReward,wPerseveration,alphaPerseveration)
            x[reg].append(runModel(obj,*params,**modelTypeDict)[-2][0])
        x['bias'].append(np.ones(obj.nTrials))
        y.append(obj.trialResponse)
        sessionTrials.append(obj.nTrials)
    if modelType == 'psytrack':
        d = {'inputs': {key: np.concatenate(val)[:,None] for key,val in x.items()},
             'y': np.concatenate(y).astype(float),
             'dayLength': np.array(sessionTrials)}
        weights = {key: 1 for key in d['inputs']}
        nWeights = sum(weights.values())
        hyper= {'sigInit': 2**4.,
                'sigma': [2**-4.] * nWeights,
                'sigDay': [2**-4.] * nWeights}
        optList = ['sigma','sigDay']
        return d,weights,hyper,optList
    elif modelType == 'glmhmm':
        # list of ntrials x nregressors array for each session
        inputs = [np.stack([x[reg][i] for reg in regressors],axis=-1) for i in range(len(y))]
        resp = [a[:,None].astype(int) for a in y]
        return inputs,resp


def evalModel(params,*args):
    trainData,trainDataTrialCluster,clust,fixedInd,fixedVal,modelType,modelTypeDict = args
    if fixedInd is not None:
        params = insertFixedParamVals(params,fixedInd,fixedVal)
    if modelType == 'psytrack':
        d,weights,hyper,optList = getModelRegressors(modelType,modelTypeDict,params,trainData)
        try:
            hyp,evd,wMode,hessInfo = psytrack.hyperOpt(d,hyper,weights,optList)
            return -evd
        except:
            return 1e6
    elif modelType == 'glmhmm':
        nCategories = 2 # binary choice (go/nogo)
        obsDim = 1 # number of observed dimensions (choice)
        inputDim = 4 # input dimensions
        nStates = 3
        # list of ntrials x nregressors array for each session
        inputs,resp = getModelRegressors(modelType,modelTypeDict,params,trainData)
        glmhmm = ssm.HMM(nStates,obsDim,inputDim,observations="input_driven_obs",observation_kwargs=dict(C=nCategories),transitions="standard")
        fitLL = glmhmm.fit(resp,inputs,method="em",num_iters=200,tolerance=10**-4)
        return -fitLL[-1]
    else:
        response = np.concatenate([obj.trialResponse for obj in trainData])
        prediction = np.concatenate([runModel(obj,*params,**modelTypeDict)[-2][0] for obj in trainData])
        if clust is not None:
            clustTrials = np.concatenate(trainDataTrialCluster) == clust
            response = response[clustTrials]
            prediction = prediction[clustTrials]
        elif 'optoLabel' in modelTypeDict and modelTypeDict['optoLabel'] is not None:
            trials = np.concatenate([np.in1d(obj.trialOptoLabel,('no opto',)+modelTypeDict['optoLabel']) for obj in trainData])
            response = response[trials]
            prediction = prediction[trials]
        logLoss = sklearn.metrics.log_loss(response,prediction)
        # logLoss += -np.log(calcPrior(params))
        return logLoss


def fitModel(mouseId,trainingPhase,testData,trainData,trainDataTrialCluster):
    betaActionBounds = (3,30)
    biasActionBounds = (-0.5,0.5)
    lapseRateBounds = (0,0.5)
    biasAttentionBounds = (-1,1)
    visConfidenceBounds = (0.5,1)
    audConfidenceBounds = (0.5,1)
    wContextBounds = (0,1)
    alphaContextBounds = (0,1)
    decayContextBounds = (10,300) 
    alphaReinforcementBounds = (0,0.5)
    rewardBiasBounds = (0,0.5)
    rewardBiasDecayBounds = (1,30)
    noRewardBiasBounds = (0,0.5)
    noRewardBiasTauBounds = (10,600)
    alphaPerseverationBounds = (0,1)
    decayPerseverationBounds = (1,120)

    betaActionOptoBounds = (3,30)
    biasActionOptoBounds = (-0.5,0.5)
    wContextOptoBounds = (0,1)

    bounds = (betaActionBounds,biasActionBounds,lapseRateBounds,biasAttentionBounds,visConfidenceBounds,audConfidenceBounds,
              wContextBounds,alphaContextBounds,decayContextBounds,alphaReinforcementBounds,
              rewardBiasBounds,rewardBiasDecayBounds,noRewardBiasBounds,noRewardBiasTauBounds,alphaPerseverationBounds,decayPerseverationBounds,
              betaActionOptoBounds,biasActionOptoBounds,wContextOptoBounds)

    fixedValues = [None,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]

    modelTypeParams = ('optoLabel',)
    modelTypes,modelTypeParamVals = zip(
                                        ('basicRL', (None,)),
                                        ('contextRLForgetting', (None,)),
                                        #('contextRLImpulsive', (None,)),
                                        #('mixedAgentRL', (None,)),
                                        ('perseverativeRL', (None,)),
                                        #('psytrack', (None,)),
                                        #('glmhmm', (None,)),
                                        #('contextRLOpto', (('lFC','PFC'),)),
                                        #('mixedAgentRLOpto', (('lFC','PFC'),)),
                                       )

    clustIds = np.arange(8)+1 if trainingPhase == 'clusters' else (None,)

    optParams = {'eps': 1e-3, 'maxfun': None,'maxiter': int(1e3),'locally_biased': False,'vol_tol': 1e-16,'len_tol': 1e-6}

    for modelType,modelTypeVals in zip(modelTypes,modelTypeParamVals):
        if modelType == 'basicRL':
            if trainingPhase == 'clusters':
                fixedParamIndices = ([6,7,8,12,13,14,15,16,17,18],)
            else:
                fixedParamIndices = tuple([6,7,8,12,13,14,15,16,17,18] + i for i in ([],[1],[2],[3],[4],[5],[9],[10,11]))
        elif modelType == 'contextRLForgetting':
            if trainingPhase == 'clusters':
                fixedParamIndices = ([6,12,13,14,15,16,17,18],)
            else:
                fixedParamIndices = tuple([6,12,13,14,15,16,17,18] + i for i in ([],[1],[2],[3],[4],[5],[8],[9],[10,11],[8,10,11]))
        elif modelType == 'contextRLImpulsive':
            if trainingPhase == 'clusters':
                fixedParamIndices = ([6,8,14,15,16,17,18],)
            else:
                fixedParamIndices = tuple([6,8,14,15,16,17,18] + i for i in ([],[1],[2],[3],[4],[5],[9],[10,11],[12,13],[10,11,12,13]))
        elif modelType == 'mixedAgentRL':
            if trainingPhase == 'clusters':
                fixedParamIndices = ([12,13,14,15,16,17,18],)
            else:
                fixedParamIndices = tuple([12,13,14,15,16,17,18] + i for i in ([],[1],[2],[3],[4],[5],[6],[8],[9],[10,11],[6,8]))
        elif modelType == 'perseverativeRL':
            if trainingPhase == 'clusters':
                fixedParamIndices = ([6,12,13,16,17,18],)
            else:
                fixedParamIndices = tuple([6,12,13,16,17,18] + i for i in ([],[1],[2],[3],[4],[5],[8],[9],[10,11],[14,15]))
        elif modelType in ('psytrack','glmhmm'):
            fixedParamIndices = ([14,15,16,17,18],)
        elif modelType in ('contextRLOpto'):
            fixedParamIndices = tuple([6,12,13,14,15,18] + i for i in ([],[16],[17]))
        elif modelType in ('mixedAgentRLOpto'):
            fixedParamIndices = tuple([12,13,14,15] + i for i in ([],[16,17],[18]))
        fixedParamValues = [([fixedValues[j] for j in i] if isinstance(i,list) else (None if i is None else fixedValues[i])) for i in fixedParamIndices]
        modelTypeDict = {p: v for p,v in zip(modelTypeParams,modelTypeVals)}
        params = []
        logLoss = []
        terminationMessage = []
        for fixedInd,fixedVal in zip(fixedParamIndices,fixedParamValues):
            bnds = bounds if fixedInd is None else tuple(b for i,b in enumerate(bounds) if (i not in fixedInd if isinstance(fixedInd,list) else i != fixedInd))
            if trainingPhase == 'clusters':
                params.append([])
                logLoss.append([])
                terminationMessage.append([])
                prms = params[-1]
                nll = logLoss[-1]
                tm = terminationMessage[-1]
            else:
                prms = params
                nll = logLoss
                tm = terminationMessage
            for clust in clustIds:
                if clust is not None and not np.any(np.concatenate(trainDataTrialCluster) == clust):
                    if modelType == 'basicRL':
                        n = 9
                    elif modelType in ('contextRLForgetting','contextRLImpulsive'):
                        n = 11
                    elif modelType == 'mixedAgentRL':
                        n = 11
                    elif modelType == 'perseverativeRL':
                        n = 13
                    prms.append(np.full(n,np.nan))
                    nll.append(np.nan)
                    tm.append('')
                else:
                    fit = scipy.optimize.direct(evalModel,bnds,args=(trainData,trainDataTrialCluster,clust,fixedInd,fixedVal,modelType,modelTypeDict),**optParams)
                    prms.append((fit.x if fixedInd is None else insertFixedParamVals(fit.x,fixedInd,fixedVal)))
                    nll.append(fit.fun)
                    tm.append(fit.message)

        fileName = str(mouseId)+'_'+testData.startTime+'_'+trainingPhase+'_'+modelType+'.npz'
        if trainingPhase == 'opto':
            filePath = os.path.join(baseDir,'Sam','RLmodel','opto',fileName)
        elif trainingPhase == 'clusters':
            filePath = os.path.join(baseDir,'Sam','RLmodel','clusters',fileName)
        else:
            filePath = os.path.join(baseDir,'Sam','RLmodel',fileName)
        np.savez(filePath,params=params,logLoss=logLoss,terminationMessage=terminationMessage,
                 trainSessions=[obj.startTime for obj in trainData],**modelTypeDict) 
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mouseId',type=int)
    parser.add_argument('--sessionIndex',type=int)
    parser.add_argument('--trainingPhase',type=str)
    args = parser.parse_args()
    trainingPhase = args.trainingPhase.replace('_',' ')
    testData,trainData,trainDataTrialCluster = getSessionsToFit(args.mouseId,trainingPhase,args.sessionIndex)
    fitModel(args.mouseId,trainingPhase,testData,trainData,trainDataTrialCluster)
