# Code to use with SVMlight

### Run perception training:

Example pipeline:

    cat aware.svmdata.w4.txt|sort -R > perception/aware/aware.svmdata.w4.shuffled.txt
    python mkFolds.py perception/aware/aware.svmdata.w4.shuffled.txt perception/aware/w4/fold 5
    ./runPerception > perception/aware/w4/results.w4.txt

### Run on entire corpus:

    ./svm_learn -c 80 -t 2 perception/aware/w8/allfolds perception/aware/w8/allfolds.model
    ./svm_classify perception/aware/w8/entire_corpus_data.tst perception/aware/w8/allfolds.model perception/aware/w8/entire_corpus_data.predict
