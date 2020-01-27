# Work in-progress - current README

### Data

The *annotation* folder contains four subdirectories for the various corpora used in this study:

* British National Corpus (BNC)
* ACPROSE (Academic section of the BNC -- all texts markes with \<acprose\> in the XML)
* PHILO (Philosophy of perception corpus)
* Stanford Encyclopedia of Philosophy (SEP)

The study is specifically focused on lexical entries *see* and *aware*. Usage samples from BNC, PHILO and SEP have been manually annotated to distinguish perceptual vs non-perceptual usages. The directory contains the normalised annotations for those three corpora. For comparison purposes, 1500 random sentences of ACPROSE are contained in the same folder, but those were *automatically* annotated (see below).

In addition to the annotation, the directory contains the contextualised vectors for *see* and *aware*, as obtained through BERT Base, for each annotated sentence. The images below show the class distribution for each corpus, after reducing the BERT vectors to 2D with PCA.

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



### Similarity between corpora

We first check how a model trained on one corpus fares on the other corpora. We first give results for *see*:

<table>
<tr>
<td></td><td><b>BNC</b></td><td><b>SEP</b></td><td><b>PHILO</b></td>
</tr>
<tr>
<td><b>Baseline</b><td>70%</td><td>59%</td><td>60%</td>
</tr>
<tr>
<td><b>BNC</b><td>-</td><td>96%</td><td>83%</td>
</tr>
<tr>
<td><b>SEP</b><td>88%</td><td>-</td><td>94%</td>
</tr>
<tr>
<td><b>PHILO</b><td></td><td></td><td>-</td>
</tr>
</table>


Results for *aware* are as follows:

<table>
<tr>
<td></td><td><b>BNC</b></td><td><b>SEP</b></td><td><b>PHILO</b></td>
</tr>
<tr>
<td><b>Baseline</b><td>77%</td><td>59%</td><td>91%</td>
</tr>
<tr>
<td><b>BNC</b><td>-</td><td>86%</td><td>88%</td>
</tr>
<tr>
<td><b>SEP</b><td>89%</td><td>-</td><td>92%</td>
</tr>
<tr>
<td><b>PHILO</b><td></td><td></td><td>-</td>
</tr>
</table>
