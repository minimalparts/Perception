# Production of SVM data:

Example pipeline:

    python ./mkSVMTrainingData.py ../annotation/see.raw.annot.txt 2 > svmdata.w2.txt
    python ./mkSVMWholeData.py ../data/raw/bnc.raw.see.sentences  > bnc.raw.see.sentences.svm

[Legacy?? After that, same deal: delete first two lines and any line with "UNKNOWN".]
