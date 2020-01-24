## Work in-progress - current README

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
     </td>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/SEP/SEP_aware.png" />
     </td>
     <td>
     <img style="vertical-align: bottom;" width="100%" height="100%" src="https://github.com/minimalparts/Perception/blob/master/annotation/PHILO/PHILO_aware.png" />
     </td>
   </tr>
</table>


