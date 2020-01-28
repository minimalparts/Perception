# Work in-progress - current README

### Data

The *annotation* folder contains four subdirectories for the various corpora used in this study:

* British National Corpus (BNC)
* ACPROSE (Academic section of the BNC -- all texts markes with \<acprose\> in the XML)
* PHILO (Philosophy of perception corpus)
* Stanford Encyclopedia of Philosophy (SEP)

The study is specifically focused on lexical entries *see* and *aware*. Usage samples from BNC, PHILO and SEP have been manually annotated to distinguish perceptual vs non-perceptual usages. The directory contains the normalised annotations for those three corpora. For comparison purposes, 1500 random sentences of ACPROSE are contained in the same folder, but those were *automatically* annotated (see below).

In addition to the annotation, the directory contains the contextualised vectors for *see* and *aware*, as obtained through BERT Base, for each annotated sentence. The images below show the class distribution for each of the annotated corpora, after reducing the BERT vectors to 2D with PCA.

<table border=0 >
   <tr>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/BNC/BNC_see.png" />
     </td>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/SEP/SEP_see.png" />
     </td>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/PHILO/PHILO_see.png" />
     </td>
   </tr>
   <tr>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/BNC/BNC_aware.png" />
     </td>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/SEP/SEP_aware.png" />
     </td>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/PHILO/PHILO_aware.png" />
     </td>
   </tr>
</table>

Below, we also show the class distribution for the automatically annotated ACPROSE, using the BNC background model (using SEP results in very little difference).

<table border=0>
  <tr>
    <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/ACPROSE/ACPROSE_see_BNC.png" />
     </td>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/ACPROSE/ACPROSE_aware_BNC.png" />
     </td>
  </tr>
</table>


### Training

The *training* directory contains code to train a perceptual vs non-perceptual classifier, using as input the BERT vectors extracted from the data. The classifier can only be trained for corpora for which we have annotation, so BNC, PHILO and SEP. The classifier is a simple MLP with two hidden layers and RELu activation, with softmax on the output layer.

The training regime is as follows. For a given dataset, we first retain 200 instances for the optimisation of the model. Tuning is performed using *optimise.py*, which relies on Bayesian Optimisation (BayesOpt). BayesOpt is run for 200 iterations before returning the best set of hyperparameters.

    python3 optimise.py BNC see

The best hyperparameters can be printed in a user-friendly way using the following command over the json file generated in the relevant directory:

    python3 read_json.py <path to json file>

Once the system is tuned on a dataset, we perform 5-fold cross-validation on the rest of the data. E.g.

    python3 classify.py --file=BNC/BNC_see_kfold_features.txt --lr=0.01 --batch=46 --epochs=50 --hidden=323 --wdecay=0.01

There is CUDA support for running on GPU.

Results for *see* are as follows (accuracy averages over 5-folds):

<table>
<tr>
<td><b>BNC</b></td><td><b>SEP</b></td><td><b>PHILO</b></td>
</tr>
<tr>
<td>90%</td><td>98%</td><td></td>
</tr>
</table>


Results for *aware* are as follows (accuracy averages over 5-folds):

<table>
<tr>
<td><b>BNC</b></td><td><b>SEP</b></td><td><b>PHILO</b></td>
</tr>
<tr>
<td>90%</td><td>98%</td><td></td>
</tr>
</table>



### Similarity between corpora

#### Cross-domain classification

We first check how a model trained on one corpus fares on the other corpora. We first give results for *see*:

<table>
<tr>
<td></td><td><b>BNC</b></td><td><b>SEP</b></td><td><b>PHILO</b></td>
</tr>
<tr>
<td><b>Baseline</b><td>71%</td><td>59%</td><td>60%</td>
</tr>
<tr>
<td><b>BNC</b><td>-</td><td>96%</td><td>83%</td>
</tr>
<tr>
<td><b>SEP</b><td>87%</td><td>-</td><td>94%</td>
</tr>
<tr>
<td><b>PHILO</b><td>81%</td>97%<td></td><td>-</td>
</tr>
</table>


Results for *aware* are as follows:

<table>
<tr>
<td></td><td><b>BNC</b></td><td><b>SEP</b></td><td><b>PHILO</b></td>
</tr>
<tr>
<td><b>Baseline</b><td>79%</td><td>60%</td><td>91%</td>
</tr>
<tr>
<td><b>BNC</b><td>-</td><td>85%</td><td>88%</td>
</tr>
<tr>
<td><b>SEP</b><td>89%</td><td>-</td><td>92%</td>
</tr>
<tr>
<td><b>PHILO</b><td>75%</td><td>80%</td><td>-</td>
</tr>
</table>


#### N-gram distributions

We also inspect the most frequent ngrams for each corpus (with n=3).

<table>
<tr>
<td></td><td><b>BNC</b></td><td><b>ACPROSE</b></td><td><b>SEP</b></td><td><b>PHILO</b></td>
</tr>
<tr>

<td><b>see<br>(forward)</b>

<td>i saw 11<br>
she saw 8<br>
he saw 8<br>
i can see 4<br>
i do n't see 4<br>
i ca n't see 4<br>
you want to see 4<br>
to come and see 3<br>
i 've just seen 3<br>
i 've never seen 3</td>

<td>as we have seen 40<br>
as we shall see 24<br>
we have seen 13<br>
we have already seen 11<br>
it can be seen 9<br>
as can be seen 7<br>
can also be seen 7<br>
, we can see 7<br>
is difficult to see 5<br>
remains to be seen 5<br>
</td>

<td>as we have seen 43<br>
is hard to see 19<br>
to see 19<br>
as we shall see 14<br>
we have seen 10<br>
as we will see 8<br>
we see 8<br>
as we saw 8<br>
in order to see 7<br>
we have already seen 7</td>

<td>as we have seen 78<br>
as we shall see 40<br>
we have already seen 33<br>
we have seen 26<br>
i do not see 25<br>
we saw 21<br>
as i can see 21<br>
is difficult to see 20<br>
that i am seeing 20<br>
, as we saw 20<br>
</td>
</tr>

<tr>
<td><b>aware<br>(forward)</b>
<td>need to be aware 14<br>
she was aware 12<br>
he was aware 8<br>
i am aware 8<br>
we are not aware 6<br>
should be made aware 6<br>
you should be aware 5<br>
be aware 4<br>
to be fully aware 4<br>
being aware 4<br>
</td>

<td>need to be aware 19<br>
important to be aware 12<br>
we are not aware 8<br>
needs to be aware 7<br>
may not be aware 6<br>
we are aware 6<br>
to be more aware 5<br>
necessary to be aware 5<br>
he was aware 5<br>
being aware 5<br>
</td>

<td>one is directly aware 23<br>
we are directly aware 17<br>
we are not aware 15<br>
that we are aware 12<br>
we are immediately aware 11<br>
that he was aware 6<br>
that i am aware 6<br>
can be directly aware 6<br>
i am directly aware 5<br>
which we are aware 5<br>
</td>

<td>we are directly aware 13<br>
that we are aware 11<br>
hallucinating subject is aware 9<br>
what we are aware 9<br>
we are immediately aware 8<br>
are not directly aware 6<br>
, we are aware 6<br>
that i am aware 5<br>
i am immediately aware 5<br>
we are not aware 4<br>
</td>
</tr>
</table>


