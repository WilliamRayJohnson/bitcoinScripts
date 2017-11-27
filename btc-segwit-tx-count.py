#!/usr/bin/python3

import json
import subprocess
import sys
import datetime

cli = 'bitcoin-cli'

try:
    blockCount = int(sys.argv[1])
except IndexError:
    blockCount = 1

countProc = subprocess.Popen( [cli, 'getblockcount'],
                            stdout=subprocess.PIPE )
blockHeight = int(countProc.stdout.read().decode('utf-8'))
segwitPercentages = []

def getTransactions(blockNum):
    hashProc = subprocess.Popen([cli, 'getblockhash', str(blockNum)],
                                stdout=subprocess.PIPE)
    blockHash = hashProc.stdout.read().decode('utf-8')
    blockProc = subprocess.Popen([cli, 'getblock', blockHash],
                                stdout=subprocess.PIPE)
    blockData = blockProc.stdout.read().decode('utf-8')
    block = json.loads(blockData)
    tx = block['tx']
    return tx

def isSegwitTx(txid):
    segwitTx = False
    txProc = subprocess.Popen([cli, 'getrawtransaction', txid],
                            stdout=subprocess.PIPE)
    rawTx = txProc.stdout.read().decode('utf-8').replace('\n', '')
    try:
        decodeProc = subprocess.Popen([cli, 'decoderawtransaction', rawTx],
                                stdout=subprocess.PIPE)
        decodedTxData = decodeProc.stdout.read().decode('utf-8')
        decodedTx = json.loads(decodedTxData)
        if 'txinwitness' in decodedTx['vin'][0]:
            segwitTx = True
    except OSError:
        segwitTx = False
    return segwitTx

for block in range(blockCount):
    segwitTxid = []
    currTxin = getTransactions(blockHeight - block)
    for tx in currTxin:
        if isSegwitTx(tx):
            segwitTxid.append(tx)
    percentage = len(segwitTxid)/len(currTxin) * 100
    segwitPercentages.append(percentage)
    print("--------------------------------------------")
    print("Block: %d" % (blockHeight - block))
    print("Segwit Transactions: %d" % len(segwitTxid))
    print("Percent Segwit txin in Block: %.0f%%" % percentage)
print("--------------------------------------------")

if blockCount > 1:
    avgSegwitPercent = sum(segwitPercentages)/blockCount
    print("\nAverage Segwit Usage per Block: %.0f%%" % avgSegwitPercent)
