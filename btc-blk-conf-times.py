#!/usr/bin/python3

import json
import subprocess
import sys
import datetime

blockchainCLI = 'bitcoin-cli'
confirmTimes = []
try:
    blockCount = int(sys.argv[1])
except IndexError:
    blockCount = 1

countProc = subprocess.Popen( [blockchainCLI, 'getblockcount'],
                            stdout=subprocess.PIPE )
blockHeight = int(countProc.stdout.read().decode('utf-8'))

def getBlockConfirmTime(blockNum):
    hashProc = subprocess.Popen( [blockchainCLI, 'getblockhash', str(blockNum)],
                                stdout=subprocess.PIPE )
    blockHash = hashProc.stdout.read().decode('utf-8')
    
    blockProc = subprocess.Popen( [blockchainCLI, 'getblock', blockHash],
                                stdout=subprocess.PIPE )
    blockData = blockProc.stdout.read().decode('utf-8')
    block = json.loads(blockData)
    blockConfirmTimestamp = int(block['time'])
    return blockConfirmTimestamp

for block in range(blockCount):
    currentBlockTime = getBlockConfirmTime(blockHeight - block)
    previousBlockTime = getBlockConfirmTime(blockHeight - block - 1)
    timeToConfirmSec = currentBlockTime - previousBlockTime
    confirmTimes.append(timeToConfirmSec)
    timeToConfirmBlock = str(datetime.timedelta(
                            seconds=(timeToConfirmSec)))
    blockConfirmTime = datetime.datetime.fromtimestamp(
            currentBlockTime).strftime('%m-%d-%Y %H:%M:%S')

    print("Block %d" % (blockHeight - block,))
    print("Block Confirmed at: %s" % (blockConfirmTime,))
    print("Time to Confirm Block: %s" % (timeToConfirmBlock,))
    
if blockCount > 1:
    avgConfirmTime = sum(confirmTimes) / blockCount
    formattedAvg = str(datetime.timedelta(seconds=avgConfirmTime))
    print("\nAverage Time to Confirm Block: %s" % (formattedAvg,))
